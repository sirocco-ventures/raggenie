from loguru import logger
import importlib
import pkgutil




def get_plugin_providers():
    plugins = importlib.import_module("app.plugins")
    modules = []
    for module_info in pkgutil.iter_modules(plugins.__path__):
        module_name = f"{plugins.__name__}.{module_info.name}"
        try:
            module = importlib.import_module(module_name)
            modules.append({
                "version": getattr(module, '__version__'),
                "icon": getattr(module, '__icon__'),
                "plugin_name": getattr(module, '__plugin_name__'),
                "display_name": getattr(module, '__display_name__'),
                "description": getattr(module, '__description__'),
                "category": getattr(module, '__category__'),
                "args": getattr(module, "__connection_args__")
            })
            
        except Exception as e:
            logger.info(f"failed loading {module_info.name}")
            
    return modules

def get_llm_providers():
    plugins = importlib.import_module("app.loaders")
    modules = []
    for module_info in pkgutil.iter_modules(plugins.__path__):
        module_name = f"{plugins.__name__}.{module_info.name}"
        try:
            module = importlib.import_module(module_name)
            modules.append({
                "display_name": getattr(module, '__display_name__'),
                "unique_name": getattr(module, '__unique_name__'),
                "icon": getattr(module, '__icon__')
            })
            
        except Exception as e:
            logger.info(f"failed loading {module_info.name}")
            
    return modules