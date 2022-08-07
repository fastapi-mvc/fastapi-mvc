"""Application implementation - error response."""
from typing import Dict, Any, Optional, List
from http import HTTPStatus

from pydantic import BaseModel, root_validator


class ErrorModel(BaseModel):
    """Define base error model for the response.

    Attributes:
        code (int): HTTP error status code.
        message (str): Detail on HTTP error.
        status (str): HTTP error reason-phrase as per in RFC7235. NOTE! Set
            automatically based on HTTP error status code.

    Raises:
        pydantic.error_wrappers.ValidationError: If any of provided attribute
            doesn't pass type validation.

    """

    code: int
    message: str
    details: Optional[List[Dict[str, Any]]]

    @root_validator(pre=False, skip_on_failure=True)
    def _set_status(cls, values: dict) -> dict:
        """Set the status field value based on the code attribute value.

        Args:
            values(dict): Stores the attributes of the ErrorModel object.

        Returns:
            dict: The attributes of the ErrorModel object with the status field.

        """
        values["status"] = HTTPStatus(values["code"]).name
        return values

    class Config:
        """Config sub-class needed to extend/override the generated JSON schema.

        More details can be found in pydantic documentation:
        https://pydantic-docs.helpmanual.io/usage/schema/#schema-customization

        """

        @staticmethod
        def schema_extra(schema: Dict[str, Any]) -> None:
            """Post-process the generated schema.

            Method can have one or two positional arguments. The first will be
            the schema dictionary. The second, if accepted, will be the model
            class. The callable is expected to mutate the schema dictionary
            in-place; the return value is not used.

            Args:
                schema (typing.Dict[str, typing.Any]): The schema dictionary.

            """
            # Override schema description, by default is taken from docstring.
            schema["description"] = "Error model."
            # Add status to schema properties.
            schema["properties"].update(
                {"status": {"title": "Status", "type": "string"}}
            )
            schema["required"].append("status")


class ErrorResponse(BaseModel):
    """Define error response model.

    Attributes:
        error (ErrorModel): ErrorModel class object instance.

    Raises:
        pydantic.error_wrappers.ValidationError: If any of provided attribute
            doesn't pass type validation.

    """

    error: ErrorModel

    def __init__(self, **kwargs):
        """Initialize ErrorResponse class object instance."""
        # Neat trick to still use kwargs on ErrorResponse model.
        super().__init__(error=ErrorModel(**kwargs))

    class Config:
        """Config sub-class needed to extend/override the generated JSON schema.

        More details can be found in pydantic documentation:
        https://pydantic-docs.helpmanual.io/usage/schema/#schema-customization

        """

        @staticmethod
        def schema_extra(schema: Dict[str, Any]) -> None:
            """Post-process the generated schema.

            Method can have one or two positional arguments. The first will be
            the schema dictionary. The second, if accepted, will be the model
            class. The callable is expected to mutate the schema dictionary
            in-place; the return value is not used.

            Args:
                schema (typing.Dict[str, typing.Any]): The schema dictionary.

            """
            # Override schema description, by default is taken from docstring.
            schema["description"] = "Error response model."
