import typing
from metrics import Metrics


def gitlab_jobs():
    """
    Rate Limit: 600 calls/minute
    https://gitlab.com/api/v4/projects/{project_id}/jobs
    https://gitlab.com/gitlab-org/gitlab
    """
    url = "https://gitlab.com/api/v4/projects/gitlab-org%2Fgitlab/jobs"
    mt = Metrics("", "", {})
    payload = mt.connect_to_endpoint(url, {})

    print(payload)

    # for iid in payload["iid"]:
    #     print(iid)

def github_jobs():
    """

    curl -H "Accept: application/vnd.github.v3+json" \
    https://api.github.com/rate_limit
    """

gitlab_jobs()
