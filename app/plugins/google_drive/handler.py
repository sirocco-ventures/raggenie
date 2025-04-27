import os
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
from loguru import logger
from app.base.base_plugin import BasePlugin
from app.base.document_data_plugin import DocumentDataPlugin
from app.base.plugin_metadata_mixin import PluginMetadataMixin
from app.readers.base_reader import BaseReader
from typing import Tuple, Optional

class GoogleDriveLoader(BasePlugin, PluginMetadataMixin, DocumentDataPlugin):
    """
    GoogleDriveLoader for loading files from Google Drive.
    """

    def __init__(self, connector_name: str, credentials_path: str, folder_id: str):
        super().__init__(__name__)
        
        self.connector_name = connector_name.replace(' ', '_')
        self.credentials_path = credentials_path
        self.folder_id = folder_id
        self.service = None

        # File types supported
        self.supported_types = {".pdf": "pdf", ".docx": "docx", ".txt": "text"}

    def connect(self) -> Tuple[bool, Optional[str]]:
        """
        Authenticate and connect to Google Drive.
        """
        try:
            creds = service_account.Credentials.from_service_account_file(
                self.credentials_path,
                scopes=["https://www.googleapis.com/auth/drive"]
            )
            self.service = build('drive', 'v3', credentials=creds)
            logger.info("Successfully connected to Google Drive.")
            return True, None
        except Exception as e:
            logger.error(f"Failed to connect to Google Drive: {str(e)}")
            return False, str(e)

    def healthcheck(self) -> Tuple[bool, Optional[str]]:
        """
        Perform a healthcheck by listing files in the folder.
        """
        logger.info("Performing healthcheck for Google Drive...")
        try:
            results = self.service.files().list(
                q=f"'{self.folder_id}' in parents and trashed = false",
                pageSize=1,
                fields="files(id, name)"
            ).execute()
            files = results.get('files', [])
            if not files:
                logger.warning("No files found in the folder.")
            return True, None
        except Exception as e:
            logger.error(f"Healthcheck failed: {str(e)}")
            return False, str(e)

    def fetch_data(self, params=None):
        """
        Fetch and download supported files from Google Drive.
        """
        logger.info("Fetching files from Google Drive...")
        data = []

        try:
            results = self.service.files().list(
                q=f"'{self.folder_id}' in parents and trashed = false",
                fields="files(id, name)"
            ).execute()

            files = results.get('files', [])

            for file in files:
                file_name = file['name']
                file_id = file['id']

                file_type = None
                for ext, typ in self.supported_types.items():
                    if file_name.endswith(ext):
                        file_type = typ
                        break

                if file_type is None:
                    logger.warning(f"Unsupported file type: {file_name}")
                    continue

                request = self.service.files().get_media(fileId=file_id)
                fh = io.BytesIO()
                downloader = MediaIoBaseDownload(fh, request)

                done = False
                while done is False:
                    status, done = downloader.next_chunk()

                fh.seek(0)

                temp_path = f"temp_{file_name}"
                with open(temp_path, "wb") as f:
                    f.write(fh.read())

                # Use BaseReader to parse downloaded file
                reader = BaseReader({
                    "type": file_type,
                    "path": [temp_path]
                })

                data.extend(reader.load_data())

                # Clean up temp file
                os.remove(temp_path)

            return data

        except Exception as e:
            logger.error(f"Failed to fetch data from Google Drive: {str(e)}")
            return []

    def close_connection(self):
        """
        Close the connection. (Not much needed for Drive, but kept for uniformity)
        """
        self.service = None
        logger.info("Closed Google Drive connection.")
