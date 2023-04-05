import typing
import api

def gitlab_jobs():
    """
    Rate Limit: 600 calls/minute
    https://gitlab.com/api/v4/projects/{project_id}/jobs
    https://gitlab.com/gitlab-org/gitlab
    """
    url = "https://gitlab.com/api/v4/projects/gitlab-org%2Fgitlab/jobs"
    payload = api.connect_to_endpoint(url=url, params={})

    print(payload)

    # for iid in payload["iid"]:
    #     print(iid)
