from app.base.abstract_handlers import AbstractHandler
from typing import Any
from loguru import logger
from app.providers.config import configs


class Executer(AbstractHandler):
    """
    A handler class for executing queries based on the inference.

    This class extends AbstractHandler and provides functionality to execute
    queries using the appropriate datasource and handle any errors that occur.
    """

    def __init__(self, common_context, datasource, fallback_handler) -> None:
        """
        Initialize the Executer.

        Args:
            common_context (Dict[str, Any]): The common context shared across handlers.
            datasource (Dict[str, Any]): A dictionary of datasources keyed by intent.
            fallback_handler (AbstractHandler): The handler to call in case of errors.
        """

        self.fall_back_handler = fallback_handler
        self.common_context = common_context
        self.datasource = datasource

    def handle(self, request: Any) -> str:
        """
        Handle the incoming request by executing the query.

        Args:
            request (Dict[str, Any]): The incoming request to be processed.

        Returns:
            str: The response after processing the request.
        """
        logger.info("passing through => executor")

        inference = request.get("inference", {})
        formated_sql = inference.get("query", "")
        logger.debug(f"executing query:{formated_sql}")

        out, err = self.datasource[self.common_context["intent"]].fetch_data(formated_sql)


        if err is not None:
            logger.error(f"error in executing query:{err}")
            if self.common_context["chain_retries"] < configs.retry_limit :
                logger.info("going back for resolving error")
                self.common_context["chain_retries"] =self.common_context["chain_retries"] + 1
                self.common_context["execution_logs"].append({"query": formated_sql, "error": str(err)})
                return self.fall_back_handler.handle(request)

        response = {**dict(request), **{
            "query_response": out,
            "query_error": err,
        }}

        return super().handle(response)
