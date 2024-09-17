from abc import ABC, abstractmethod

class MessagePlugin(ABC):
    
    @abstractmethod
    def Send(self):
        pass
    