from app.models.prompt import Prompt
from collections import OrderedDict
from app.models.request import ConnectionArgument

# Plugin Metadata
__version__ = '1.0.0'
__plugin_name__ = 'sharepoint'
__display_name__ = 'SharePoint Loader'
__description__ = 'SharePoint integration for handling SharePoint data'
__icon__ = '/assets/plugins/logos/sharepoint.svg'
__category__ = 2

# Connection arguments
__connection_args__ = OrderedDict(
    sharepoint_site_url=ConnectionArgument(
        type=4,
        generic_name='SharePoint Site URL',
        description='URL of the SharePoint site',
        order=1,
        required=True,
        value=None,
        slug="sharepoint_site_url"
    ),
    client_id=ConnectionArgument(
        type=1,
        generic_name='Client ID',
        description='Client ID for authentication',
        order=2,
        required=True,
        value=None,
        slug="client_id"
    ),
    client_secret=ConnectionArgument(
        type=1,
        generic_name='Client Secret',
        description='Client Secret for authentication',
        order=3,
        required=True,
        value=None,
        slug="client_secret"
    ),
    tenant_id=ConnectionArgument(
        type=1,
        generic_name='Tenant ID',
        description='Tenant ID for SharePoint',
        order=4,
        required=False,
        value=None,
        slug="tenant_id"
    )
)

# Prompt
__prompt__ = Prompt(**{
    "base_prompt": "{system_prompt}{user_prompt}",
    "system_prompt": {
        "template": """
        You are a Chatbot designed to answer user questions based only on the context given to you.
        Use the details enclosed in `[context][/context]` to generate answers.

        [context]
        {context}
        [/context]

        Adhere to these rules while generating queries:
        - Deliberately go through the question and context word by word to appropriately answer the question.
        """
    },
    "user_prompt": {
        "template": """
        User question is "$question"
        generate a JSON in the following format without any formatting.
        {
            "explanation": "Explain how you finalized the query using the schemas and rules provided",
            "operation_kind": "none",
            "general_message": "Answer to user question based on the context",
            "confidence": "confidence in 100",
            "main_entity": "document"
        }
        """
    },
    "regeneration_prompt": {
        "template": """
        User question is "$question"
        generate a JSON in the following format without any formatting.
        {
            "explanation": "Explain how you finalized the query using the schemas and rules provided",
            "operation_kind": "none",
            "general_message": "Answer to user question based on the context",
            "confidence": "confidence in 100",
            "main_entity": "document"
        }
        """
    }
})

__all__ = [
    __version__, __plugin_name__, __display_name__, __description__, __icon__, __category__, __prompt__
]
