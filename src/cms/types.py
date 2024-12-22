# -------------------------------------------------------------------------------- #
# CMS Types
# -------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Type imports
from typing import Optional, List
import os

# Environment imports
from dotenv import load_dotenv

# Pydantic imports
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()


# -------------------------------------------------------------------------------- #
# CMS Create Article Request
# -------------------------------------------------------------------------------- #


class CmsCreateArticleRequest(BaseModel):
    """
    Request model for making requests to 'Articles' in the CMS API.
    """
    title: str = Field(description="The title of the content")
    excerpt: str = Field(description="The excerpt of the content")
    content: str = Field(description="The content of the content")
    brandId: str = Field(description="The ID of the brand which the content belongs to.")
    tagIds: List[str] = Field(description="The IDs of the tags which the content belongs to.")
    # TODO: Make this default for now...edit later
    authorId: Optional[str] = Field(description="The ID of the author which the content belongs to.", default=os.getenv("CMS_AUTHOR_ID"))

# -------------------------------------------------------------------------------- #
# CMS Resource Base Response
# -------------------------------------------------------------------------------- #

class CmsResourceBaseResponse(BaseModel):
    """
    Response model for making requests to 'Xml Blocks' in the CMS API.
    """
    docs: List[BaseModel] = Field(..., description="The list of documents.")
    totalDocs: int = Field(..., description="Total number of documents")
    limit: int = Field(..., description="Number of documents per page")
    totalPages: int = Field(..., description="Total number of pages")
    page: int = Field(..., description="Current page number")
    pagingCounter: int = Field(..., description="Counter for pagination")
    hasPrevPage: bool = Field(..., description="Indicates if there is a previous page")
    hasNextPage: bool = Field(..., description="Indicates if there is a next page")
    prevPage: Optional[int] = Field(None, description="Previous page number")
    nextPage: Optional[int] = Field(None, description="Next page number")

# -------------------------------------------------------------------------------- #
# XML Blocks Models
# -------------------------------------------------------------------------------- #
# TODO: Simplify this

class CmsXmlBlockParameter(BaseModel):
    """
    Model for XML block parameters in the CMS API.
    """
    id: str = Field(..., description="The ID of the parameter")
    name: str = Field(..., description="The name of the parameter") 
    ts_name: str = Field(..., description="The TypeScript name of the parameter")
    required: bool = Field(..., description="Whether the parameter is required")
    description: Optional[str] = Field(description="The description of the parameter", default="")
    data_type: str = Field(..., description="The data type of the parameter")

class CmsXmlBlock(BaseModel):
    """
    Model for XML blocks in the CMS API.
    """
    id: str = Field(..., description="The ID of the XML block")
    name: str = Field(..., description="The name of the XML block")
    ts_name: str = Field(..., description="The TypeScript name of the XML block")
    description: str = Field(..., description="The description of the XML block")
    parameters: List[CmsXmlBlockParameter] = Field(..., description="The parameters of the XML block")

