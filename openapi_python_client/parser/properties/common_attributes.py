from __future__ import annotations

from attrs import define

from openapi_python_client import schema as oai


@define(frozen=True)
class CommonAttributes:
    """Attributes that are copied directly from the schema and do not vary by property type."""

    description: str | None = None
    example: str | None = None
    read_only: bool = False

    @classmethod
    def from_data(cls, data: oai.Schema) -> CommonAttributes:
        return CommonAttributes(
            description=data.description,
            example=data.example,
            read_only=data.readOnly is not None and data.readOnly,
        )

    def override_with(self, other: CommonAttributes) -> CommonAttributes:
        return CommonAttributes(
            description=other.description or self.description,
            example=other.example or self.example,
            read_only=other.read_only or self.read_only,
        )


DEFAULT_COMMON = CommonAttributes()
