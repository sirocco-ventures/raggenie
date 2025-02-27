from app.readers.docs_reader import DocsReader
from loguru import logger
import fitz
from docling.document_converter import DocumentConverter


class PDFLoader(DocsReader):
    def load(self):
        out = []
        if "path" in self.source:
            paths = self.source["path"]

            for path in paths:
                try:
                    metadata = {"path":path}

                    converter = DocumentConverter()
                    result = converter.convert(path)
                    temp = {}
                    temp["content"] = result.document.export_to_markdown()
                    temp["metadata"] = metadata
                    if len(temp["content"]) > 0:
                            out.append(temp)
                except Exception as e:
                    logger.error(e)
        return out


