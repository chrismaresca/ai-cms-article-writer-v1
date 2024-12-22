# Serverless Python + AWS Lambda HTTP Post To Categorize Content

An AWS Lambda function to categorize content based on the brand id and content.

## Configure Serverless

1. Install the `serverless-python-requirements` plugin if you don't have it already.

```bash
sls plugin install -n serverless-python-requirements
```


2. Install the `serverless-plugin-resource-tagging` plugin if you don't have it already.

```bash
pnpm install serverless-plugin-resource-tagging
```

3. Install the `serverless-functions-base-path` plugin if you don't have it already.

```bash
pnpm install serverless-functions-base-path
```

4. Set the following environment variables (Everything except the OpenAI API key are already set in the `.env.sample` file. To use this file, rename it to `.env` with the following command 

```bash
mv .env.sample .env
```

For a brief explanation of each environment variable, see below:

- **OPENAI_API_KEY**: Your OpenAI API key

- **PROMPT_TEMPLATE_DIR**: Directory containing prompt templates (default: prompt_templates)

- **LOG_LEVEL**: Logging level (default: DEBUG).

- **CMS_BASE_URL**: Base URL for CMS API

- **CMS_ARTICLES_PATH**: Path for articles API endpoint

- **CMS_TAGS_PATH**: Path for tags API endpoint 

- **CMS_XML_BLOCKS_PATH**: Path for XML blocks API endpoint

- **CMS_AUTHOR_ID**: Author ID for CMS. This is the author ID for the user that will be used to create the article. Should be extended in the future so we don't have to hardcode this.

5. Update `serverless.yml` to include the `serverless-python-requirements` plugin.

6. Update `serverless.yml` to include the `serverless-plugin-resource-tagging` plugin.

7. Update `serverless.yml` to include the `serverless-functions-base-path` plugin.

8. Update the 'service' of the service in `serverless.yml` to your desired service name.

9. Logging is configured in `src/utils/logger.py` to output to stdout. This should work on AWS CloudWatch. 


## Deploy Serverless

```bash
serverless deploy
```
