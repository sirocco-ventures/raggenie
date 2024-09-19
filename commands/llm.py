import click
from commands.cli import cli
from loguru import logger
from app.providers.config import configs
from app.main import create_app
import uvicorn
from app.providers.config import configs
import sys



@cli.command()
@click.pass_obj
def llm(ctx) -> None:
    """
    Starts the LLM chain server using Uvicorn.
    
    :param ctx: Configuration context passed from the CLI command.
    """
    
    logger.info("Intializing fastapi application server")
    try:
        
        app = create_app(config=ctx)
        logger.info("Intialized fastapi application")
        logger.info("Starting Uvicorn server...")
        uvicorn.run(app,
                    host="0.0.0.0", 
                    port=configs.application_port, 
                    reload=False)
        
    except Exception as e:
        logger.critical(f"Failed to start the LLM server: {e}")
        sys.exit(1)


# Registering llm command
cli.add_command(llm)
   