from abc import ABC, abstractmethod


class BaseFormatter(ABC):

    @abstractmethod
    def format(self)-> (dict):
        """
        Abstract method to format data.

        This method should be implemented by subclasses to define
        specific formatting logic.

        Returns:
            dict: A dictionary containing the formatted data.
        """
        pass