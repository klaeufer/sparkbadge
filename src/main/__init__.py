from os.path import join, dirname
from typing import Dict, Callable, List
from functools import reduce 
import api
import yaml

def make_unflatten_keys(metric_shortcode: str, entry: dict) -> Callable:
    """Lambda generator that takes a string and interpolates dict nesting.

    Args:
        metric_shortcode: Param name to slice to get at the value.
        entry: The entry, representing one datapoint in a series of API calls.

    Returns:
        A lambda function, which itself returns a string.

    Examples:
        "commit.author.date" becomes "data[commit][author][date]".
    """
    keys = metric_shortcode.split(".")
    return lambda: reduce(
        lambda d, k: d[k] 
        if isinstance(d, dict) else d,
        keys,
        entry 
    )


def make_entry_params(metric_params: dict, entry: dict):
    """Lambda generator that takes a string and interpolates dict nesting.

    Args:
        metric_params: The list of meta parameters of the metric. 
        entry: The entry, representing one datapoint in a series of API calls.
    """
    return lambda: {
        mt: make_unflatten_keys(metric_params[mt], entry)()
        for mt in metric_params
    }


def make_output(metric: dict, payload):
    """Lambda generator that takes a string and interpolates dict nesting.

    Args:
        metric_shortcode: Param name to slice to get at the value.
        entry: The entry, representing one datapoint in a series of API calls.
    """
    metric_id = metric["id"]
    metric_params = metric["params"]
    # return lambda: [
    #     { entry[metric_id]: make_entry_params(metric_params, entry)() }
    #     for entry in payload
    # ]

    locate_params = lambda metric_params, entry: {
        mt: make_unflatten_keys(metric_params[mt], entry)()
        for mt in metric_params
    } 

    return lambda: [
        { entry[metric_id]: locate_params(metric_params, entry) }
        for entry in payload
    ]


def build_url(meta: dict, 
              source: str, 
              metric_type: str, 
              uep: str) -> str:
    """Constructs a url in prep for api calls.

    Args:
        meta:
        source:
        metric_type:
        uep:

    Returns:
        The full url to be used in a HTTP GET request.

    Examples:
        "https://api.github.com/repos/facebook/react/commits"
        "https://gitlab.com/api/v4/projects/gitlab-org%2Fgitlab/repository/commits"
    """
    # Build url
    base_url = meta["config"][source]["base_url"]
    url = f"{base_url}/{uep}/"
    # Add any suffixes if applicable
    url_suffix = meta["metrics"][source][metric_type]["url_suffix"]
    if url_suffix:
        url += url_suffix + "/"
    # Append metric type
    url += metric_type
    return url


def sparkbadge(uep, timeframe, metric_type, source, spark_dir, config):

    # Load the spark.yml config 
    with open(spark_dir + "/" + config, 'r') as file:
        cfg = file.read()
    meta = yaml.safe_load(cfg)
    
    # Load info about the metric 
    metric = meta["metrics"][source][metric_type] 

    # Construct url and get auth token (if needed)
    url = build_url(meta, source, metric_type, uep)
    auth_token = meta["config"][source]["auth_token"]

    # HTTP GET request
    payload = api.connect_to_endpoint(url, {}, auth_token)

    # Parse and standardize payload
    output = make_output(metric, payload)()

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

### COMMITS
sparkbadge("facebook/react", "", "commits", "github", spark_dir, "spark.yml")
# sparkbadge("", "", "commits", "gitlab", spark_dir, "spark.yml")

### ISSUES
# sparkbadge("", "", "issues", "github", spark_dir, "spark.yml")

### RUNS
# sparkbadge("", "", "runs", "github", spark_dir, "spark.yml")
