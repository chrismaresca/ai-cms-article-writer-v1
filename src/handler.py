# -------------------------------------------------------------------------------- #
# Handler
# -------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Built-in imports
from typing import Dict, Any, Tuple
from dotenv import load_dotenv
import json

# Async imports
import asyncio

# Requests Imports
import requests

# Pydantic Imports
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

# Logger
from src.utils.logger import logger

# Type Imports
from src.api.types import HandlerApiRequest, LambdaApiResponse, BaseApiBody

# Handler Utils Imports
from src.utils.handler_utils import parse_request_body, validate_request_body

# CMS Imports
from src.cms.calls import fetch_xml_blocks, create_article_in_cms
from src.cms.types import CmsCreateArticleRequest

# LLM Imports
from src.llm.calls import call_content_generation_agent, call_title_and_excerpt_generation_agent

# -------------------------------------------------------------------------------- #
# Configuration
# -------------------------------------------------------------------------------- #


# Load environment variables
load_dotenv()
logger.info("Loaded environment variables")


# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #


async def write_long_form_article_async(event: Dict[str, Any], context: Dict[str, Any]) -> LambdaApiResponse:
    logger.info(f"Received event: {event}")

    try:
        # Step One: Parse the request body
        parsed_request = parse_request_body(event=event, request_model=HandlerApiRequest)

        # Step Two: Validate the request body
        validate_request_body(body=parsed_request, request_model=HandlerApiRequest)

        # Step Three: Extract Body into  HandlerApiRequest
        handler_api_request = HandlerApiRequest(**parsed_request)

        # Step Four: Fetch the XML blocks from the CMS
        xml_blocks = await fetch_xml_blocks(brand_id=handler_api_request.brand_id)

        # Step Five: Configure the content generation kwargs
        content_generation_kwargs = {
            "raw_content": handler_api_request.content,
            "xml_blocks": xml_blocks,
        }

        # Step Six: Configure and run the agent
        content = await call_content_generation_agent(developer_prompt_kwargs=content_generation_kwargs)

        # Step Seven: Call the title and excerpt generation agent
        title_and_excerpt = await call_title_and_excerpt_generation_agent(content=content)

        # Step Eight: Prepare Body
        cms_create_article_request = CmsCreateArticleRequest(
            title=title_and_excerpt.title,
            excerpt=title_and_excerpt.excerpt,
            content=content,
            brandId=handler_api_request.brand_id,
            tagIds=[handler_api_request.category_id],
        )

        # Step Nine: Create the article in the CMS
        cms_create_article_response = await create_article_in_cms(cms_create_article_request)

        # Step Ten: Prepare the response
        body = BaseApiBody(
            status="success",
            message="Article created in CMS.",
            data={"article_id": cms_create_article_response},
        )

        # Prepare the response
        handler_response = LambdaApiResponse(
            body=body
        )

        return handler_response

    except ValueError as e:
        logger.error(f"Error occurred: {e}")

        # Prepare the response
        body = BaseApiBody(
            status="error",
            message=str(e),
            data=None,
        )

        # Prepare the response
        handler_response = LambdaApiResponse(
            status_code=400,
            body=body,
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

        # Prepare the response
        body = BaseApiBody(
            status="error",
            message=str(e),
            data=None,
        )

        # Prepare the response
        handler_response = LambdaApiResponse(
            status_code=500,
            body=body,
        )

        return handler_response


def write_long_form_article(event, context):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(write_long_form_article_async(event, context))


if __name__ == "__main__":
    event = {
        "body": json.dumps({
            "content": "Hello engineers",
            "brand_id": "38372249-fbcd-45f1-84a9-78ffa493c7c4",
            "category_id": "4878dd6b-7c33-4b74-8071-d08a13c11d04", 
            "category_slug": "recent-ai-developments-and-news"
        })
    }

    # Run the handler
    response = write_long_form_article(event, None)
    logger.info(f"Finished running handler. Response: {response}")
