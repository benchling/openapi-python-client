import pytest
from end_to_end_tests.end_to_end_test_helpers import (
    assert_bad_schema_warning,
    inline_spec_should_cause_warnings,
)


class TestUnionInvalidSchemas:
    @pytest.fixture(scope="class")
    def warnings(self):
        return inline_spec_should_cause_warnings(
"""
components:
  schemas:
    ModelType1:
      type: object
      properties:
        modelType: {"type": "string"}
        name: {"type": "string"}
      required: ["modelType"]
    ModelType2:
      type: object
      properties:
        modelType: {"type": "string"}
        name: {"type": "string"}
      required: ["modelType"]
    UnionWithInvalidReference:
      anyOf:
        - $ref: "#/components/schemas/DoesntExist"
    UnionWithInvalidDefault:
      type: ["number", "integer"]
      default: aaa
"""
        )

    def test_invalid_reference(self, warnings):
        assert_bad_schema_warning(warnings, "UnionWithInvalidReference", "Could not find reference")

    def test_invalid_default(self, warnings):
        assert_bad_schema_warning(warnings, "UnionWithInvalidDefault", "Invalid int value: aaa")


class TestInvalidDiscriminators:
    @pytest.fixture(scope="class")
    def warnings(self):
        return inline_spec_should_cause_warnings(
"""
components:
  schemas:
    ModelType1:
      type: object
      properties:
        modelType: {"type": "string"}
        name: {"type": "string"}
      required: ["modelType"]
    ModelType2:
      type: object
      properties:
        modelType: {"type": "string"}
        name: {"type": "string"}
      required: ["modelType"]
    ModelType3:
      type: object
      properties:
        modelType: {"type": "string"}
        name: {"type": "string"}
      required: ["modelType"]
    StringType:
      type: string
    WithUnknownSchemaInMapping:
      type: object
      properties:
        unionProp:
          oneOf:
            - $ref: "#/components/schemas/ModelType1"
            - $ref: "#/components/schemas/ModelType2"
          discriminator:
            propertyName: modelType
            mapping:
              "type1": "#/components/schemas/ModelType1"
              "type2": "#/components/schemas/DoesntExist"
    WithReferenceToSchemaNotInUnion:
      type: object
      properties:
        unionProp:
          oneOf:
            - $ref: "#/components/schemas/ModelType1"
            - $ref: "#/components/schemas/ModelType2"
          discriminator:
            propertyName: modelType
            mapping:
              "type1": "#/components/schemas/ModelType1"
              "type2": "#/components/schemas/ModelType2"
              "type3": "#/components/schemas/ModelType3"
    WithNonObjectVariant:
      type: object
      properties:
        unionProp:
          oneOf:
            - $ref: "#/components/schemas/ModelType1"
            - $ref: "#/components/schemas/StringType"
          discriminator:
            propertyName: modelType
    WithInlineSchema:
      type: object
      properties:
        unionProp:
          oneOf:
            - $ref: "#/components/schemas/ModelType1"
            - type: object
              properties:
                modelType: {"type": "string"}
                name: {"type": "string"}
          discriminator:
            propertyName: modelType
      
"""
        )
    
    def test_invalid_reference(self, warnings):
        assert_bad_schema_warning(
            warnings,
            "WithUnknownSchemaInMapping",
            'Invalid reference "#/components/schemas/DoesntExist" in discriminator mapping',
        )

    def test_reference_to_schema_not_in_union(self, warnings):
        assert_bad_schema_warning(
            warnings,
            "WithReferenceToSchemaNotInUnion",
            'Discriminator mapping referred to "ModelType3" which is not one of the schema variants',
        )

    def test_non_object_variant(self, warnings):
        assert_bad_schema_warning(
            warnings,
            "WithNonObjectVariant",
            "All schema variants must be objects when using a discriminator",
        )

    def test_inline_schema(self, warnings):
        assert_bad_schema_warning(
            warnings,
            "WithInlineSchema",
            "Inline schema declarations are not allowed when using a discriminator",
        )
