# CI_Server Notes

## General Notes

- Use this to check github rate limits:
```sh
curl -H "Accept: application/vnd.github.v3+json" \
         https://api.github.com/rate_limit
```
## Metrics to track

### Worflow Pipelines

- GH Actions:
    - Name: list wf runs
    - URL: https://api.github.com/repos/{owner}/{repo}/actions/runs 
    - Dox: https://docs.github.com/en/rest/actions/workflow-runs?apiVersion=2022-11-28#list-workflow-runs-for-a-repository
- Gitlab:
    - Name: Pipelines
    - URL: https://gitlab.com/api/v4/projects/{project_id}/pipelines
    - Dox: https://docs.gitlab.com/ee/api/pipelines.html 
