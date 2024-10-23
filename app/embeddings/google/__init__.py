from collections import OrderedDict
from app.models.request import ConnectionArgument

__provider_name__ = "google"
__vectordb_name__ = ["chroma"]
__icon__ = '/assets/embeddings/logos/google.svg'
__connection_args__ = [
    {
    "config": ["api_key"],
    "models": []
    }
]





__all__ = [
    __vectordb_name__, __connection_args__, __provider_name__, __icon__
]