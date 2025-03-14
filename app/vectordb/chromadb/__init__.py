from collections import OrderedDict
from app.models.request import ConnectionArgument

# Plugin Metadata
__version__ = '1.0.0'
__vectordb_name__ = 'chroma'
__display_name__ = 'ChromaDB'
__description__ = 'ChromaDB for Vector Storage'
__icon__ = '/assets/vectordb/logos/chromadb.svg'
__connection_args__ = [
    {
        "config_type": 1,
        "name": "ChromaDB path",
        "description": "path to connect to ChromaDB",
        "order": 1,
        "required": True,
        "slug": "path",
        "field": "path",
        "placeholder": "./chromadb",
    }
]





__all__ = [
    __version__, __vectordb_name__, __display_name__ , __description__, __icon__, __connection_args__
]