from ..extensions import Enums
from enum import IntEnum

class {{ enum.reference.class_name }}(Enums.KnownInt):
    {% for key, value in enum.values.items() %}
    {{ key }} = {{ value }}
    {% endfor %}

    def __str__(self) -> str:
        return str(self.value)
