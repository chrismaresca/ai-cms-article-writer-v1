# -------------------------------------------------------------------------------- #
# AI Configuration
# -------------------------------------------------------------------------------- #

# OpenAI Model Name
MODEL_NAME = 'gpt-4o'

# -------------------------------------------------------------------------------- #
# Prompt Templates
# -------------------------------------------------------------------------------- #


# XML Parameters Template
XML_PARAMETERS_TEMPLATE: str = """
<parameter>
    <name>{parameter_name}</name>
    <optional>{parameter_optional}</optional>
    <description>{parameter_description}</description>
</parameter>
"""

# XML Tags
XML_BLOCK_TEMPLATE: str = """
<custom-xml-block>

    <name>{xml_block_name}</name>
    <when-to-use>{xml_block_description}</when-to-use>
    <parameters>
        {xml_parameters}
    </parameters>
</custom-xml-block>
"""


# System Prompt
SYSTEM_PROMPT_TEMPLATE: str = """

<<purpose>
    You are an expert writer that sifts through content about the most recent AI developments and news.
    Your goal is to transform the given content and into an MDX structured article that can be used to create a blog post. 
    The article should be 1000-1500 words and include a title, subtitle, and a table of contents.
</purpose>

<instructions>
    <instruction>Analyze the provided in the [[content]] tags.</instruction>
    <instruction>IMPORTANT:Ignore any ads, sponsors, discussions about personal agencies/businesses, or self-promotion content. Discard this information in the analysis and writing. verify that the content is not self-promotional or sponsored before outputting the article.</instruction>
    <instruction>The article should be 1000-1500 words and include a title, subtitle, and a table of contents.</instruction>
    <instruction>You have all of the basic MDX tags available to you, along with custom XML blocks that you can use to structure the article. These blocks are defined in the <custom-xml-blocks> section. Only use them if needed.</instruction>
    <instruction>Return the result as a JSON object with keys "content" (string; as MDX formatted content), and nothing else.</instruction>
    <instruction>Do not include any text outside of the JSON object.</instruction>
</instructions>

<custom-xml-blocks>

    {xml_blocks}
    
</custom-xml-blocks>
"""


# User Prompt Template
USER_PROMPT_TEMPLATE: str = """

<user-input>
    <raw-content>
        {raw_content}
    </raw-content>
</user-input>
"""
