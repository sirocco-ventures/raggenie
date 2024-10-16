import requests

def openai_llm_models(llm_provider):
    """
    Retrieve models from the OpenAI API.

    Args:
        llm_provider: The LLM provider object with API key.

    Returns:
        List of OpenAI model names or an error message.
    """
    url = "https://api.openai.com/v1/models"
    headers = {
        "Authorization": f"Bearer {llm_provider.api_key}",
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            models = [{"display_name": model["id"], "id": model["id"]} for model in data.get("data", [])]

            return models, False
        else:
            return f"Failed to retrieve OpenAI models: {response.status_code} {response.text}", True
    except requests.RequestException as e:
        return f"Error occurred: {str(e)}", True

def togetherai_llm_models(llm_provider):
    """
    Retrieve models from the TogetherAI API.

    Args:
        llm_provider: The LLM provider object with API key.

    Returns:
        List of TogetherAI model names or an error message.
    """
    url = "https://api.together.xyz/v1/models"
    headers = {
        "Authorization": f"Bearer {llm_provider.api_key}",
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            models = [{"display_name": model["display_name"], "id": model["id"]} for model in data]

            return models, False
        else:
            return f"Failed to retrieve TogetherAI models: {response.status_code} {response.text}", True
    except requests.RequestException as e:
        return f"Error occurred: {str(e)}", True

import requests

def ai71_llm_models(llm_provider):
    """
    Retrieve models from the AI71 API and reformat the response.

    Args:
        llm_provider: The LLM provider object with API key.

    Returns:
        List of reformatted model information or an error message.
    """
    url = "https://api.ai71.ai/v1/models"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            models = [{"display_name": model["name"], "id": model["id"]} for model in data.get("data", [])]
            return models, False
        else:
            return f"Failed to retrieve AI71 models: {response.status_code} {response.text}", True
    except requests.RequestException as e:
        return f"Error occurred: {str(e)}", True


def model_reader(llm_provider):
    """
    Retrieves the models for a given LLM provider based on its key.

    Args:
        llm_provider: The LLM provider object with API key and key.

    Returns:
        List of model names or an error message.
    """
    match llm_provider.key:
        case "openai":
            return openai_llm_models(llm_provider)
        case "togethor":
            return togetherai_llm_models(llm_provider)
        case "ai71":
            return ai71_llm_models(llm_provider)
        case _:
            return "Invalid LLM provider key", False