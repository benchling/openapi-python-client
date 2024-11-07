
from end_to_end_tests.end_to_end_test_helpers import (
    assert_model_decode_encode,
    with_generated_code_import,
    with_generated_client_fixture,
)


@with_generated_client_fixture(
"""
paths: {}
components:
  schemas:
    ThingA:
      type: object
      properties:
        propA: { type: "string" }
      required: ["propA"]
    ThingB:
      type: object
      properties:
        propB: { type: "string" }
      required: ["propB"]
    ModelWithUnion:
      type: object
      properties:
        thing:
            oneOf:
            - $ref: "#/components/schemas/ThingA"
            - $ref: "#/components/schemas/ThingB"
        thingOrString:
            oneOf:
            - $ref: "#/components/schemas/ThingA"
            - type: string
""")
@with_generated_code_import(".models.ThingA")
@with_generated_code_import(".models.ThingB")
@with_generated_code_import(".models.ModelWithUnion")
class TestOneOf:
    def test_disambiguate_objects_via_required_properties(self, ThingA, ThingB, ModelWithUnion):
        assert_model_decode_encode(
            ModelWithUnion,
            {"thing": {"propA": "x"}},
            ModelWithUnion(thing=ThingA(prop_a="x")),
        )
        assert_model_decode_encode(
            ModelWithUnion,
            {"thing": {"propB": "x"}},
            ModelWithUnion(thing=ThingB(prop_b="x")),
        )

    def test_disambiguate_object_and_non_object(self, ThingA, ModelWithUnion):
        assert_model_decode_encode(
            ModelWithUnion,
            {"thingOrString": {"propA": "x"}},
            ModelWithUnion(thing_or_string=ThingA(prop_a="x")),
        )
        assert_model_decode_encode(
            ModelWithUnion,
            {"thingOrString": "x"},
            ModelWithUnion(thing_or_string="x"),
        )


@with_generated_client_fixture(
"""
paths: {}
components:
  schemas:
    ThingA:
      type: object
      properties:
        kind: { type: "string" }
        name: { type: "string" }
    ThingB:
      type: object
      properties:
        kind: { type: "string" }
        name: { type: "string" }
    ModelWithDiscriminatorImplicitMapping:
      type: object
      properties:
        thing:
          oneOf:
            - $ref: "#/components/schemas/ThingA"
            - $ref: "#/components/schemas/ThingB"
          discriminator:
            propertyName: kind
    ModelWithDiscriminatorExplicitMapping:
      type: object
      properties:
        thing:
          oneOf:
            - $ref: "#/components/schemas/ThingA"
            - $ref: "#/components/schemas/ThingB"
          discriminator:
            propertyName: kind
            mapping:
              A: "#/components/schemas/ThingA"
              B: "ThingB"
              AlsoB: "ThingB"
    ModelWithDiscriminatorPartialMapping:
      type: object
      properties:
        thing:
          oneOf:
            - $ref: "#/components/schemas/ThingA"
            - $ref: "#/components/schemas/ThingB"
          discriminator:
            propertyName: kind
            mapping:
              A: "#/components/schemas/ThingA"
              # there's no mapping for ThingB here, so the value for it defaults to "ThingB"
""")
@with_generated_code_import(".models.ThingA")
@with_generated_code_import(".models.ThingB")
@with_generated_code_import(".models.ModelWithDiscriminatorImplicitMapping")
@with_generated_code_import(".models.ModelWithDiscriminatorExplicitMapping")
@with_generated_code_import(".models.ModelWithDiscriminatorPartialMapping")
class TestDiscriminator:
    def test_implicit_mapping(self, ThingA, ThingB, ModelWithDiscriminatorImplicitMapping):
        assert_model_decode_encode(
            ModelWithDiscriminatorImplicitMapping,
            {"thing": {"kind": "ThingA", "name": "x"}},
            ModelWithDiscriminatorImplicitMapping(thing=ThingA(kind="ThingA", name="x")),
        )
        assert_model_decode_encode(
            ModelWithDiscriminatorImplicitMapping,
            {"thing": {"kind": "ThingB", "name": "x"}},
            ModelWithDiscriminatorImplicitMapping(thing=ThingB(kind="ThingB", name="x")),
        )

    def test_explicit_mapping(self, ThingA, ThingB, ModelWithDiscriminatorExplicitMapping):
        assert_model_decode_encode(
            ModelWithDiscriminatorExplicitMapping,
            {"thing": {"kind": "A", "name": "x"}},
            ModelWithDiscriminatorExplicitMapping(thing=ThingA(kind="A", name="x")),
        )
        assert_model_decode_encode(
            ModelWithDiscriminatorExplicitMapping,
            {"thing": {"kind": "B", "name": "x"}},
            ModelWithDiscriminatorExplicitMapping(thing=ThingB(kind="B", name="x")),
        )
        assert_model_decode_encode(
            ModelWithDiscriminatorExplicitMapping,
            {"thing": {"kind": "AlsoB", "name": "x"}},
            ModelWithDiscriminatorExplicitMapping(thing=ThingB(kind="AlsoB", name="x")),
        )

    def test_partial_mapping(self, ThingA, ThingB, ModelWithDiscriminatorPartialMapping):
        assert_model_decode_encode(
            ModelWithDiscriminatorPartialMapping,
            {"thing": {"kind": "A", "name": "x"}},
            ModelWithDiscriminatorPartialMapping(thing=ThingA(kind="A", name="x")),
        )
        assert_model_decode_encode(
            ModelWithDiscriminatorPartialMapping,
            {"thing": {"kind": "ThingB", "name": "x"}},
            ModelWithDiscriminatorPartialMapping(thing=ThingB(kind="ThingB", name="x")),
        )
