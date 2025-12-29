import json

def json_response(payload: str) -> str:
    """
    Helper function to return a JSON response for the middleware.
    """
    return json.dumps(payload)