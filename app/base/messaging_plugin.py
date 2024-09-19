from abc import ABC, abstractmethod

class MessagePlugin(ABC):

    @abstractmethod
    def send(self):
        pass
