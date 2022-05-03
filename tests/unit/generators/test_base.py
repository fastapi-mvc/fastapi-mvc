from logging import Logger

import mock
import pytest
from click import Argument, Option
from fastapi_mvc.generators import Generator


@mock.patch.multiple(
    "fastapi_mvc.generators.base.Generator",
    __abstractmethods__=set()
)
def test_base_generator():
    assert Generator.name == NotImplemented
    assert Generator.template == NotImplemented
    assert not Generator.usage
    assert Generator.category == "Other"

    assert len(Generator.cli_arguments) == 1
    assert isinstance(Generator.cli_arguments[0], Argument)
    assert Generator.cli_arguments[0].opts == ["NAME"]
    assert Generator.cli_arguments[0].required
    assert Generator.cli_arguments[0].nargs == 1

    assert len(Generator.cli_options) == 1
    assert isinstance(Generator.cli_options[0], Option)
    assert Generator.cli_options[0].opts == ["-S", "--skip"]
    assert Generator.cli_options[0].help == "Skip files that already exist."
    assert Generator.cli_options[0].is_flag

    assert not Generator.cli_help
    assert not Generator.cli_short_help
    assert not Generator.cli_deprecated

    generator = Generator()
    generator.new()
    generator.destroy()

    assert isinstance(generator, Generator)
    assert not hasattr(generator, "__dict__")
    assert hasattr(generator, "__slots__")
    assert generator.__slots__ == ("_log",)

    assert isinstance(generator._log, Logger)


def test_init_subclass():
    with pytest.raises(NotImplementedError):
        type('SubClass', (Generator,), {})

    obj = type('SubClass', (Generator,), {"template": "/some/path"})
    obj.name = "SubClass"
