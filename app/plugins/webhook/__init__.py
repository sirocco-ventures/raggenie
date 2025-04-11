from app.models.prompt import Prompt
from collections import OrderedDict
from app.models.request import ConnectionArgument

# Plugin Metadata
__version__ = '1.0.0'
__plugin_name__ = 'webhook'
__display_name__ = 'Webhooks'
__description__ = 'Webhooks integration for pushing data to rest endpoints'
__icon__ = '/assets/plugins/logos/webhook.svg'
__category__ = 3
__actions_enabled__ = True
__actions_supported__ = ["send"]


# Connection arguments
__connection_args__ = OrderedDict(
    webhook_url= ConnectionArgument(
        type = 4,
        generic_name= 'Webhook URL',
        description = 'URL of website',
        order = 1,
        required = True,
        value = None,
        slug = "webhook_url"
    ),
    webhook_method= ConnectionArgument(
        type = 6,
        generic_name= 'Webhook Method',
        description = 'HTTP method to exexute',
        order = 2,
        required = True,
        value=[{"label":"post", "value": "POST"}, {"label":"get", "value": "GET"}, {"label":"put", "value": "PUT"}],
        slug = "webhook_method"
    ),
    webhook_headers= ConnectionArgument(
        type = 7,
        generic_name= 'Webhook headers',
        description = 'HTTP headers to pass',
        order = 3,
        required = True,
        value = None,
        slug = "webhook_headers"
    )
)

# Prompt
__prompt__ = Prompt(**{
        "base_prompt": "{system_prompt}{user_prompt}",
        "system_prompt": {
            "template": """
            You are an Chatbot designed to answer user questions based only on the context given to you.
            Use the details enclosed in `[context][/context]` to generate answer

            [context]
            {context}
            [/context]

            Adhere to these rules while generating query:
            - Deliberately go through the question and context word by word to appropriately answer the question
            """
        },
        "user_prompt":{
            "template": """
            User question is "$question"
            generate a json in the following format without any formatting.
            {
                "explanation": "Explain how you finalized the sql query using the schemas and rules provided",
                "operation_kind" : "none",
                "general_message": "answer to user question based on the context",
                "confidence" : "confidence in 100",
                "main_entity": "document"
            }
            """
        },
        "regeneration_prompt": {
            "template": """
            User question is "$question"
            generate a json in the following format without any formatting.
            {
                "explanation": "Explain how you finalized the sql query using the schemas and rules provided",
                "operation_kind" : "none",
                "general_message": "answer to user question based on the context",
                "confidence" : "confidence in 100",
                "main_entity": "document"
            }
            """
        }
    })



__all__ = [
    __version__, __plugin_name__, __display_name__ , __description__, __icon__, __category__, __prompt__
]