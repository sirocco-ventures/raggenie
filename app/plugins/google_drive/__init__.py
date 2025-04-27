from app.models.prompt import Prompt, SystemPrompt, UserPrompt, RegenerationPrompt
from collections import OrderedDict
from app.models.request import ConnectionArgument

# Plugin Metadata
__version__ = '1.0.0'
__plugin_name__ = 'google_drive'
__display_name__ = 'Google Drive Documents'
__description__ = 'Plugin to fetch documents from Google Drive.'
__icon__ = '/assets/plugins/logos/google-drive.svg'
__category__ = 2  # Example category (like document loaders)

# Connection arguments
__connection_args__ = OrderedDict(
    credentials_path=ConnectionArgument(
        type=1,
        generic_name='Service Account Credentials Path',
        description='Path to your downloaded Google Service Account JSON key file.',
        order=1,
        required=True,
        value=None,
        slug="credentials_path"
    ),
    folder_id=ConnectionArgument(
        type=1,
        generic_name='Google Drive Folder ID',
        description='ID of the Google Drive folder you want to load documents from.',
        order=2,
        required=True,
        value=None,
        slug="folder_id"
    ),
)

# Prompt
__prompt__ = Prompt(
    base_prompt="{system_prompt}{user_prompt}",
    system_prompt=SystemPrompt(
        template="""
        You are a document loader expert specializing in fetching and reading files from Google Drive folders.
        Extract and present the content based on user needs.
        """
    ),
    user_prompt=UserPrompt(
        template="""
        Load documents like PDFs, DOCXs, and TXTs from the specified Google Drive folder ID.
        """
    ),
    regeneration_prompt=RegenerationPrompt(
        template="No regeneration needed for document loading tasks."
    )
)

# Export all
__all__ = [
    __version__,
    __plugin_name__,
    __display_name__,
    __description__,
    __icon__,
    __category__,
    __prompt__,
    __connection_args__,
]
