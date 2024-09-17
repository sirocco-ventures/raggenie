from app.base.abstract_handlers import AbstractHandler
from typing import Any, Optional
from loguru import logger

class PostProcessor(AbstractHandler):
        
    def handle(self, request: Any) -> str:
        logger.info("passing through => post_processor")
        response = request
        return response
