# -------------------------------------------------------------------------------- #
# Ingest Module
# -------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Built-in imports
from typing import Optional, Dict, Any
import time

# OpenAI imports
from openai import OpenAI, AsyncOpenAI

# Pydantic imports
from pydantic import BaseModel


# Jinja imports
from src.utils.jinja_utils import render_prompt_template_with_kwargs

# Types
from src.llm.types import TitleExcerptResponse

# LLM Utils
from src.utils.llm_utils import o1_messages_format, base_model_messages_format

# LLM Constants
from src.llm.constants import O1_MODEL, BASE_MODEL

# Logger imports
from src.utils.logger import logger

# -------------------------------------------------------------------------------- #
# Client
# -------------------------------------------------------------------------------- #

# TODO: Make this a singleton
client = AsyncOpenAI()


# -------------------------------------------------------------------------------- #
# o1 Call
# -------------------------------------------------------------------------------- #

async def call_content_generation_agent(category_slug: str, developer_prompt_kwargs: Dict[str, Any]) -> str:
    """
    Call the LLM to generate a v1 draft of given source content.
    """

    template_name = f"{category_slug}-template.jinja"

    # Get the start time
    start_time = time.monotonic()
    logger.debug(f"Calling content generation agent with template name: {template_name} and kwargs: {developer_prompt_kwargs}")

    # Render the developer prompt
    developer_prompt = render_prompt_template_with_kwargs(template_name=template_name,
                                                          **developer_prompt_kwargs)

    # Format the messages
    messages = o1_messages_format(developer_prompt)

    # Log initial call with model name
    logger.info(f"Calling {O1_MODEL} now to generate draft article content...")

    # Call the LLM
    response = await client.chat.completions.create(
        model=O1_MODEL,
        messages=messages
    )

    logger.debug(f"The response is: {response.choices[0].message.content}")

    # Get the call latency
    latency = time.monotonic() - start_time
    # Log finish call with latency
    logger.info(f"Finished calling {O1_MODEL} model. Took: {latency:.2f}s to generate draft article content from source.")
    return response.choices[0].message.content


# -------------------------------------------------------------------------------- #
# Parser Call
# -------------------------------------------------------------------------------- #


async def call_title_and_excerpt_generation_agent(content: str) -> TitleExcerptResponse:
    """
    Call the LLM to generate a title and excerpt from the given content source.
    """

    # Get the start time
    start_time = time.monotonic()


    # TODO: Improve this
    developer_prompt_name = "title-and-expert-developer.jinja"
    execution_prompt_name = "title-and-expert-execution.jinja"

    # Render the developer prompt
    developer_prompt = render_prompt_template_with_kwargs(template_name=developer_prompt_name)

    # Render the execution prompt
    execution_prompt = render_prompt_template_with_kwargs(template_name=execution_prompt_name,
                                                          content=content)

    # Format the messages
    messages = base_model_messages_format(developer_prompt, execution_prompt)

    # Log initial call with model name
    logger.info(f"Calling {BASE_MODEL} now to generate an article title and excerpt...")

    # Start the timer
    start_time = time.monotonic()

    # Call the LLM
    response = await client.beta.chat.completions.parse(
        model=BASE_MODEL, response_format=TitleExcerptResponse, messages=messages)
    
    logger.debug(f"The response is: {response.choices[0].message.parsed}")

    # Get the call latency
    latency = time.monotonic() - start_time
    # Log finish call with latency
    logger.info(f"Finished calling {BASE_MODEL} model. Took: {latency:.2f}s to generate an article title and excerpt.")
    return response.choices[0].message.parsed
