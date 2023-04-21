from os import walk
from os.path import join, dirname
from typing import Dict, Callable
from functools import reduce 
import api
import yaml

def recurse_json(data, targets):
    """Recursively scan a nested JSON object for certain keys.

    Args:
        json_obj (dict): The JSON object to scan.
        target_keys (list): A list of strings representing the keys to look for.

    Returns:
        A list of dictionaries, where each dictionary contains information about the
        location of a target key in the JSON object. Each dictionary has the following keys:
        - 'key': The name of the target key.
        - 'value': The value associated with the target key.
        - 'path': A list of strings representing the path to the target key, in the format
          ['root_key', 'child_key', 'grandchild_key', ...].
    """
    results = []
    for key, value in data.items():
        if key in targets:
            results.append({'key': key, 'value': value, 'path': [key]})
        if isinstance(value, dict):
            sub_results = recurse_json(value, targets)
            for sub_result in sub_results:
                sub_result['path'].insert(0, key)
                results.append(sub_result)
    return results


"""Generator that makes a lambda which recurses through a nested dict object.

Args:
    param_dict: The list of 

"""
def make_expand(metric_shortcode:str, entry:dict) -> Callable:
    keys = metric_shortcode.split(".")
    return lambda: reduce(
        lambda d, k: d[k] 
        if isinstance(d, dict) else d,
        keys,
        entry 
    )


def make_params(metric_params:dict, entry:dict):
    return lambda: {
        mt: make_expand(metric_params[mt], entry)()
        for mt in metric_params
    }
            

def sparkbadge(uep, timeframe, metric_type, source, spark_dir, config):

    # Conenct to endpoint and get the payload body
    # url = "some url"
    # params = "some params"
    # payload = api.connect_to_endpoint(url, params)

    # Load the YAML string into a Python object
    with open(spark_dir + "/" + config, 'r') as file:
        cfg = file.read()
    meta = yaml.safe_load(cfg)
    metric = meta["metrics"][source][metric_type] 


    # output = {}
    output = [] 
    for entry in payload:
        inst = {}
        key = entry[metric["id"]]
        params = make_params(metric["params"], entry)()

        output.append({key: params})
    print(f"output is: {output}")


# Github-style response
payload = [
    {
        "sha" : 700,
        "commit": {
            "author": {
                "date": "2023-04-06"
            },
            "committer": {
                "date": "2022-08-17"
            },
            "verification": {
                "verified": True
            }
        }
    },
    {
        "sha" : 1625,
        "commit": {
            "author": {
                "date": "2023-04-06"
            },
            "committer": {
                "date": "2022-08-17"
            },
            "verification": {
                "verified": False 
            }
        }
    },
]

# Gitlab-style response
# payload = [
#     {
#         "id" : 700,
#         "authored_date": "2023-04-06",
#         "committed_date": "2022-08-17",
#     },
#     {
#         "id" : 1625,
#         "authored_date": "2023-04-06",
#         "committed_date": "2022-08-17",
#     },
# ]
        
spark_dir = join(dirname(__file__), "../../.sparkbadge")

sparkbadge("", "", "commits", "github", spark_dir, "spark.yml")
# sparkbadge("", "", "commits", "gitlab", spark_dir, "spark.yml")

"""Example unfolded query
commit["sha"] : {
    "authored_at": commit["commit"]["author"]["date"], 
    "applied_at": commit["commit"]["committer"]["date"],
    "verified" : commit["commit"]["verification"]["verified"]
} 
"""
