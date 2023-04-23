"""Output a longitudinal status sparkline as an SVG.

For more information, run:
$ python3 -m sparkbadge --help
"""

import argparse
import sparkbadge
from os.path import join, dirname


def main():
    parser = argparse.ArgumentParser(
        "sparkbadge",
        description="Generate sparklines for your status badge.")
    parser.add_argument(
        "-u",
        "--uep",
        help="The ID or URL-encoded path of the project.")
    parser.add_argument(
        "-t",
        "--timeframe",
        default="full",
        help=("The timeframe to create sparklines over, inclusive. "
            " Format (start year to end year) is \"YYYY-YYYY\"."
            " An example input would be \"--timeframe 2017-2020\"."
            " Currently only years are supported."))
    parser.add_argument(
        "-m",
        "--metrics",
        choices=[
            # Code quality metrics
            #TODO: "loc", 
            #TODO:  "coverage", 
            #TODO:  "deps", 

            # Project activity metrics
            "commits",
            "issues",
            #TODO: "pr",

            # CI server metrics
            #TODO: "workflow_runs", 
        ],
        help="The sparkline to use.")
    parser.add_argument(
        "-s",
        "--source",
        default="github",
        help="The source forge (i.e. github or gitlab).")
    parser.add_argument(
        "-d",
        "--dir",
        default=".sparkbadge",
        help="The directory to store sparkbadges. Default is .sparkbadge/")

    args = parser.parse_args()

    uep = args.uep
    timeframe = args.timeframe
    metrics = args.metrics
    source = args.source
    spark_dir = (args.dir 
                if parser.get_default("dir") 
                else join(dirname(__file__), "../.sparkbadge"))

    sparkbadge.sparkbadge(uep, 
                          timeframe, 
                          metrics, 
                          source, 
                          spark_dir)


if __name__ == "__main__":
    main()
