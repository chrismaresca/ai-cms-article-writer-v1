# -------------------------------------------------------------------------------- #
# Handler Utils
# -------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Standard Library
import json
from typing import Dict, Any, Tuple, Set

# Pydantic
from pydantic import BaseModel, ValidationError

# Logger
from src.utils.logger import logger

# -------------------------------------------------------------------------------- #
# Parse the request body
# -------------------------------------------------------------------------------- #

def parse_request_body(event: Dict[str, Any], request_model: BaseModel) -> Dict[str, Any]:
    """
    Parse and validate the JSON body from an AWS Lambda event.
    """
    try:
        # 1. Attempt to parse the JSON body.
        body = json.loads(event.get("body", "{}"))
    except json.JSONDecodeError as e:
        logger.error("Failed to decode request body as JSON", exc_info=True)
        raise ValueError("Invalid JSON in request body.") from e

    # 2. Check for empty body.
    if not body:
        logger.error("Received an empty request body.")
        raise ValueError("Request body cannot be empty.")

    # 3. For debugging, log minimal details if needed.
    logger.debug("Parsed JSON body: %s", body)

    # 4. Validate required keys (optional step, but often recommended).
    required_keys = request_model.model_json_schema()["required"]
    missing_keys = [key for key in required_keys if key not in body]

    # 5. If missing keys, raise an error.
    if missing_keys:
        logger.error(f"Missing required keys in body: {missing_keys}. Raising ValueError.")
        raise ValueError(f"Missing required keys: {', '.join(missing_keys)}")

    # 5. Return the valid, parsed body.
    return body


# -------------------------------------------------------------------------------- #
# Validate the request body
# -------------------------------------------------------------------------------- #

def validate_request_body(body: Dict[str, Any], request_model: BaseModel) -> None:
    """
    Validate the request body against the request model.
    """
    try:
        request_model(**body)
        logger.debug(f"Request validation passed for the request model: {request_model}")
    except ValidationError as e:
        logger.error(f"Request validation failed for the request model: {request_model}. Error: {e}. Raising ValueError.")
        raise ValueError(f"Request validation failed. {e} for the request model: {request_model}")


