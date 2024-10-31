import importlib
import os
import shutil
from filecmp import cmpfiles, dircmp
from pathlib import Path
import sys
import tempfile
from typing import Any, Callable, Dict, Generator, List, Optional, Set, Tuple

from attrs import define
import pytest
from click.testing import Result
from typer.testing import CliRunner

from openapi_python_client.cli import app
from openapi_python_client.utils import snake_case


@define
class GeneratedClientContext:
    """A context manager with helpers for tests that run against generated client code.
    
    On entering this context, sys.path is changed to include the root directory of the
    generated code, so its modules can be imported. On exit, the original sys.path is
    restored, and any modules that were loaded within the context are removed.
    """

    output_path: Path
    generator_result: Result
    base_module: str
    monkeypatch: pytest.MonkeyPatch
    old_modules: Optional[Set[str]] = None

    def __enter__(self) -> "GeneratedClientContext":
        self.monkeypatch.syspath_prepend(self.output_path)
        self.old_modules = set(sys.modules.keys())
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.monkeypatch.undo()
        for module_name in set(sys.modules.keys()) - self.old_modules:
            del sys.modules[module_name]
        shutil.rmtree(self.output_path, ignore_errors=True)

    def import_module(self, module_path: str) -> Any:
        """Attempt to import a module from the generated code."""
        return importlib.import_module(f"{self.base_module}{module_path}")


def _run_command(
    command: str,
    extra_args: Optional[List[str]] = None,
    openapi_document: Optional[str] = None,
    url: Optional[str] = None,
    config_path: Optional[Path] = None,
    raise_on_error: bool = True,
) -> Result:
    """Generate a client from an OpenAPI document and return the result of the command."""
    runner = CliRunner()
    if openapi_document is not None:
        openapi_path = Path(__file__).parent / openapi_document
        source_arg = f"--path={openapi_path}"
    else:
        source_arg = f"--url={url}"
    config_path = config_path or (Path(__file__).parent / "config.yml")
    args = [command, f"--config={config_path}", source_arg]
    if extra_args:
        args.extend(extra_args)
    result = runner.invoke(app, args)
    if result.exit_code != 0 and raise_on_error:
        raise Exception(result.stdout)
    return result


def generate_client(
    openapi_document: str,
    extra_args: List[str] = [],
    output_path: str = "my-test-api-client",
    base_module: str = "my_test_api_client",
    overwrite: bool = True,
    raise_on_error: bool = True,
) -> GeneratedClientContext:
    """Run the generator and return a GeneratedClientContext for accessing the generated code."""
    full_output_path = Path.cwd() / output_path
    if not overwrite:
        shutil.rmtree(full_output_path, ignore_errors=True)
    args = [
        *extra_args,
        "--output-path",
        str(full_output_path),
    ]
    if overwrite:
        args = [*args, "--overwrite"]
    generator_result = _run_command("generate", args, openapi_document, raise_on_error=raise_on_error)
    print(generator_result.stdout)
    return GeneratedClientContext(
        full_output_path,
        generator_result,
        base_module,
        pytest.MonkeyPatch(),
    )


def generate_client_from_inline_spec(
    openapi_spec: str,
    extra_args: List[str] = [],
    filename_suffix: Optional[str] = None,
    config: str = "",
    base_module: str = "testapi_client",
    add_openapi_info = True,
    raise_on_error: bool = True,
) -> GeneratedClientContext:
    """Run the generator on a temporary file created with the specified contents.
    
    You can also optionally tell it to create a temporary config file.
    """
    if add_openapi_info and not openapi_spec.lstrip().startswith("openapi:"):
        openapi_spec += """
openapi: "3.1.0"
info:
  title: "testapi"
  description: "my test api"
  version: "0.0.1"
"""

    output_path = tempfile.mkdtemp()
    file = tempfile.NamedTemporaryFile(suffix=filename_suffix, delete=False)
    file.write(openapi_spec.encode('utf-8'))
    file.close()

    if config:
        config_file = tempfile.NamedTemporaryFile(delete=False)
        config_file.write(config.encode('utf-8'))
        config_file.close()
        extra_args = [*extra_args, "--config", config_file.name]

    generated_client = generate_client(
        file.name,
        extra_args,
        output_path,
        base_module,
        raise_on_error=raise_on_error,
    )
    os.unlink(file.name)
    if config:
        os.unlink(config_file.name)

    return generated_client


def with_generated_client_fixture(
    openapi_spec: str,
    name: str="generated_client",
    config: str="",
    extra_args: List[str] = [],
):
    """Decorator to apply to a test class to create a fixture inside it called 'generated_client'.
    
    The fixture value will be a GeneratedClientContext created by calling
    generate_client_from_inline_spec().
    """
    def _decorator(cls):
        def generated_client(self):
            with generate_client_from_inline_spec(openapi_spec, extra_args=extra_args, config=config) as g:
                yield g

        setattr(cls, name, pytest.fixture(scope="class")(generated_client))
        return cls

    return _decorator


def with_generated_code_import(import_path: str, alias: Optional[str] = None):
    """Decorator to apply to a test class to create a fixture from a generated code import.
    
    The 'generated_client' fixture must also be present.

    If import_path is "a.b.c", then the fixture's value is equal to "from a.b import c", and
    its name is "c" unless you specify a different name with the alias parameter.
    """
    parts = import_path.split(".")
    module_name = ".".join(parts[0:-1])
    import_name = parts[-1]

    def _decorator(cls):
        nonlocal alias

        def _func(self, generated_client):
            module = generated_client.import_module(module_name)
            return getattr(module, import_name)
        
        alias = alias or import_name
        _func.__name__ = alias
        setattr(cls, alias, pytest.fixture(scope="class")(_func))
        return cls
    
    return _decorator


def assert_model_decode_encode(model_class: Any, json_data: dict, expected_instance: Any):
    instance = model_class.from_dict(json_data)
    assert instance == expected_instance
    assert instance.to_dict() == json_data
