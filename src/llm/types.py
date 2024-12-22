# -------------------------------------------------------------------------------- #
# AI Types
# -------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #


# Pydantic imports
from pydantic import BaseModel, Field


# -------------------------------------------------------------------------------- #
# AI Model Response Types
# -------------------------------------------------------------------------------- #

# TODO: Use this when o1 adds support for structured outputs
# class ContentResponse(BaseModel):
#     """Response model for the MDX content generation process."""
#     content: str = Field(description="The content of the content")


class TitleExcerptResponse(BaseModel):
    """Response model for the title and excerpt generation process."""
    title: str = Field(description="The title of the content")
    excerpt: str = Field(description="The excerpt of the content")
