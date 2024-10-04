from app.readers.docs_reader import DocsReader
from loguru import logger
import yaml

class YamlLoader(DocsReader):
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
                    body = yaml.safe_load(content)
                    temp["content"] = yaml.dump(body)
                    temp["metadata"] = metadata
                    out.append(temp)
                except Exception as e:
                    logger.error(e)
        return out