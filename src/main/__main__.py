import argparse

def main():
    parser = argparse.ArgumentParser(
        "sparkbadge",
        description="Generate sparklines for your status badge.")
    parser.add_argument(
        "-t",
        "--timeframe",
        default="full",
        help=("The timeframe to create sparklines over, inclusive. "
            " Format (start year to end year) is \"YYYY-YYYY\"."
            " An example input would be \"--timeframe 2017-2020\"."
            " Currently only years are supported."))
    parser.add_argument(
        "-s",
        "--sparkline",
        choices=[
            # Code quality metrics
            "loc", 
            "coverage", 
            "deps", 
            # Project activity metrics
            "commits",
            "issues",
            "pr",
            # CI server metrics
            "wf_runs", 
        ],
        help="The sparkline to use.")
    parser.add_argument(
        "-d",
        "--dir",
        default=".sparkbadge",
        help="The directory to store sparkbadges. Default is .sparkbadge/")
    parser.add_argument(
        "-o",
        "--owner",
        help="The repository owner.")
    parser.add_argument(
        "-r",
        "--repo",
        help="The repository.")

    args = parser.parse_args()

    owner = args.owner
    repo = args.repo
    sparkline = args.sparkline


if __name__ == "__main__":
    main()
