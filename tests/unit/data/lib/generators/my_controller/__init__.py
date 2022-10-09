"""Custom generator for fastapi-mvc."""
from .my_controller import my_controller

# NOTE! Do not edit this! Method for programmatically loading user generators
# depends on having only one fastapi_mvc.Generator in module `generator` attribute.
generator = my_controller
