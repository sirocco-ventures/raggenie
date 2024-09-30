class Formatter:

    def format(data: any, error: any) -> (dict):
        response = {}

        response["main_entity"] = "none"
        response["main_format"] = "general_chat"
        response["role"] = "assistant"
        response["content"] = data
        response["summary"] = data
        response["error"] = error

        return response