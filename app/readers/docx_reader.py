from app.readers.docs_reader import DocsReader
from loguru import logger
import textract

class DocxReader(DocsReader):
    def load(self):
        out = []
        if "path" in self.source:
            paths = self.source["path"]
            for path in paths:
                try:
                    text = textract.process(path)
                    metadata = {
                        "path": path
                    }
                    out.append({"content": str(text), "metadata": metadata})
                    
                except Exception as e:
                            logger.error(e)
        return out