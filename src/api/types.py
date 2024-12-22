# -------------------------------------------------------------------------------- #
# API Types
# -------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Type imports
from typing import List, Optional, Dict, Any
import json

# Pydantic imports
from pydantic import BaseModel, Field


# -------------------------------------------------------------------------------- #
# API Request Types
# -------------------------------------------------------------------------------- #


class HandlerApiRequest(BaseModel):
    """Request model for the handler API."""
    content: str = Field(description="The raw content to be processed into draft content")
    category_id: str = Field(description="The ID of the category which represents the type of the content for the brand.")
    category_slug: str = Field(description="The slug of the category which represents the type of the content for the brand.")
    brand_id: str = Field(description="The ID of the brand which the content belongs to.")


# -------------------------------------------------------------------------------- #
# API Response Types
# -------------------------------------------------------------------------------- #


class BaseApiBody(BaseModel):
    """
    Base model for the API body. Includes status, message, and data.
    """
    status: str = Field(description="The status of the response", default="success")
    message: str = Field(description="The message of the response", default="The request was successful")
    data: Optional[Dict[str, Any]] = Field(description="The response from the AI models", default=None)


# -------------------------------------------------------------------------------- #

class LambdaApiResponse(BaseModel):
    """
    Response model for the Lambda HTTP handler.
    """
    statusCode: int = Field(description="The status code of the response", default=200)
    headers: Dict[str, str] = Field(description="The headers of the response", default={"Content-Type": "application/json"})
    body: BaseApiBody = Field(description="The body of the response. Includes status, message, and data.", default=BaseApiBody())
