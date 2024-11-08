from __future__ import annotations

from typing import Any, ClassVar

from attr import define

from openapi_python_client.parser.properties.common_attributes import CommonAttributes

from ...utils import PythonIdentifier
from .protocol import PropertyProtocol, Value


@define
class AnyProperty(PropertyProtocol):
    """A property that can be any type (used for empty schemas)"""

    @classmethod
    def build(
        cls,
        name: str,
        required: bool,
        default: Any,
        python_name: PythonIdentifier,
    ) -> AnyProperty:
        return cls(
            name=name,
            required=required,
            default=AnyProperty.convert_value(default),
            python_name=python_name,
        )

    @classmethod
    def convert_value(cls, value: Any) -> Value | None:
        from .string import StringProperty

        if value is None:
            return value
        if isinstance(value, str):
            return StringProperty.convert_value(value)
        return Value(python_code=str(value), raw_value=value)

    name: str
    required: bool
    default: Value | None
    python_name: PythonIdentifier
    common: CommonAttributes = CommonAttributes()
    read_only: bool = False
    _type_string: ClassVar[str] = "Any"
    _json_type_string: ClassVar[str] = "Any"
