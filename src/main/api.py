import os
from os.path import join, dirname
import json
import requests
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

def get_payload(url: str, params: Dict[str, Any]) -> Dict:
    """
    """

def read_cfg(spark_dir: str):
    """Read from the config file.
    """
    cfg = join(dirname(__file__), f"{spark_dir}/config.json")


def connect_to_endpoint(url: str, params: Dict[str, Any]) -> Dict:
    """Connect to API endpoint.

    Args:
        url: The base url.
        params: The query params to retrieve.
        
    Returns:
        The json response. 
    """

    access_token = os.getenv("GITLAB_API_TOKEN")
    headers = { "Authorization": f"Bearer {access_token}" }
    # response = requests.get(url, headers, params)
    response = requests.get(url, headers=headers)
    # response = requests.get(url)
        
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()
