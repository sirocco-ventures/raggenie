from dependency_injector import containers, providers
from app.plugins.loader import DSLoader
from app.providers.clustering import Clustering
from app.vectordb.loader import VectorDBLoader





class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    datasources = providers.Singleton(lambda config: {ds['name']: DSLoader(
            ds
        ).load_ds() for ds in config["datasources"]} if config and config.get("datasources") else None, config)
    vectorstore = providers.Singleton(VectorDBLoader, config = config.vector_db)
    clustering = providers.Singleton(Clustering)


