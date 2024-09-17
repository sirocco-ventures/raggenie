from app.readers.text_reader import TxtLoader
from app.readers.docx_reader import DocxReader
from app.readers.yaml_reader import YamlLoader
from app.readers.url_reader import UrlReader
from app.readers.pdf_reader import PDFLoader

from loguru import logger

class BaseReader:
    def __init__(self, source):
        logger.info(f"initializing docs {source}")
        self.source = source

    def load_data(self):
        type = self.source["type"] if "type" in self.source else ""
        match type:
            case "text":
                loader = TxtLoader(source=self.source)
            case "yaml":
                loader = YamlLoader(source=self.source)
            case "docx":
                loader = DocxReader(source=self.source)
            case "url":
                loader = UrlReader(source=self.source)
            case "pdf":
                loader = PDFLoader(source=self.source)
            case default:
                raise ValueError(f"Documentation in given format '{type}' not supported.")
        return loader.load()