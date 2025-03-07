from app.base.abstract_handlers import AbstractHandler
from typing import Any
from loguru import logger

class PostProcessor(AbstractHandler):

    async def handle(self, request: Any) -> str:
        logger.info("passing through => post_processor")
        response = request
        return response
