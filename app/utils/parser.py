import json
from loguru import logger

def parse_llm_response(body):
        text = body.replace("\\n","")
        text = text.replace("\n","")
        text = text.replace("\\","")
        text = text.replace("\\_","_")
        if '\\"' not in text:
            text = text.replace("\\","")
        text = text.removeprefix("```json")
        text = text.removesuffix("```")
        text = text.removesuffix("User:")

        try:
            out = json.loads(text)
        except Exception as e:
            logger.info("error parsing llm response")
            logger.critical(e)
            out = {}

        return out

def markdown_parse_llm_response(body):
        # text = body.replace("\\n","")
        # text = text.replace("\n","")
        # text = text.replace("\\","")
        # text = text.replace("\\_","_")
        # if '\\"' not in text:
        #     text = text.replace("\\","")
        text = body.removeprefix("```json")
        text = text.removesuffix("```")
        text = text.removesuffix("User:")

        try:
            out = json.loads(text)
        except Exception as e:
            logger.info("error parsing llm response")
            logger.critical(e)
            out = {}

        return out

