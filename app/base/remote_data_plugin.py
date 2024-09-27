from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class RemoteDataPlugin(ABC):

    @abstractmethod
    def fetch_data(self, params: Optional[Dict[str, Any]] = None) -> list:
        """
        Fetches data based on the provided parameters.

        :param params: Optional query parameters.
        :return: a list of strings
        """
        pass
