# -------------------------------------------------------------------------------- #
# LLM Utils
# -------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #
from typing import List, Dict, Any


# -------------------------------------------------------------------------------- #
# Functions
# -------------------------------------------------------------------------------- #


def o1_messages_format(developer_prompt: str) -> List[Dict[str, Any]]:
    """
    Create a list of messages for OpenAI's o1 reasoning models.
    """

    return [{
        "role": "user",
        "content": [{
            "type": "text",
            "text": developer_prompt
        }]
    }]


# -------------------------------------------------------------------------------- #
def base_model_messages_format(developer_prompt: str,
                               execution_prompt: str) -> List[Dict[str, Any]]:
    """
    Create a list of messages for OpenAI's non-reasoning models
    """

    return [{
        "role": "system",
        "content": [{
            "type": "text",
            "text": developer_prompt
        }]
    }, {
        "role": "user",
        "content": [{
            "type": "text",
            "text": execution_prompt
        }]
    }]
