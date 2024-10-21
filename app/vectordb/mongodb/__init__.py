from collections import OrderedDict
from app.models.request import ConnectionArgument

# Plugin Metadata
__version__ = '1.0.0'
__vectordb_name__ = 'mongodb'
__display_name__ = 'MongoDB'
__description__ = 'MongoDB for Vector Storage'
__icon__ = '/assets/vectordb/logos/mongodb.svg'
__connection_args__ = [
    {
        "type": 4,
        "name": "MongoDB uri",
        "description": "URI to connect to MongoDB",
        "order": 1,
        "required": True,
        "slug": "uri",
        "field": "uri"
    }
]





__all__ = [
    __version__, __vectordb_name__, __display_name__ , __description__, __icon__, __connection_args__
]