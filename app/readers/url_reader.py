from app.readers.docs_reader import DocsReader
from loguru import logger
import requests
from bs4 import BeautifulSoup



class UrlReader(DocsReader):
    def load(self):
        out = []
        if "path" in self.source:
            urls = self.source["path"]
            for url in urls:
                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        tag = soup.body
                        text = ''.join(list(tag.strings)[:-1])
                        metadata = {
                            "path": url
                        }
                        out.append({"content": str(text), "metadata": metadata})
                    else:
                        logger.critical(f"Failed to retrieve content, status code: {response.status_code}")

                except Exception as e:
                            logger.error(e)
        return out