# -------------------------------------------------------------------------------- #
# Jinja2 Utils
# -------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Built-in imports
import os
from typing import Optional, Set

# Jinja2 imports
from jinja2 import Environment, FileSystemLoader, meta

# Logging
from src.utils.logger import logger

# Load environment variables
from dotenv import load_dotenv
load_dotenv()


# -------------------------------------------------------------------------------- #
# Prompt Template Directory
# -------------------------------------------------------------------------------- #

PROMPT_TEMPLATE_DIR = os.environ.get("PROMPT_TEMPLATE_DIR")
if not PROMPT_TEMPLATE_DIR:
    logger.error("PROMPT_TEMPLATE_DIR environment variable must be set")
    raise ValueError("PROMPT_TEMPLATE_DIR environment variable must be set")


# -------------------------------------------------------------------------------- #
# Jinja2 Utils
# -------------------------------------------------------------------------------- #

# TODO: make a singleton
def create_prompt_environment() -> Environment:
    """
    Create a Jinja2 environment for prompt templates that can load templates from a given directory.
    """
    logger.info(f"Creating Jinja2 environment for prompt templates from directory: {PROMPT_TEMPLATE_DIR}")
    env = Environment(
        loader=FileSystemLoader(PROMPT_TEMPLATE_DIR),
        autoescape=True
    )

    logger.debug(f"Jinj2 enironment successfully created. Here are the templates within the directory: {env.list_templates()}")

    
    logger.info(f"Jinja2 environment created successfully")
    return env


# def get_template_name(template_name: str,
#                       env: Optional[Environment] = None) -> Set[str]:
#     """
#     Get the required kwargs for a given template name.
#     """
#     # Create the environment if it doesn't exist
#     if not env:
#         env = create_prompt_environment()

#     # Get the template
#     logger.debug(f"Getting required kwargs for template {template_name}")
#     template = env.loader.get_source(env, template_name)
#     # Parse the template
#     parsed_template = env.parse(template)
#     # Get the required kwargs
#     required_kwargs = meta.find_undeclared_variables(parsed_template)
#     logger.debug(f"Required kwargs for template {template_name}: {required_kwargs}")
#     return required_kwargs


def render_prompt_template_with_kwargs(template_name: str,
                                       env: Optional[Environment] = None,
                                       **kwargs) -> str:
    """
    Render a Jinja2 template by name, injecting any variables provided as kwargs.
    """
    # Create the environment if it doesn't exist
    if not env:
        env = create_prompt_environment()

    # Get the template
    logger.info(f"Getting template {template_name}")
    try:
        template = env.get_template(template_name)
        logger.info(f"Template {template_name} fetched successfully")
    except Exception as e:
        logger.error(f"Failed to fetch template {template_name}. Error: {e}")
        raise e
    # Render the template
    rendered_template = template.render(**kwargs)
    logger.info(f"Template {template_name} rendered successfully")
    return rendered_template
