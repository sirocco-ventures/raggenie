from app.readers.docs_reader import DocsReader
from loguru import logger
import fitz

class PDFLoader(DocsReader):
    def load(self):
        out = []
        if "path" in self.source:
            paths = self.source["path"]
            
            for path in paths:
                try:
                    reader = fitz.open(path)

                    metadata = {"path":path}
                    for page_index, page in enumerate(reader):
                        temp = {} 
                        temp["content"] = page.get_text()
                        temp["metadata"] = {**metadata, "page_number": page_index}
                        if len(temp["content"]) > 0:
                            out.append(temp)
                            


                except Exception as e:
                    logger.error(e)
        return out
    

