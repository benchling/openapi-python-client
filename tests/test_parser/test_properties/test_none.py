from openapi_python_client.parser.errors import PropertyError
from openapi_python_client.parser.properties import NoneProperty
from openapi_python_client.parser.properties.protocol import Value
from openapi_python_client.utils import PythonIdentifier


def test_default():
    err = NoneProperty.build(
        default="not None",
        required=False,
        python_name="not_none",
        name="not_none",
    )

    assert isinstance(err, PropertyError)


def test_dont_retest_values():
    prop = NoneProperty.build(
        default=Value("not None", "not None"),
        required=False,
        python_name=PythonIdentifier("not_none", ""),
        name="not_none",
    )

    assert isinstance(prop, NoneProperty)
