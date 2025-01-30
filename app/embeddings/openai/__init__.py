from collections import OrderedDict
from app.models.request import ConnectionArgument


__provider_name__ = "openai"
__vectordb_name__ = ["chroma"]
__icon__ = '/assets/embeddings/logos/openai.svg'
__connection_args__ = [
    {
        "config": ["api_key"],
        "models": [
                "text-embedding-ada-002",
                "text-embedding-3-small",
                "text-embedding-3-large"
        ]
    }
]





__all__ = [
    __vectordb_name__, __connection_args__, __provider_name__, __icon__
]