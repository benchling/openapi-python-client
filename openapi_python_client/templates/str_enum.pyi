from ..extensions import Enums
from enum import Enum
from functools import lru_cache
from typing import cast

class {{ enum.reference.class_name }}(Enums.KnownString):
    {% for key, value in enum.values.items() %}
    {{ key }} = "{{ value }}"
    {% endfor %}

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "{{ enum.reference.class_name }}":
        if not isinstance(val, str):
            raise ValueError(f"Value of {{ enum.reference.class_name }} must be a string ({val})")
        newcls = Enum("{{ enum.reference.class_name }}", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast({{ enum.reference.class_name }}, getattr(newcls, "_UNKNOWN"))

