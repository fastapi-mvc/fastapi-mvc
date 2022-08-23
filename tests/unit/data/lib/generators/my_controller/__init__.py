"""Custom generator for fastapi-mvc."""
from .my_controller import MyControllerGenerator

# NOTE! Do not edit this! Method for programmatically loading user generators
# depends on having only one class in module `generator_class` attribute.
generator_class = MyControllerGenerator
