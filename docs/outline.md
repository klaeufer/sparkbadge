# Notes

## Protocol Layers

1) Repo hosting (GitHub, GitLab, bitbucket, sourcehut, custom?)
2) CI servers (Actions, GitLab CI, Circle, Travis, etc.
3) App/Protocol (Handles the SVG creation)

## CLI Usage

```
usage: sparkbadge [-h] [-o OWNER] [-r REPO]
                  [-s {histogram,bargraph,scatterplot}]
                  [-m {loc,coverage,deps,commits,issues,pr,wf_runs}] [-d DIR]

Generate sparklines for your status badge.

options:
  -h, --help            show this help message and exit
  -o OWNER, --owner OWNER
                        The repository owner.
  -r REPO, --repo REPO  The repository.
  -s {histogram,bargraph,scatterplot}, --sparkline {histogram,bargraph,scatterplot}
                        The sparkline to use.
  -m {loc,coverage,deps,commits,issues,pr,wf_runs}, --metrics {loc,coverage,deps,commits,issues,pr,wf_runs}
                        The metrics to create.
  -d DIR, --dir DIR     The directory to store sparkbadges. Default is
                        .sparkbadge/
```

- Protocol spec:
    - Our API should be able to handle the above layers interchangeably 
    - Should allow for easy creation of new longitudinal metrics
    - Split into 3 areas:
        - Code quality 
        - Project activity 
        - CI server metrics
    - Hosted **on** a CI service like gh actions, or on cloud
- Hosting:
    - On gh actions, add a workflow to run sparkbadge script triggered by a commit/some other action
    - Cache badges in `.sparkbadge/` 
    - Look into hosting solutions (AWS, Azure, fly.io)
- Goals:
    - Add to `pip`?

## Diagram

![Diagram](diagram.svg)
