from __future__ import annotations

from typing import Any, ClassVar

from attr import define

from openapi_python_client.parser.properties.common_attributes import CommonAttributes

from ... import schema as oai
from ...utils import PythonIdentifier
from ..errors import PropertyError
from .protocol import PropertyProtocol, Value


@define
class IntProperty(PropertyProtocol):
    """A property of type int"""

    name: str
    required: bool
    default: Value | None
    python_name: PythonIdentifier
    common: CommonAttributes = CommonAttributes()

    _type_string: ClassVar[str] = "int"
    _json_type_string: ClassVar[str] = "int"
    _allowed_locations: ClassVar[set[oai.ParameterLocation]] = {
        oai.ParameterLocation.QUERY,
        oai.ParameterLocation.PATH,
        oai.ParameterLocation.COOKIE,
        oai.ParameterLocation.HEADER,
    }
    template: ClassVar[str] = "int_property.py.jinja"

    @classmethod
    def build(
        cls,
        name: str,
        required: bool,
        default: Any,
        python_name: PythonIdentifier,
    ) -> IntProperty | PropertyError:
        checked_default = cls.convert_value(default)
        if isinstance(checked_default, PropertyError):
            return checked_default

        return cls(
            name=name,
            required=required,
            default=checked_default,
            python_name=python_name,
        )

    @classmethod
    def convert_value(cls, value: Any) -> Value | None | PropertyError:
        if value is None or isinstance(value, Value):
            return value
        converted = value
        if isinstance(converted, str):
            try:
                converted = float(converted)
            except ValueError:
                return PropertyError(f"Invalid int value: {converted}")
        if isinstance(converted, float):
            as_int = int(converted)
            if converted == as_int:
                converted = as_int
        if isinstance(converted, int) and not isinstance(converted, bool):
            return Value(python_code=str(converted), raw_value=value)
        return PropertyError(f"Invalid int value: {value}")
