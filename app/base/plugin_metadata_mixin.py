import importlib
from loguru import logger

class PluginMetadataMixin:
    
    # plugin default variables
    __version__ = ""
    __plugin_name__ = ""
    __description__ = ""
    __icon__ = ""
    __connection_args__= ""
    __category__ = ""
    __prompt__ = ""
    
    
    
    def __init__(self, name):
        logger.info("Initializing mixin class")
        self._load_metadata(name.removesuffix('.handler'))
        
    
    @classmethod
    def _load_metadata(self, class_path):
        module = importlib.import_module(class_path)
        
        try:
            self.__version__ = getattr(module, '__version__')
            self.__plugin_name__ = getattr(module, '__plugin_name__')
            self.__description__ = getattr(module, '__description__')
            self.__icon__ = getattr(module, '__icon__')
            self.__connection_args__ = getattr(module, '__connection_args__')
            self.__category__ = getattr(module, '__category__')   
            self.__prompt__ = getattr(module, '__prompt__')
        except Exception as e:
            raise Exception(e)