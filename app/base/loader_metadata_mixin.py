import importlib
from loguru import logger

class LoaderMetadataMixin:

    # plugin default variables
    __unique_name__ = ""
    __display_name__ = ""
    __icon__ = ""


    def __init__(self, name):
        logger.info("Initializing mixin class")
        self._load_metadata(name.removesuffix('.loader'))


    @classmethod
    def _load_metadata(self, class_path):
        module = importlib.import_module(class_path)

        try:
            self.__unique_name__ = getattr(module, '__unique_name__')
            self.__display_name__ = getattr(module, '__display_name__')
            self.__icon__ = getattr(module, '__icon__')
        except Exception as e:
            raise Exception(e)