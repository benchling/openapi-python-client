from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING, ClassVar, Dict, List, Optional, Set, Union

import attr

from ... import schema as oai
from ... import utils
from ..errors import PropertyError
from ..reference import Reference
from .property import Property

if TYPE_CHECKING:
    from .schemas import Schemas


@attr.s(auto_attribs=True, frozen=True)
class ModelProperty(Property):
    """ A property which refers to another Schema """

    reference: Reference
    references: List[oai.Reference]
    required_properties: List[Property]
    optional_properties: List[Property]
    discriminator_property: Optional[str]
    discriminator_mappings: Dict[str, Property]

    description: str
    relative_imports: Set[str]
    additional_properties: Union[bool, Property]
    _json_type_string: ClassVar[str] = "Dict[str, Any]"

    template: ClassVar[str] = "model_property.pyi"
    json_is_dict: ClassVar[bool] = True

    def resolve_references(
        self, components: Dict[str, Union[oai.Reference, oai.Schema]], schemas: Schemas
    ) -> Union[Schemas, PropertyError]:
        from ..properties import property_from_data

        required_set = set()
        props = {}
        while self.references:
            reference = self.references.pop()
            source_name = Reference.from_ref(reference.ref).class_name
            referenced_prop = components[source_name]
            assert isinstance(referenced_prop, oai.Schema)
            for p, val in (referenced_prop.properties or {}).items():
                props[p] = (val, source_name)
            for sub_prop in referenced_prop.allOf or []:
                if isinstance(sub_prop, oai.Reference):
                    self.references.append(sub_prop)
                else:
                    for p, val in (sub_prop.properties or {}).items():
                        props[p] = (val, source_name)
            if isinstance(referenced_prop.required, Iterable):
                for sub_prop_name in referenced_prop.required:
                    required_set.add(sub_prop_name)

        for key, (value, source_name) in (props or {}).items():
            required = key in required_set
            prop, schemas = property_from_data(
                name=key, required=required, data=value, schemas=schemas, parent_name=source_name
            )
            if isinstance(prop, PropertyError):
                return prop
            if required:
                self.required_properties.append(prop)
                # Remove the optional version
                new_optional_props = [op for op in self.optional_properties if op.name != prop.name]
                self.optional_properties.clear()
                self.optional_properties.extend(new_optional_props)
            elif not any(ep for ep in (self.optional_properties + self.required_properties) if ep.name == prop.name):
                self.optional_properties.append(prop)
            self.relative_imports.update(prop.get_imports(prefix=".."))

        for _, value in self.discriminator_mappings.items():
            self.relative_imports.add(f"from ..models.{value.module_name} import {value.class_name}")

        return schemas

    def get_base_type_string(self) -> str:
        return self.reference.class_name

    def get_discriminator_name(self) -> str:
        """
        Returns the python_name of the discriminator value, or None if there isn't one.

        discriminator_property is the name in openapi.yaml, for example 'nucleotideType'
        This function returns its python_name, e.g. "nucleotide_type"

        Oligo:
          discriminator:
            propertyName: nucleotideType
            mapping:
              DNA: DnaOligo
              RNA: RnaOligo
        """
        if not self.discriminator_property:
            return None
        all_properties = self.optional_properties + self.required_properties
        discriminator_reference = next(filter(lambda x: x.name == self.discriminator_property, all_properties), None)
        if discriminator_reference:
            return discriminator_reference.python_name
        # self.discriminator_property is not a property of this model.
        # If so, we assume it's a property inherited from oneOf or anyOf.
        # Render it in snake_case since we cannot access it directly during template expansion.
        return utils.snake_case(self.discriminator_property)

    def get_imports(self, *, prefix: str) -> Set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names. This should be the number of . to get
            back to the root of the generated client.
        """
        imports = super().get_imports(prefix=prefix)
        imports.update(
            {
                f"from {prefix}models.{self.reference.module_name} import {self.reference.class_name}",
                "from typing import Dict",
                "from typing import cast",
            }
        )
        return imports
