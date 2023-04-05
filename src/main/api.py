import os
import json
import requests
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

def connect_to_endpoint(url: str, params: Dict[str, Any]) -> Dict:
    """Connect to API endpoint.

    Args:
        url: The base url.
        params: The query params to retrieve.
        
    Returns:
        The json response. 
    """

    # access_token = os.getenv("GITLAB_API_TOKEN")
    # headers = { "Private-Token": access_token }
    # response = requests.get(url, headers, params)
    response = requests.get(url, params)
        
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()
