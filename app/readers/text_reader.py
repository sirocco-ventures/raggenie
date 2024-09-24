from app.readers.docs_reader import DocsReader
from loguru import logger

class TxtLoader(DocsReader):
    def load(self):
        out = []
        if "path" in self.source:
            paths = self.source["path"]
            for path in paths:
                try:
                    metadata = {"path":path}
                    temp = {}
                    with open(path, 'r', encoding='utf-8') as file:
                        content = file.read()
                    temp["content"] = str(content)
                    temp["metadata"] = metadata
                    out.append(temp)
                except Exception as e:
                    logger.error(e)
        elif "value" in self.source:
            if self.source["value"] is not None:
                out.append(
                    {
                        "content": self.source["value"],
                        "metadata": {
                        }
                    }
                )
        return out