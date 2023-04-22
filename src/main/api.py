import os
from os.path import join, dirname
import requests
from typing import Dict, Any, Union
from dotenv import load_dotenv

load_dotenv()

def read_cfg(spark_dir: str):
    """Read from the config file.
    """
    cfg = join(dirname(__file__), f"{spark_dir}/config.json")


def connect_to_endpoint(url: str, 
                        params: Dict[str, Any], 
                        auth_token: Union[str, None]) -> Dict:
    """Connect to API endpoint.

    Args:
        url: The base url.
        params: The query params to retrieve.
        auth_token: An optional authentication token.
        
    Returns:
        The json response. 
    """
    response = {}
    if auth_token:
        access_token = os.getenv(auth_token)
        headers = { "Authorization": f"Bearer {access_token}" }
        response = requests.get(url=url, headers=headers, params=params)
    else:
        response = requests.get(url=url, params=params)
        
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()
