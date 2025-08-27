from app.providers.document_parser.docling import DoclingParser
from app.providers.document_parser.azure import AzureParser
from loguru import logger

class ParserEngineLoader:
        
    def load_engine(self, unique_name):
        engine_class = {
            "docling": DoclingParser,
            "azure": AzureParser
        }
        engine = engine_class.get(unique_name)
        if engine:
            try:
                en = engine()
                return en
            except Exception as e:
                logger.error(f"Failed to load parser {unique_name}: {e}")
                return None
            
        else:
            logger.warning("Invalid engine specified in configuration.")
            return None
            