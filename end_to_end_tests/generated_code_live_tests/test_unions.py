import pytest

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

    def test_decode_fails_if_property_not_found(self, ModelWithDiscriminatorExplicitMapping):
        with pytest.raises(TypeError):
            ModelWithDiscriminatorExplicitMapping.from_dict({"thing": {"name": "x"}})

    def test_decode_fails_if_property_has_unrecognized_value(self, ModelWithDiscriminatorExplicitMapping):
        with pytest.raises(TypeError):
            ModelWithDiscriminatorExplicitMapping.from_dict({"thing": {"kind": "C", "name": "x"}})


@with_generated_client_fixture(
"""
paths: {}
components:
  schemas:
    Corgi:
      type: object
      properties:
        dogType: { type: "string" }
        name: { type: "string" }
    Schnauzer:
      type: object
      properties:
        dogType: { type: "string" }
        name: { type: "string" }
    Dog:
      oneOf:
        - $ref: "#/components/schemas/Corgi"
        - $ref: "#/components/schemas/Schnauzer"
      discriminator:
        propertyName: dogType
    Condor:
      type: object
      properties:
        birdType: { type: "string" }
        name: { type: "string" }
    Emu:
      type: object
      properties:
        birdType: { type: "string" }
        name: { type: "string" }
    Quail:
      type: object
      properties:
        birdType: { type: "string" }
        name: { type: "string" }
    Sparrow:
      type: object
      properties:
        birdType: { type: "string" }
        name: { type: "string" }
    BigBird:
      oneOf:
        - $ref: "#/components/schemas/Condor"
        - $ref: "#/components/schemas/Emu"
      discriminator:
        propertyName: birdType
    LittleBird:
      oneOf:
        - $ref: "#/components/schemas/Quail"
        - $ref: "#/components/schemas/Sparrow"
      discriminator:
        propertyName: birdType
    Bird:
      oneOf:
        - $ref: "#/components/schemas/BigBird"
        - $ref: "#/components/schemas/LittleBird"
    ModelWithDogOrBird:
      type: object
      properties:
        dogOrBird:
          oneOf:
            - $ref: "#/components/schemas/Dog"
            - $ref: "#/components/schemas/Bird"
""")
@with_generated_code_import(".models.Corgi")
@with_generated_code_import(".models.Schnauzer")
@with_generated_code_import(".models.Condor")
@with_generated_code_import(".models.Emu")
@with_generated_code_import(".models.Quail")
@with_generated_code_import(".models.Sparrow")
@with_generated_code_import(".models.ModelWithDogOrBird")
class TestDiscriminatorInNestedUnion:
    def test_different_discriminator_properties(self, Schnauzer, Sparrow, ModelWithDogOrBird):
        assert_model_decode_encode(
            ModelWithDogOrBird,
            {"dogOrBird": {"dogType": "Schnauzer", "name": "Fido"}},
            ModelWithDogOrBird(dog_or_bird=Schnauzer(dog_type="Schnauzer", name="Fido")),
        )
        assert_model_decode_encode(
            ModelWithDogOrBird,
            {"dogOrBird": {"birdType": "Sparrow", "name": "Fido"}},
            ModelWithDogOrBird(dog_or_bird=Sparrow(bird_type="Sparrow", name="Fido")),
        )

    def test_same_discriminator_property_in_different_unions(self, Emu, Sparrow, ModelWithDogOrBird):
        assert_model_decode_encode(
            ModelWithDogOrBird,
            {"dogOrBird": {"birdType": "Emu", "name": "Fido"}},
            ModelWithDogOrBird(dog_or_bird=Emu(bird_type="Emu", name="Fido")),
        )
        assert_model_decode_encode(
            ModelWithDogOrBird,
            {"dogOrBird": {"birdType": "Sparrow", "name": "Fido"}},
            ModelWithDogOrBird(dog_or_bird=Sparrow(bird_type="Sparrow", name="Fido")),
        )
        assert_model_decode_encode(
            ModelWithDogOrBird,
            {"dogOrBird": {"birdType": "Sparrow", "name": "Fido"}},
            ModelWithDogOrBird(dog_or_bird=Sparrow(bird_type="Sparrow", name="Fido")),
        )
