from app.base.abstract_handlers import AbstractHandler
from typing import Any
from loguru import logger


class InputFormatter(AbstractHandler):

    def handle(self, request: Any) -> str:
        logger.info("passing through => input_formatter")

        response = request
        return super().handle(response)
