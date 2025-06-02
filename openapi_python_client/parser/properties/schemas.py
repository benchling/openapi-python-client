__all__ = ["Schemas"]

from typing import Dict, List, NewType, Tuple, Union, cast
from urllib.parse import urlparse

import attr

from ... import schema as oai
from ...schema.parameter import Parameter
from ...utils import ClassName
from ..errors import ParameterError, ParseError
from .enum_property import EnumProperty
from .model_property import ModelProperty

ReferencePath = NewType("ReferencePath", str)


def parse_reference_path(ref_path_raw: str) -> Union[ReferencePath, ParseError]:
    """
    Takes a raw string provided in a `$ref` and turns it into a validated `_ReferencePath` or a `ParseError` if
    validation fails.

    See Also:
        - https://swagger.io/docs/specification/using-ref/
    """
    parsed = urlparse(ref_path_raw)
    if parsed.scheme or parsed.path:
        return ParseError(detail=f"Remote references such as {ref_path_raw} are not supported yet.")
    return cast(ReferencePath, parsed.fragment)


@attr.s(auto_attribs=True, frozen=True)
class Schemas:
    """ Structure for containing all defined, shareable, and resuabled schemas (attr classes and Enums) """

    enums: Dict[str, EnumProperty] = attr.ib(factory=dict)
    models: Dict[str, ModelProperty] = attr.ib(factory=dict)
    errors: List[ParseError] = attr.ib(factory=list)


@attr.s(auto_attribs=True, frozen=True)
class Parameters:
    """Structure for containing all defined, shareable, and reusable parameters"""

    classes_by_reference: dict[ReferencePath, Parameter] = attr.ib(factory=dict)
    classes_by_name: dict[ClassName, Parameter] = attr.ib(factory=dict)
    errors: list[ParseError] = attr.ib(factory=list)


def parameter_from_data(
    *,
    name: str,
    required: bool,
    data: Union[oai.Reference, oai.Parameter],
    parameters: Parameters,
) -> Tuple[Union[Parameter, ParameterError], Parameters]:
    """Generates parameters from an OpenAPI Parameter spec."""

    if isinstance(data, oai.Reference):
        return ParameterError("Unable to resolve another reference"), parameters

    if data.param_schema is None:
        return ParameterError("Parameter has no schema"), parameters

    new_param = Parameter(
        name=name,
        required=required,
        explode=data.explode,
        style=data.style,
        param_schema=data.param_schema,
        param_in=data.param_in,
    )
    parameters = attr.evolve(parameters, classes_by_name={**parameters.classes_by_name, name: new_param})
    return new_param, parameters


def update_parameters_with_data(
    *, ref_path: ReferencePath, data: oai.Parameter, parameters: Parameters
) -> Union[Parameters, ParameterError]:
    """
    Update a `Parameters` using some new reference.

    Args:
        ref_path: The output of `parse_reference_path` (validated $ref).
        data: The schema of the thing to add to Schemas.
        parameters: `Parameters` up until now.

    Returns:
        Either the updated `parameters` input or a `PropertyError` if something went wrong.

    See Also:
        - https://swagger.io/docs/specification/using-ref/
    """
    param, parameters = parameter_from_data(data=data, name=data.name, parameters=parameters, required=True)

    if isinstance(param, ParameterError):
        param.detail = f"{param.header}: {param.detail}"
        param.header = f"Unable to parse parameter {ref_path}"
        if isinstance(param.data, oai.Reference) and param.data.ref.endswith(ref_path):  # pragma: nocover
            param.detail += (
                "\n\nRecursive and circular references are not supported. "
                "See https://github.com/openapi-generators/openapi-python-client/issues/466"
            )
        return param

    parameters = attr.evolve(parameters, classes_by_reference={ref_path: param, **parameters.classes_by_reference})
    return parameters


def parameter_from_reference(
    *,
    param: Union[oai.Reference, Parameter],
    parameters: Parameters,
) -> Union[Parameter, ParameterError]:
    """
    Returns a Parameter from a Reference or the Parameter itself if one was provided.

    Args:
        param: A parameter by `Reference`.
        parameters: `Parameters` up until now.

    Returns:
        Either the updated `schemas` input or a `PropertyError` if something went wrong.

    See Also:
        - https://swagger.io/docs/specification/using-ref/
    """
    if isinstance(param, Parameter):
        return param

    ref_path = parse_reference_path(param.ref)

    if isinstance(ref_path, ParseError):
        return ParameterError(detail=ref_path.detail)

    _resolved_parameter_class = parameters.classes_by_reference.get(ref_path, None)
    if _resolved_parameter_class is None:
        return ParameterError(detail=f"Reference `{ref_path}` not found.")
    return _resolved_parameter_class
