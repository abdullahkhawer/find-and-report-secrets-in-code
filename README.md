# Find secrets in code to alert on Slack and track on Confluence

- Founder: Abdullah Khawer (LinkedIn: https://www.linkedin.com/in/abdullah-khawer/)

## Introduction

This repository has a solution to find secrets in a git repository using Gitleaks, generate a JSON report based on the findings from Gitleaks by extracting relevant information only along with finding the commit id and author for each finding and then finally update an Atlassian Confluence page with the secrets found based on that generated report and send alerts on Slack.

❓ Where I can run this?

👉🏻 This solution can be executed on any macOS or Linux system either locally or on a remote server. It can also be executed on a GitLab CI pipeline.

## Usage Notes

### Prerequisites

Following are the prerequisites to be met once before you begin:

- Following packages are installed on your system:
   - In case of Linux, install the following packages using either `./installation/linux_install_packages.sh` script or manually:
      - `git`
      - `jq`
      - `python3-pip`
      - `python3`
      - `make`
      - `wget`
      - `golang`
      - `gitleaks`
      - `atlassian-python-api`
         - Using `pip`
      - `pytz`
         - Using `pip`
   - In case of macOS, install the following packages using either `./installation/macos_install_packages.sh` script or manually:
      - `git`
      - `jq`
      - `python`
      - `python@3`
      - `gitleaks`
      - `atlassian-python-api`
         - Using `pip`
      - `pytz`
         - Using `pip`

### Execution Instructions

Once all the prerequisites are met, set the following environment variables:
   - `PATH_TO_GIT_REPO`
      - Example: `/Users/Abdullah.Khawer/Desktop/myrepo`
   - `CONFLUENCE_SITE`
      - Example: `https://mydomain.atlassian.net`
   - `CONFLUENCE_USER_EMAIL_ID`
      - Example: `myname@mydomain.com`
   - `CONFLUENCE_USER_TOKEN`
      - Example: `__REDACTED__`
   - `CONFLUENCE_PAGE_TITLE`
      - Example: `Review Secrets Detected in GitLab Repositories`
   - `CONFLUENCE_PAGE_SPACE`
      - Example: `docs`

And then simply run the following 2 commands in the correct order:
- `bash gitleaks.sh`
- `python main.py [TIME ZONE] [REPOSITORY NAME] [BRANCH NAME]`
   - Example: `python main.py Europe/Amsterdam appdev/appdev master`
   - Note: Details about supported time zones and their constant names can be found here: [pypi.org > project > pytz > Helpers](https://pypi.org/project/pytz/#:~:text=through%20multiple%20timezones.-,Helpers,-There%20are%20two)

*Notes:*
- *A sample Gitleaks configuration file can be found here if interested in using it: `.gitleaks.toml`*
- *The Atlassian user should have access to the Confluence app, the `View` and `Add` permissions in the space on it and the `Can edit` permission on the page in that space. Also, you need to create an API token as the password won't work.*

### References

A list of useful references can be found below:
- https://gitleaks.io/index.html
- https://docs.gitlab.com/ee/user/application_security/secret_detection/
- https://github.com/gitleaks/gitleaks#configuration
- https://github.com/gitleaks/gitleaks/blob/master/config/gitleaks.toml
- https://docs.python.org/3/
- https://atlassian-python-api.readthedocs.io/
- https://www.gnu.org/savannah-checkouts/gnu/bash/manual/bash.html
- https://docs.gitlab.com/ee/ci/
- https://pypi.org/project/pytz/
- https://git-scm.com/docs/git-blame

##### Any contributions, improvements and suggestions will be highly appreciated. 😊
