import click
from loguru import logger
from app.utils.read_config import read_yaml_file
from app.providers.config import configs
import sys

@click.group()
@click.option('--debug', default=False, envvar='DEBUG_MODE', help='Enable debug mode')
@click.option('--config', prompt='please provide config file', help='Path to the configuration file')
@click.pass_context
def cli(ctx, debug, config):
    """
    CLI for managing application commands.

    :param ctx: Click context object for passing configurations.
    :param debug: Flag to enable or disable debug mode.
    :param config: Path to the configuration file.
    """
    
    if debug:
        logger.debug("Debug mode enabled")
        
    
    logger.info("loading configurations")
    config = read_yaml_file(config)

    
    if len(config) > 0:
        ctx.obj = config
    else:
        logger.critical("Configuration data is empty or invalid")
        sys.exit(1) 
