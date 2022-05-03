import os

from fastapi_mvc.generators import load_generators, Generator


GENERATORS_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(__file__),
        "../../data/lib/generators",
    )
)


def test_loader():
    generators = load_generators([GENERATORS_DIR])
    assert sorted(generators.keys()) == sorted(["my_controller", "foobar"])
    assert issubclass(generators["my_controller"], Generator)
    assert generators["my_controller"].__name__ == "MyControllerGenerator"
    assert issubclass(generators["foobar"], Generator)
    assert generators["foobar"].__name__ == "FoobarGenerator"
