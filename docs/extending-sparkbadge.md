# Extending Sparkbadge

The `spark.yml` file is used to standardize data across multiple sources. It "describes" where the desired metrics can be found in each API. 

- For each source forge, add an authentication token (if necessary) and the base url inside the `config` level.
 
```yaml
config:
    # Add auth token names, located in .env
    github:
        auth_token: null
        base_url: "https://api.github.com/repos"
    gitlab: 
        auth_token: "GITLAB_API_TOKEN"
        base_url: "https://gitlab.com/api/v4/projects"
```

- Next, the location of metrics for each source and metric type are found inside the `metrics` level.

```yaml
metrics:
  # Github metrics
  github:
    # All metrics for github here
    commits:
      id: "sha"
      url_suffix: null 
      params:
        # Describes the location of each parameter
        # "commit.author.date" is parsed as a slice of our json data
        # i.e. "commit.author.date" -> data["commit"]["author"]["date"]
        authored_date: "commit.author.date"
        committed_date: "commit.committer.date"
        verified: "commit.verification.verified"
    issues:
      id: "id"
      url_suffix: null 
      params:
        created_date: "created_at"
        closed_date: "closed_at"
        state: "state"
```

- We can add gitlab as another source forge like so:

```yaml
metrics:
  github:
  # [.....]
  gitlab:
    commits:
      id: "id"
      # Sometimes there is a url suffix, which comes 
      # after user/repo but before metric
      url_suffix: "repository" 
      params:
        authored_date: "authored_date"
        committed_date: "committed_date"
    issues:
      id: "TODO"
      url_suffix: "repository" 
      params:
```
