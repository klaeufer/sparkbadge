from os.path import join, dirname
from typing import Dict 
from functools import reduce
import api
import yaml

"""
1. Detect source forge (github or gitlab)
2. Detect any API tokens
3. Read json hierarchical structure from sparkbadge.yml
"""

def recurse_json(data, targets):
    """
    Recursively scan a nested JSON object for certain keys.

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


def sparkbadge(uep, timeframe, metric_type, source, spark_dir, config):

    # TODO: Load config

    # TODO: Parse forge

    # TODO: Do some stuff to format input...

    # Conenct to endpoint and get the payload body
    # url = "some url"
    # params = "some params"
    # payload = api.connect_to_endpoint(url, params)

    # Load the YAML string into a Python object
    with open(spark_dir + "/" + config, 'r') as file:
        cfg = file.read()
    meta = yaml.safe_load(cfg)
    metric = meta["output"][source][metric_type] 

    author_test = metric["params"]["authored_date"]
    print(author_test)
    # Get the nested dictionary key from the string
    params = author_test.split(".")
    print(params)

    # Create a nested dictionary access from the list of keys
    # unpacked = lambda keys: reduce(
    #     lambda nested_dict, key: nested_dict.setdefault(key, {}),
    #     keys,
    #     {}
    # )
    # unpacked_params = unpacked(params)
    # print(unpacked_params)

    data = {
        "commit": {
            "author": {
                "date": "2023-04-06"
            }
        }
    }

    # result = reduce(lambda d, k: d[k], params, data)
    result = reduce(lambda d, k: d[k] 
        if isinstance(d, dict) 
        else d, params, data
    )
    print(result)

    # result = data
    # for key in keys:
    #     result = result[key]
    # print(result)



spark_dir = join(dirname(__file__), "../../.sparkbadge")

sparkbadge("", "", "commits", "github", spark_dir, "spark.yml")

"""Example unfolded query
commit["sha"] : {
    "authored_at": commit["commit"]["author"]["date"], 
    "applied_at": commit["commit"]["committer"]["date"],
    "verified" : commit["commit"]["verification"]["verified"]
} 
"""


    # Create a nested dictionary access from the list of keys
    # result = nested_dict = {}
    # for key in keys:
    #     nested_dict[key] = {}
    #     nested_dict = nested_dict[key]

    # commit_data = lambda commits: {
        # str(commit["sha"]) : {
        #     "authored_at": commit["commit"]["author"]["date"], 
        #     "applied_at": commit["commit"]["committer"]["date"],
        #     "verified" : commit["commit"]["verification"]["verified"]
        # } 
    #     for commit in commits 
    # }

