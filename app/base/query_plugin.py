from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Tuple

class QueryPlugin(ABC):

    @abstractmethod
    def fetch_data(self, query: str, params: Optional[Dict[str, Any]] = None) -> Tuple[Any, Optional[str]]:
        """
        Fetches data based on the provided query.

        :param query: The query.
        :param params: Optional query parameters.
        :return: A tuple containing the fetched data and an optional error message.
        """
        pass

    @abstractmethod
    def fetch_schema_details(self) -> Tuple[list, list]:
        """
        Fetches schema details from Airtable.

        :return: A tuple containing schema DDL as a list of strings and table metadata.
        """
        pass

    @abstractmethod
    def create_ddl_from_metadata(self, table_metadata: list) -> list:
        """
        Creates DDL from table metadata.

        :param table_metadata: List of table metadata dictionaries.
        :return: List of schema DDL strings.
        """
        pass

    @abstractmethod
    def validate(self, formatted_sql: str) -> None:
        """
        Validates the provided SQL.

        :param formatted_sql: SQL string to validate.
        """
        pass