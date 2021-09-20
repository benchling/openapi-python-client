from functools import lru_cache

from ..extensions import Enums
from enum import Enum, IntEnum
from functools import lru_cache
from typing import cast

class {{ enum.reference.class_name }}(Enums.KnownInt):
    {% for key, value in enum.values.items() %}
    {{ key }} = {{ value }}
    {% endfor %}

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: int) -> "{{ enum.reference.class_name }}":
        if not isinstance(val, int):
            raise ValueError(f"Value of {{ enum.reference.class_name }} must be an int ({val})")
        newcls = Enum("{{ enum.reference.class_name }}", {"_UNKNOWN": val}, type=Enums.UnknownInt)  # type: ignore
        return cast({{ enum.reference.class_name }}, getattr(newcls, "_UNKNOWN"))

