from ..extensions import Enums
from enum import Enum

class {{ enum.reference.class_name }}(Enums.KnownString):
    {% for key, value in enum.values.items() %}
    {{ key }} = "{{ value }}"
    {% endfor %}

    def __str__(self) -> str:
        return str(self.value)
