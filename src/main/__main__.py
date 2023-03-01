import argparse

def main():
    parser = argparse.ArgumentParser(
        'sparkbadge',
        description='Generate sparklines for your status badge.')
    parser.add_argument(
        '-o',
        '--owner',
        help='The repository owner.')
    parser.add_argument(
        '-r',
        '--repo',
        help='The repository.')
    parser.add_argument(
        '-s',
        '--sparkline',
        choices=[
            # Code quality metrics
            'loc', 
            'coverage', 
            'deps', 
            # Project activity metrics
            'commits',
            'issues',
            'pr',
            # CI server metrics
            'wf_runs', 
        ],
        help='The sparkline to use.')
    parser.add_argument(
        '-d',
        '--dir',
        default=".sparkbadge",
        help='The directory to store sparkbadges. Default is .sparkbadge/')

    args = parser.parse_args()

    owner = args.owner
    repo = args.repo
    sparkline = args.sparkline


if __name__ == "__main__":
    main()
