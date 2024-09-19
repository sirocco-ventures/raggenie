import yaml
from loguru import logger



def read_yaml_file(config_file) -> dict:
    """
    Reads a YAML file and returns its contents as a dictionary.

    :param file_path: Path to the YAML file.
    :return: Dictionary containing the file contents.
    """
    try:
        # Read YAML config file
        with open(config_file, "r") as yaml_file:
            yaml_config = yaml.safe_load(yaml_file)
        return yaml_config
    except Exception as e:
        logger.warning(e)
        return {}



