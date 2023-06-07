"""Creates a longitudinal status sparkline as an SVG.

This package creates a longitudinal status graphic, 
which can then be added to a github-style badge using pybadges or shields.io.
"""

from os.path import join, dirname
from typing import Callable
from functools import reduce 
import yaml

from sparkbadge import api


def make_unflatten_keys(metric_shortcode: str, entry: dict) -> Callable:
    """Lambda generator that takes a string and interpolates dict nesting.

    Args:
        metric_shortcode: Param name to slice to get at the value.
        entry: The entry, representing one datapoint in a series of API calls.

    Returns:
        A lambda function, which itself returns a string.

    Examples:
        "commit.author.date" becomes VALUE of "data[commit][author][date]".
    """
    keys = metric_shortcode.split(".")
    return lambda: reduce(
        lambda d, k: d[k] 
        if isinstance(d, dict) else d,
        keys,
        entry 
    )


def make_output(metric: dict, payload):
    """Lambda generator that takes a string and interpolates dict nesting.

    Args:
        metric_shortcode: Param name to slice to get at the value.
        entry: The entry, representing one datapoint in a series of API calls.
    """
    metric_id = metric["id"]
    metric_params = metric["params"]

    # Recurse through params and unflatten the values
    locate_params = lambda metric_params, entry: {
        mt: make_unflatten_keys(metric_params[mt], entry)()
        for mt in metric_params
    } 

    # Process each row of data
    return lambda: [
        { entry[metric_id]: locate_params(metric_params, entry) }
        for entry in payload
    ]


def build_url(meta: dict, 
              source: str, 
              metric_type: str, 
              uep: str) -> str:
    """Constructs a URL in prep for API calls.

    Args:
        meta: The config details and location of metrics.
        source: The source forge.
        metric_type: The metric to use.
        uep: The URL-encoded path.

    Returns:
        The full URL to be used in a HTTP GET request.

    Examples:
        "https://api.github.com/repos/facebook/react/commits"
        "https://gitlab.com/api/v4/projects/gitlab-org%2Fgitlab/repository/commits"
    """
    base_url = meta["config"][source]["base_url"]
    url = f"{base_url}/{uep}/"

    # Add any suffixes if applicable
    url_suffix = meta["metrics"][source][metric_type]["url_suffix"]
    if url_suffix:
        url += url_suffix + "/"

    # Append metric type
    url += metric_type
    return url


def sparkbadge(uep: str, 
               timeframe: str, 
               metric_type: str, 
               source: str, 
               spark_dir: str):
    """Creates a longitudinal sparkline.
    
    Args:
        uep: The ID or URL-encoded path of the project.
        timeframe: The timeframe to create sparklines over.
            See 'python -m sparkbadge' --help for more.
        metric_type:
        source: The source forge (i.e. github or gitlab).
        spark_dir: Directory to store sparkbadges. Default is .sparkbadge/
    """
    
    # Load the spark.yml config 
    with open(spark_dir + "/spark.yml" , 'r') as file:
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


spark_dir = join(dirname(__file__), "../.sparkbadge")

sparkbadge("facebook/react", "", "commits", "github", spark_dir)
# sparkbadge("", "", "commits", "gitlab", spark_dir,)
