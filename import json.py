import json

def parse_error_message(error_string):
    """Parses the error message from the given string.

    Args:
        error_string (str): The error string to parse.

    Returns:
        str: The extracted error message.
    """
    try:
        # Assuming the error string is a JSON object
        error_dict = json.loads(error_string)
        # Navigate through the dictionary to extract the message
        message = error_dict['error']['message']
        return message
    except (json.JSONDecodeError, KeyError):
        # Handle cases where the string is not JSON or the structure is different
        return "Failed to parse error message."

# Example usage
error_string = "Error code: 400 - {'error': {'code': 'content_policy_violation', 'message': 'Your request was rejected as a result of our safety system. Your prompt may contain text that is not allowed by our safety system.', 'param': None, 'type': 'invalid_request_error'}}"
error_message = parse_error_message(error_string)
print(error_message)