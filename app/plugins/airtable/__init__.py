from app.models.prompt import Prompt
from collections import OrderedDict
from app.models.request import ConnectionArgument

# Plugin Metadata
__version__ = '1.0.0'
__plugin_name__ = 'airtable'
__display_name__ = 'Airtable'
__description__ = 'Airtable integration for handling Airtable database operations.'
__icon__ = '/assets/plugins/logos/airtable.svg'
__category__ = 2
__actions_enabled__ = False
__actions_supported__ = []


# Connection arguments
__connection_args__ = OrderedDict(
    token= ConnectionArgument(
        type = 2,
        generic_name= 'Airtable token',
        description = 'Token for airtable workspace',
        order = 2,
        required = True,
        value = None,
        slug = "api_key"
    ),
    workspace_id=ConnectionArgument(
        type= 1,
        generic_name= 'Airtable workspace id',
        description= 'Airtable workspace ID',
        order = 1,
        required = True,
        value = None,
        slug = "space_name"
    )
)

# Prompt
__prompt__ = Prompt(**{
        "base_prompt": "{system_prompt}{user_prompt}",
        "system_prompt": {
            "template": """
            You are an Airtable expert.Your job is to answer questions about the Airtable tables specified in schema.
            You must output the Airtable query that answers the question using the schema provided.
            Use the schema details and db constraints enclosed in `[schema][/schema]` to generate query


            [schema]
            {schema}
            [/schema]

            {context}

            sample queries generated previously

            question: list all hospitals
            query: https://api.airtable.com/v0/appXXXXXXX/hospitals

            question: list all hospitals in x
            query: executing query:https://api.airtable.com/v0/appXXXXXXX/hospitals?filterByFormula=AND(SEARCH(LOWER('x'),LOWER({{location}}))=1)

            question: list all hospital supports xyz ab plan
            query: https://api.airtable.com/v0/appXXXXXXX/hospitals?filterByFormula=AND(SEARCH(LOWER("xyz ab"),LOWER({{insurance_plan}}))=1)


            Adhere to these rules while generating query:
            - Deliberately go through the question and database schema word by word to appropriately answer the question
            - Dont change the field names
            - Use Lower for comparing or equality
            """
        },
        "user_prompt":{
            "template": """
            User question is "$question"
            generate a json in the following format without any formatting.
            {
                "explanation": "Explain how you finalized the sql query using the schemas and rules provided",
                "query" : "complete airtable rest api query without authentication",
                "operation_kind" : "aggregation|list",
                "general_message": "general message like 'here is the list of x'",
                "schema": "used schema details separated by comma",
                "confidence" : "confidence in 100",
                "main_entity": "document"
            }
            """
        },
        "regeneration_prompt": {
            "template": """
            User query is "$question"
            generate a json in the following format without any formatting. extra explanation is strictly prohibited.
            {
                "output": "Your answer for the question",
                "main_entity": "document",
                "operation_kind": "text"
            }
            """
        }
    })



__all__ = [
    __version__, __plugin_name__, __display_name__ , __description__, __icon__, __category__, __prompt__
]