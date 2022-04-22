"""fastapi-mvc."""
from fastapi_mvc.generators.base import Generator
from fastapi_mvc.generators.project import ProjectGenerator
from fastapi_mvc.generators.controller import ControllerGenerator
from fastapi_mvc.generators.generator import GeneratorGenerator
from fastapi_mvc.generators.loader import load_generators


builtins = {
    ControllerGenerator.name: ControllerGenerator,
    GeneratorGenerator.name: GeneratorGenerator,
}


__all__ = (
    Generator,
    ProjectGenerator,
    ControllerGenerator,
    GeneratorGenerator,
    load_generators,
)
