from app.base.abstract_handlers import AbstractHandler
from typing import Any
from loguru import logger


class InputFormatter(AbstractHandler):

    async def handle(self, request: Any) -> str:
        logger.info("passing through => input_formatter")

        response = request
        return await super().handle(response)
