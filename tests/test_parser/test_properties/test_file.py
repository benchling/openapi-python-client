from openapi_python_client.parser.errors import PropertyError
from openapi_python_client.parser.properties import FileProperty


def test_no_default_allowed():
    err = FileProperty.build(
        default="not none",
        required=False,
        python_name="not_none",
        name="not_none",
    )

    assert isinstance(err, PropertyError)
