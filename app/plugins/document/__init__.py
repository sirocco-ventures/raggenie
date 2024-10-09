from app.models.prompt import Prompt
from collections import OrderedDict
from app.models.request import ConnectionArgument

# Plugin Metadata
__version__ = '1.0.0'
__plugin_name__ = 'document'
__display_name__ = 'document loader'
__description__ = 'document integration for handling document data'
__icon__ = '/assets/plugins/logos/document.svg'
__category__ = 4
__actions_enabled__ = False
__actions_supported__ = []

# Connection arguments
__connection_args__ = OrderedDict(
    document_files= ConnectionArgument(
        type = 8,
        generic_name= 'document files',
        description = 'Supports only .pdf, .yaml, .txt, and .docx files.',
        order = 1,
        required = True,
        value = None,
        slug = "document_files"
    )
)

# Prompt
__prompt__ = Prompt(**{
        "base_prompt": "{system_prompt}{user_prompt}",
        "system_prompt": {
        "template": """
        You are a Chatbot designed to answer user questions based only on the context given to you.
        Use the details enclosed in [context][/context] to generate answers.
        [context]
        {context}
        [/context]

        Adhere to these rules while generating answers:
        - Carefully read through the question and context word by word to appropriately answer the question.
        - Only use information provided in the context to answer questions.
        - Answer should not break the json format
        - If the answer cannot be found in the context, state that you don't have enough information to answer.
        
        """
        },
        "user_prompt":{
            "template": """
            User question is "$question"
            Generate a JSON response in the following format without any formatting:
            {
                "explanation": "Explain how you determined the answer using the provided context",
                "general_message": "Answer to user question based on the context",
            }
            """
        },
        "regeneration_prompt": {
            "template": """
            User question is "$question"
            Generate a JSON response in the following format without any formatting:
            {
                "explanation": "Explain how you determined the answer using the provided context",
                "general_message": "Answer to user question based on the context",
            }
            """
        }
    })



__all__ = [
    __version__, __plugin_name__, __display_name__ , __description__, __icon__, __category__, __prompt__
]