# -*- coding: utf-8 -*-
from setuptools import setup

packages = [
    "openapi_python_client",
    "openapi_python_client.parser",
    "openapi_python_client.parser.properties",
    "openapi_python_client.schema",
    "openapi_python_client.templates",
]

package_data = {"": ["*"], "openapi_python_client.templates": ["property_templates/*"]}

install_requires = [
    "attrs>=20.1.0,<22.0",
    "autoflake>=1.4,<2.0",
    "black>=20.8b1",
    "httpx>=0.23.0",
    "isort>=5.0.5,<6.0.0",
    "jinja2>=3.1.0,<4.0.0",
    "pydantic>=1.6.1,<2.0.0",
    "python-dateutil>=2.8.1,<3.0.0",
    "pyyaml>=5.3.1,<6.0.0",
    "shellingham>=1.3.2,<2.0.0",
    "stringcase>=1.2.0,<2.0.0",
    "typer>=0.3,<0.4",
]

extras_require = {
    ':python_version < "3.8"': ["importlib_metadata>=4.4"],
    ':sys_platform == "win32"': ["colorama>=0.4.3,<0.5.0"],
}

entry_points = {"console_scripts": ["openapi-python-client = openapi_python_client.cli:app"]}

setup_kwargs = {
    "name": "openapi-python-client",
    "version": "1.0.1",
    "description": "Generate modern Python clients from OpenAPI",
    "long_description": '[![triaxtec](https://circleci.com/gh/triaxtec/openapi-python-client.svg?style=svg)](https://circleci.com/gh/triaxtec/openapi-python-client)\n[![codecov](https://codecov.io/gh/triaxtec/openapi-python-client/branch/main/graph/badge.svg)](https://codecov.io/gh/triaxtec/openapi-python-client)\n[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)\n[![Generic badge](https://img.shields.io/badge/type_checked-mypy-informational.svg)](https://mypy.readthedocs.io/en/stable/introduction.html)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![PyPI version shields.io](https://img.shields.io/pypi/v/openapi-python-client.svg)](https://pypi.python.org/pypi/openapi-python-client/)\n[![Downloads](https://static.pepy.tech/personalized-badge/openapi-python-client?period=total&units=international_system&left_color=blue&right_color=green&left_text=Downloads)](https://pepy.tech/project/openapi-python-client)\n\n# openapi-python-client\n\nGenerate modern Python clients from OpenAPI 3.x documents.\n\n_This generator does not support OpenAPI 2.x FKA Swagger. If you need to use an older document, try upgrading it to\nversion 3 first with one of many available converters._\n\n**This project is still in development and does not support all OpenAPI features**\n\n## Why This?\n\nThe Python clients generated by openapi-generator support Python 2 and therefore come with a lot of baggage. This tool\naims to generate clients which:\n\n1. Use all the latest and greatest Python features like type annotations and dataclasses\n1. Don\'t carry around a bunch of compatibility code for older version of Python (e.g. the `six` package)\n1. Have better documentation and more obvious usage instructions\n\nAdditionally, because this generator is written in Python, it should be more accessible to contribution by the people\nusing it (Python developers).\n\n## Installation\n\nI recommend you install with [pipx](https://pipxproject.github.io/pipx/) so you don\'t conflict with any other packages\nyou might have: `pipx install openapi-python-client`.\n\nBetter yet, use `pipx run openapi-python-client <normal params / options>` to always use the latest version of the generator.\n\nYou can install with normal pip if you want to though: `pip install openapi-python-client`\n\nThen, if you want tab completion: `openapi-python-client --install-completion`\n\n## Usage\n\n### Create a new client\n\n`openapi-python-client generate --url https://my.api.com/openapi.json`\n\nThis will generate a new client library named based on the title in your OpenAPI spec. For example, if the title\nof your API is "My API", the expected output will be "my-api-client". If a folder already exists by that name, you\'ll\nget an error.\n\n### Update an existing client\n\n`openapi-python-client update --url https://my.api.com/openapi.json`\n\n> For more usage details run `openapi-python-client --help` or read [usage](usage.md)\n\n### Using custom templates\n\nThis feature leverages Jinja2\'s [ChoiceLoader](https://jinja.palletsprojects.com/en/2.11.x/api/#jinja2.ChoiceLoader) and [FileSystemLoader](https://jinja.palletsprojects.com/en/2.11.x/api/#jinja2.FileSystemLoader). This means you do _not_ need to customize every template. Simply copy the template(s) you want to customize from [the default template directory](openapi_python_client/templates) to your own custom template directory (file names _must_ match exactly) and pass the template directory through the `custom-template-path` flag to the `generate` and `update` commands. For instance,\n\n```\nopenapi-python-client update \\\n  --url https://my.api.com/openapi.json \\\n  --custom-template-path=relative/path/to/mytemplates\n```\n\n_Be forewarned, this is a beta-level feature in the sense that the API exposed in the templates is undocumented and unstable._\n\n## What You Get\n\n1. A `pyproject.toml` file with some basic metadata intended to be used with [Poetry].\n1. A `README.md` you\'ll most definitely need to update with your project\'s details\n1. A Python module named just like the auto-generated project name (e.g. "my_api_client") which contains:\n   1. A `client` module which will have both a `Client` class and an `AuthenticatedClient` class. You\'ll need these\n      for calling the functions in the `api` module.\n   1. An `api` module which will contain one module for each tag in your OpenAPI spec, as well as a `default` module\n      for endpoints without a tag. Each of these modules in turn contains one function for calling each endpoint.\n   1. A `models` module which has all the classes defined by the various schemas in your OpenAPI spec\n\nFor a full example you can look at the `end_to_end_tests` directory which has an `openapi.json` file.\n"golden-record" in that same directory is the generated client from that OpenAPI document.\n\n## OpenAPI features supported\n\n1. All HTTP Methods\n1. JSON and form bodies, path and query parameters\n1. File uploads with multipart/form-data bodies\n1. float, string, int, date, datetime, string enums, and custom schemas or lists containing any of those\n1. html/text or application/json responses containing any of the previous types\n1. Bearer token security\n\n## Configuration\n\nYou can pass a YAML (or JSON) file to openapi-python-client with the `--config` option in order to change some behavior.\nThe following parameters are supported:\n\n### class_overrides\n\nUsed to change the name of generated model classes. This param should be a mapping of existing class name\n(usually a key in the "schemas" section of your OpenAPI document) to class_name and module_name. As an example, if the\nname of the a model in OpenAPI (and therefore the generated class name) was something like "\\_PrivateInternalLongName"\nand you want the generated client\'s model to be called "ShortName" in a module called "short_name" you could do this:\n\nExample:\n\n```yaml\nclass_overrides:\n  _PrivateInternalLongName:\n    class_name: ShortName\n    module_name: short_name\n```\n\nThe easiest way to find what needs to be overridden is probably to generate your client and go look at everything in the\nmodels folder.\n\n### project_name_override and package_name_override\n\nUsed to change the name of generated client library project/package. If the project name is changed but an override for the package name\nisn\'t provided, the package name will be converted from the project name using the standard convention (replacing `-`\'s with `_`\'s).\n\nExample:\n\n```yaml\nproject_name_override: my-special-project-name\npackage_name_override: my_extra_special_package_name\n```\n\n### field_prefix\n\nWhen generating properties, the `name` attribute of the OpenAPI schema will be used. When the `name` is not a valid\nPython identifier (e.g. begins with a number) this string will be prepended. Defaults to "field\\_".\n\nExample:\n\n```yaml\nfield_prefix: attr_\n```\n\n### package_version_override\n\nSpecify the package version of the generated client. If unset, the client will use the version of the OpenAPI spec.\n\nExample:\n\n```yaml\npackage_version_override: 1.2.3\n```\n\n## How to publish changes\nQuip doc that highlights how to pull the dependency to Aurelia and publish using a buildkite pipeline can be found [here](https://benchling.quip.com/PgytA283Rlyo/2022-02-16-Guide-for-Publishing-a-Package)\n\nAfter changes are made to this package, to publish a new version of this package:\n* Bump the version on pyproject.toml\n* Install `gnu-sed` (assuming that you\'re running on a mac) by running `brew install gnu-sed`\n  * macOS uses BSD sed, which is similar to Linux\'s GNU sed but cannot explicitly edit files in place i.e. cannot utilize `-i` tag\n* Set GNU sed PATH by running `brew info gnu-sed` to check for PATH\n* Run `poetry run task gen-setuppy` which updates setup.py\n* Kick off a buildkite pipeline build as highlighted in the quip doc (would need to designate the branch of which to check for publish)\n\n\n[changelog.md]: CHANGELOG.md\n[poetry]: https://python-poetry.org/\n',
    "author": "Dylan Anthony",
    "author_email": "danthony@triaxtec.com",
    "maintainer": None,
    "maintainer_email": None,
    "url": "https://github.com/triaxtec/openapi-python-client",
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "extras_require": extras_require,
    "entry_points": entry_points,
    "python_requires": ">=3.7,<4.0",
}


setup(**setup_kwargs)
