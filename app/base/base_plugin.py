from abc import ABC, abstractmethod

class BasePlugin(ABC):
    
    @abstractmethod
    def connect(self):
        pass
    
    @abstractmethod
    def healthcheck(self):
        pass