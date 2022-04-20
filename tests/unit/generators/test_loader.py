import os

import mock
from fastapi_mvc.generators import load_generators, Generator


DATA_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(__file__),
        "../../data",
    )
)


def test_loader():
    parser = mock.Mock()
    parser.package_name = "test_app"
    parser.folder_name = "test-app"
    parser.project_root = "/path/to/project"

    generators = load_generators(DATA_DIR)
    assert sorted(generators.keys()) == sorted(["my_controller", "foobar"])
    assert issubclass(generators["my_controller"], Generator)
    assert generators["my_controller"].__name__ == "MyControllerGenerator"
    assert isinstance(
        generators["my_controller"](parser=parser),
        generators["my_controller"],
    )
    assert issubclass(generators["foobar"], Generator)
    assert generators["foobar"].__name__ == "FoobarGenerator"
    assert isinstance(
        generators["foobar"](parser=parser),
        generators["foobar"],
    )
