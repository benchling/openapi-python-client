from typing import ClassVar, Optional, Set

import attr

from ... import utils


@attr.s(auto_attribs=True, frozen=True)
class Property:
    """
    Describes a single property for a schema

    Attributes:
        template: Name of the template file (if any) to use for this property. Must be stored in
            templates/property_templates and must contain two macros: construct and transform. Construct will be used to
            build this property from JSON data (a response from an API). Transform will be used to convert this property
            to JSON data (when sending a request to the API).

    Raises:
        ValidationError: Raised when the default value fails to be converted to the expected type
    """

    name: str
    required: bool
    nullable: bool
    _type_string: ClassVar[str] = ""
    _json_type_string: ClassVar[str] = ""  # Type of the property after JSON serialization
    default: Optional[str] = attr.ib()
    python_name: str = attr.ib(init=False)
    description: Optional[str]

    template: ClassVar[Optional[str]] = None
    json_is_dict: ClassVar[bool] = False

    def __attrs_post_init__(self) -> None:
        object.__setattr__(self, "python_name", utils.to_valid_python_identifier(utils.snake_case(self.name)))

    def get_base_type_string(self) -> str:
        return self._type_string

    def get_type_string(self, no_optional: bool = False, query_parameter: bool = False, json: bool = False) -> str:
        """
        Get a string representation of type that should be used when declaring this property

        Args:
            no_optional: Do not include Optional or Unset even if the value is optional (needed for isinstance checks)
            query_parameter: True if the property's type is being used for a query parameter
            json: True if the type refers to the property after JSON serialization
        """
        if json:
            type_string = self._json_type_string
        else:
            type_string = self.get_base_type_string()

        if no_optional:
            return type_string
        if self.required:
            if self.nullable:
                return f"Optional[{type_string}]"
            else:
                return type_string
        else:
            if self.nullable:
                return f"Union[Unset, None, {type_string}]"
            else:
                return f"Union[Unset, {type_string}]"

    def get_instance_type_string(self) -> str:
        """Get a string representation of runtime type that should be used for `isinstance` checks"""
        return self.get_type_string(no_optional=True)

    # noinspection PyUnusedLocal
    def get_imports(self, *, prefix: str) -> Set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names. This should be the number of . to get
            back to the root of the generated client.
        """
        imports = set()
        if self.nullable:
            imports.add("from typing import Optional")
        if not self.required:
            imports.add("from typing import Union")
            imports.add(f"from {prefix}types import UNSET, Unset")
        return imports

    def to_string(self, query_parameter: bool = False) -> str:
        """
        How this should be declared in a dataclass

        Args:
            query_parameter: True if the property's type is being used for a query parameter
        """
        default: Optional[str]
        if self.default is not None:
            default = self.default
        elif not self.required:
            default = "UNSET"
        else:
            default = None

        if default is not None:
            return f"{self.python_name}: {self.get_type_string(query_parameter=query_parameter)} = {default}"
        else:
            return f"{self.python_name}: {self.get_type_string(query_parameter=query_parameter)}"
