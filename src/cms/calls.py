# -------------------------------------------------------------------------------- #
# CMS Fetching Functions
# -------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Standard Library
from typing import List, Any

# Requests
import requests
import httpx

# Logging
from src.utils.logger import logger

# CMS Constants
from src.cms.constants import CMS_BASE_URL, CMS_XML_BLOCKS_PATH, CMS_ARTICLES_PATH

# CMS Types
from src.cms.types import CmsXmlBlock, CmsXmlBlockParameter, CmsCreateArticleRequest


# -------------------------------------------------------------------------------- #
# Helper Functions
# -------------------------------------------------------------------------------- #

def _extract_xml_blocks(xml_blocks_response: Any) -> List[CmsXmlBlock]:
    """
    Extract and parse the XML blocks from the API response.
    """
    logger.info("Starting XML blocks extraction")

    try:
        docs = xml_blocks_response.get("docs", [])
        if not docs:
            logger.warning("No documents found in XML blocks response")
            return []

        xml_blocks = []
        for doc in docs:
            try:
                # Parse parameters for each xmlBlock
                xml_block_data = doc.get("xmlBlock", {})
                if not xml_block_data:
                    logger.warning(f"Missing xmlBlock data in document: {doc}")
                    continue

                parameters = []
                for param in xml_block_data.get("xmlBlockParameters", []):
                    try:
                        parameter = CmsXmlBlockParameter(
                            id=param.get("id"),
                            name=param.get("name"),
                            ts_name=param.get("tsName"),
                            required=param.get("required"),
                            description=param.get("description") or "",  # Default to empty string if None
                            data_type=param.get("dataType"),
                        )
                        parameters.append(parameter)
                    except Exception as e:
                        logger.error(f"Failed to parse parameter {param}: {str(e)}")
                        continue

                # Parse the xmlBlock
                xml_block = CmsXmlBlock(
                    id=xml_block_data.get("id"),
                    name=xml_block_data.get("name"),
                    ts_name=xml_block_data.get("tsName"),
                    description=xml_block_data.get("description"),
                    parameters=parameters,
                )
                xml_blocks.append(xml_block)
                logger.debug(f"Successfully parsed XML block: {xml_block.name}")

            except Exception as e:
                logger.error(f"Failed to parse document {doc}: {str(e)}")
                continue

        logger.info(f"Successfully extracted {len(xml_blocks)} XML blocks")
        return xml_blocks

    except Exception as e:
        logger.error(f"Failed to extract XML blocks: {str(e)}")
        raise ValueError(f"Failed to extract XML blocks: {str(e)}")


# -------------------------------------------------------------------------------- #
# Functions
# -------------------------------------------------------------------------------- #


# def fetch_xml_blocks(brand_id: str) -> List[CmsXmlBlock]:
#     """
#     Fetch tags from the CMS for a given brand ID.
#     """
#     # Construct the request URL
#     logger.info(f"Fetching XML blocks for brand ID: {brand_id}")
#     request_url = f"{CMS_BASE_URL}{CMS_XML_BLOCKS_PATH}?where[brandId][equals]={brand_id}"

#     # Make the request
#     logger.debug(f"Request URL: {request_url}")
#     response = requests.get(request_url)
#     response.raise_for_status()

#     logger.debug(f"Response: {response.json()}")
#     # Check if the response is successful
#     if response.status_code != 200:
#         logger.error(f"Failed to fetch XML blocks from CMS. Status code: {response.status_code}. Response: {response.text}")
#         raise ValueError(f"Failed to fetch XML blocks from CMS. Status code: {response.status_code}. Response: {response.text}")

#     # Parse the response
#     logger.info(f"XML blocks successfully fetched from CMS")
#     # Extract the XML blocks
#     xml_blocks = _extract_xml_blocks(response.json())
#     logger.info(f"XML blocks successfully extracted.")
#     # Return the XML blocks
#     return xml_blocks


# def create_article_in_cms(cms_create_article_request: CmsCreateArticleRequest) -> str:
#     """
#     Create an article in the CMS.
#     """

#     # Make the request
#     request_url = f"{CMS_BASE_URL}{CMS_ARTICLES_PATH}"
#     logger.info(f"Creating article in CMS. Request URL: {request_url}.")

#     response = requests.post(request_url, json=cms_create_article_request.model_dump())
#     response.raise_for_status()

#     if response.status_code != 200:
#         logger.error(f"Failed to create article in CMS. Status code: {response.status_code}. Response: {response.text}")
#         raise ValueError(f"Failed to create article in CMS. Status code: {response.status_code}. Response: {response.text}")

#     logger.info(f"Article created in CMS.")
#     logger.debug(f"Article created in CMS. Response: {response.json()}")

#     article_id = response.json().get("id")

#     if not article_id:
#         logger.error(f"Something went wrong when parsing the response. Response: {response.json()}")
#         raise ValueError(f"Something went wrong when parsing the response. Response: {response.json()}")

#     # Return the response
#     return article_id



async def fetch_xml_blocks(brand_id: str) -> List[CmsXmlBlock]:
    """
    Fetch tags from the CMS for a given brand ID.
    """
    # Construct the request URL
    logger.info(f"Fetching XML blocks for brand ID: {brand_id}")
    request_url = f"{CMS_BASE_URL}{CMS_XML_BLOCKS_PATH}?where[brandId][equals]={brand_id}"

    # Make the request
    logger.debug(f"Request URL: {request_url}")
    async with httpx.AsyncClient() as client:
        response = await client.get(request_url)

    response.raise_for_status()

    logger.debug(f"Response: {response.json()}")
    # Check if the response is successful
    if response.status_code != 200:
        logger.error(f"Failed to fetch XML blocks from CMS. Status code: {response.status_code}. Response: {response.text}")
        raise ValueError(f"Failed to fetch XML blocks from CMS. Status code: {response.status_code}. Response: {response.text}")

    # Parse the response
    logger.info(f"XML blocks successfully fetched from CMS")
    # Extract the XML blocks
    xml_blocks = _extract_xml_blocks(response.json())
    logger.info(f"XML blocks successfully extracted.")
    # Return the XML blocks
    return xml_blocks


async def create_article_in_cms(cms_create_article_request: CmsCreateArticleRequest) -> str:
    """
    Create an article in the CMS.
    """

    # Make the request
    request_url = f"{CMS_BASE_URL}{CMS_ARTICLES_PATH}"
    logger.info(f"\n\nCreating article in CMS. Request URL: {request_url}. With body: {cms_create_article_request.model_dump()}\n\n")

    # Use async client to make the request
    async with httpx.AsyncClient() as client:
        response = await client.post(request_url, json=cms_create_article_request.model_dump())

    # Check if the response is successful
    if response.status_code != 200:
        logger.error(f"Failed to create article in CMS. Status code: {response.status_code}. Response: {response.text}")
        raise ValueError(f"Failed to create article in CMS. Status code: {response.status_code}. Response: {response.text}")

    # Log the response
    logger.info(f"Article created in CMS.")
    logger.debug(f"Article created in CMS. Response: {response.json()}")

    # Parse the response into the article ID
    article_id = response.json().get("id")

    # Check if the article ID is present. If not, raise an error
    if not article_id:
        logger.error(f"Something went wrong when parsing the response. Response: {response.json()}")
        raise ValueError(f"Something went wrong when parsing the response. Response: {response.json()}")

    # Return the response
    return article_id
