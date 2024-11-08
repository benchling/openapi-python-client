from __future__ import annotations

from typing import Any, ClassVar

from attr import define
from dateutil.parser import isoparse

from openapi_python_client.parser.properties.common_attributes import CommonAttributes

from ...utils import PythonIdentifier
from ..errors import PropertyError
from .protocol import PropertyProtocol, Value


@define
class DateProperty(PropertyProtocol):
    """A property of type datetime.date"""

    name: str
    required: bool
    default: Value | None
    python_name: PythonIdentifier
    common: CommonAttributes = CommonAttributes()

    _type_string: ClassVar[str] = "datetime.date"
    _json_type_string: ClassVar[str] = "str"
    template: ClassVar[str] = "date_property.py.jinja"

    @classmethod
    def build(
        cls,
        name: str,
        required: bool,
        default: Any,
        python_name: PythonIdentifier,
    ) -> DateProperty | PropertyError:
        checked_default = cls.convert_value(default)
        if isinstance(checked_default, PropertyError):
            return checked_default

        return DateProperty(
            name=name,
            required=required,
            default=checked_default,
            python_name=python_name,
        )

    @classmethod
    def convert_value(cls, value: Any) -> Value | None | PropertyError:
        if isinstance(value, Value) or value is None:
            return value
        if isinstance(value, str):
            try:
                isoparse(value).date()  # make sure it's a valid value
            except ValueError as e:
                return PropertyError(f"Invalid date: {e}")
            return Value(python_code=f"isoparse({value!r}).date()", raw_value=value)
        return PropertyError(f"Cannot convert {value} to a date")

    def get_imports(self, *, prefix: str) -> set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names. This should be the number of . to get
            back to the root of the generated client.
        """
        imports = super().get_imports(prefix=prefix)
        imports.update({"import datetime", "from typing import cast", "from dateutil.parser import isoparse"})
        return imports
