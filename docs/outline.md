# Notes

## Protocol Layers

1) Repo hosting (GitHub, GitLab, bitbucket, sourcehut, custom?)
2) CI servers (Actions, GitLab CI, Circle, Travis, etc.
3) App/Protocol (Handles the SVG creation)

## Outline

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

## CLI Usage

```
usage: sparkbadge [-h] [-o OWNER] [-r REPO]
                  [-s {loc,coverage,deps,commits,issues,pr,wf_runs}] [-d DIR]

Generate sparklines for your status badge.

options:
  -h, --help            show this help message and exit
  -o OWNER, --owner OWNER
                        The repository owner.
  -r REPO, --repo REPO  The repository.
  -s {loc,coverage,deps,commits,issues,pr,wf_runs}, --sparkline {loc,coverage,deps,commits,issues,pr,wf_runs}
                        The sparkline to use.
  -d DIR, --dir DIR     The directory to store sparkbadges. Default is
                        .sparkbadge/
```

- Additional considerations:
    - Color customization
    - Separate `-s` flag into chart style and data source for increased flexibility

## Diagram

- Here's proof-of-concept diagram of how the project could be structured. I figured that broadly speaking, the metrics we've discussed can be broken down into 3 categories - code quality, project activity, and CI/CD. 
- I tried to break it down by priority, but if we go with this hierarchical structure, the first place to start might be to add one feature from each of the 3 categories.
 
![Diagram](diagram.svg)
