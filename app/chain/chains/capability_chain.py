from app.chain.modules.input_formatter import InputFormatter
from app.chain.modules.post_processor import PostProcessor
from app.chain.modules.follow_up_handler import FollowupHandler
from app.chain.modules.context_retreiver import ContextRetreiver
from app.chain.modules.followup_interpreter import FollowupInterpreter


from loguru import logger

class CapabilityChain:
    """
    CapabilityChain class represents the processing chain for handling capability-related requests.

    This class orchestrates various modules to process user input, handle follow-ups,
    interpret follow-up requests, and manage context across interactions.

    Attributes:
        common_context (dict): A shared context dictionary used across modules.
        input_formatter (InputFormatter): Module for formatting user input.
        context_retriver (ContextRetreiver): Module for retrieving context.
        followup_handler (FollowupHandler): Module for handling follow-up requests.
        followup_interpreter (FollowupInterpreter): Module for interpreting follow-up requests.
        post_processor (PostProcessor): Module for post-processing responses.
        handler: The first module in the processing chain.

    The CapabilityChain class follows a modular design, where each module is responsible
    for a specific part of the processing pipeline. This allows for flexibility
    and easy extension of functionality.
    """
    def __init__(self, model_configs, context_storage, general_chain):

        logger.info("loading modules into capability chain")


        self.common_context = {}

        self.input_formatter = InputFormatter()
        self.context_retriver = ContextRetreiver(self.common_context, context_storage)
        self.followup_handler = FollowupHandler(self.common_context, model_configs)
        self.followup_interpreter = FollowupInterpreter(self.common_context, general_chain)
        self.post_processor = PostProcessor()



        logger.info("initializing chain")
        self.input_formatter.set_next(self.context_retriver).set_next(self.followup_handler).set_next(self.followup_interpreter).set_next(self.post_processor)
        self.handler =  self.input_formatter


    def invoke(self, user_request):
        logger.info("Processing user request")
        return self.handler.handle(user_request)
