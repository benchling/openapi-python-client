from __future__ import annotations

import re
from keyword import iskeyword
from typing import Any

import stringcase


class ClassName(str):
    """A PascalCase string which has been validated / transformed into a valid class name for Python"""

    def __new__(cls, value: str, prefix: str) -> ClassName:
        new_value = fix_keywords(pascal_case(sanitize(value)))

        if not new_value.isidentifier():
            value = f"{prefix}{new_value}"
            new_value = fix_keywords(pascal_case(sanitize(value)))
        return str.__new__(cls, new_value)

    def __deepcopy__(self, _: Any) -> ClassName:
        return self


def sanitize(value: str) -> str:
    """ Removes every character that isn't 0-9, A-Z, a-z, ' ', -, or _ """
    return re.sub(r"[^\w _\-]+", "", value)


def fix_keywords(value: str) -> str:
    if iskeyword(value):
        return f"{value}_"
    return value


def group_title(value: str) -> str:
    value = re.sub(r"([A-Z]{2,})([A-Z][a-z]|[ \-_]|$)", lambda m: m.group(1).title() + m.group(2), value.strip())
    value = re.sub(r"(^|[ _-])([A-Z])", lambda m: m.group(1) + m.group(2).lower(), value)
    return value


def snake_case(value: str) -> str:
    return fix_keywords(stringcase.snakecase(group_title(sanitize(value))))


def pascal_case(value: str) -> str:
    return fix_keywords(stringcase.pascalcase(sanitize(value.replace(" ", ""))))


def kebab_case(value: str) -> str:
    return fix_keywords(stringcase.spinalcase(group_title(sanitize(value))))


def remove_string_escapes(value: str) -> str:
    return value.replace('"', r"\"")


# This can be changed by config.Config.load_config
FIELD_PREFIX = "field_"


def to_valid_python_identifier(value: str) -> str:
    """
    Given a string, attempt to coerce it into a valid Python identifier by stripping out invalid characters and, if
    necessary, prepending a prefix.

    See:
        https://docs.python.org/3/reference/lexical_analysis.html#identifiers
    """
    new_value = fix_keywords(sanitize(value))

    if new_value.isidentifier():
        return new_value

    return f"{FIELD_PREFIX}{new_value}"
