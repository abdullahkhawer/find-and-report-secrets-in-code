# Find and Report Secrets in Code

- Founder: Abdullah Khawer (LinkedIn: https://www.linkedin.com/in/abdullah-khawer/)

# Introduction

A security solution that finds secrets in a git repository using Gitleaks, generates a JSON report based on the findings from Gitleaks by extracting only the relevant information, finds the commit id and commit author for each finding, updates an Atlassian Confluence page with the secrets found based on that generated report and finally sends an alert on Slack.

❓ Where I can run this?

👉🏻 This solution can be executed on any macOS or Linux system either locally or on a remote server. It can also be executed on a CI/CD pipeline.

Below you can find an example of the JSON report generated:

```json
[
  {
    "Description": "Identified a HashiCorp Terraform password field, risking unauthorized infrastructure configuration and security breaches.",
    "File": "./code/main.py",
    "Line No.": "11",
    "Secret Type": "hashicorp-tf-password",
    "Commit": "__REDACTED__",
    "Author": "__REDACTED__"
  },
  {
    "Description": "Identified a HashiCorp Terraform password field, risking unauthorized infrastructure configuration and security breaches.",
    "File": "./code/main.conf",
    "Line No.": "30",
    "Secret Type": "hashicorp-tf-password",
    "Commit": "__REDACTED__",
    "Author": "__REDACTED__"
  }
]
```

Note: In the actual execution, you will see the actual values instead of `__REDACTED__` values.

Below you can find an example of the Slack notification:

![image](https://github.com/abdullahkhawer/find-and-report-secrets-in-code/assets/27900716/fc798318-7373-4437-a205-4d71065fb2f7)

# Usage Notes

## Manually on a Local or Remote Server

### Prerequisites

Following are the prerequisites to be met once before you begin:

- Following packages should be installed on your system:
   - In case of Linux, install the following packages by running either `./installation/linux_install_packages.sh` command or by installing them manually:
      - `git`
      - `jq`
      - `bash`
      - `make`
      - `wget`
      - `python3`
      - `py3-pip`
      - `golang`
      - `gitleaks`
      - `atlassian-python-api`
         - Using `pip`
      - `pytz`
         - Using `pip`
      - `requests`
         - Using `pip`
   - In case of macOS, install the following packages by running either `./installation/macos_install_packages.sh` command or by installing them manually:
      - `git`
      - `jq`
      - `bash`
      - `python`
      - `python@3`
      - `gitleaks`
      - `atlassian-python-api`
         - Using `pip`
      - `pytz`
         - Using `pip`
      - `requests`
         - Using `pip`

### Execution Instructions

Once all the prerequisites are met, set the following environment variables:
   - `PATH_TO_GIT_REPO`
      - Description: To keep the size of the git repository to be cloned lower to make the job faster.
      - Example: `/Users/Abdullah.Khawer/Desktop/myrepo`
      - Requirement: REQUIRED
   - `CONFLUENCE_ENABLED`
      - Description: Whether to enable reporting on Atlassian Confluence or not.
      - Example: `1`
      - Requirement: REQUIRED
      - Possible Values: `1` or `0`
   - `CONFLUENCE_SITE`
      - Description: Atlassian Confluence host link.
      - Example: `https://mydomain.atlassian.net`
      - Requirement: REQUIRED (if `CONFLUENCE_ENABLED` is set to `1`)
   - `CONFLUENCE_USER_EMAIL_ID`
      - Description: Atlassian Confluence user email ID.
      - Example: `myname@mydomain.com`
      - Requirement: REQUIRED (if `CONFLUENCE_ENABLED` is set to `1`)
   - `CONFLUENCE_USER_TOKEN`
      - Description: Atlassian Confluence user token.
      - Requirement: REQUIRED (if `CONFLUENCE_ENABLED` is set to `1`)
   - `CONFLUENCE_PAGE_TITLE`
      - Description: Atlassian Confluence page title.
      - Example: `Secrets Detected in the Git Repositories`
      - Requirement: REQUIRED (if `CONFLUENCE_ENABLED` is set to `1`)
   - `CONFLUENCE_PAGE_SPACE`
      - Description: Atlassian Confluence page space.
      - Example: `docs`
      - Requirement: REQUIRED (if `CONFLUENCE_ENABLED` is set to `1`)
   - `SLACK_ENABLED`
      - Description: Whether to enable notifications on Slack or not.
      - Example: `1`
      - Requirement: REQUIRED
      - Possible Values: `1` or `0`
   - `SLACK_WEBHOOK_URL`
      - Description: Slack Webhook URL.
      - Example: `[https://mydomain.atlassian.net](https://hooks.slack.com/services/__REDACTED__/__REDACTED__/__REDACTED__)`
      - Requirement: REQUIRED (if `SLACK_ENABLED` is set to `1`)

And then simply run the following 3 commands in the correct order:
- `bash gitleaks.sh`
- `python3 main.py TIME_ZONE REPOSITORY_NAME BRANCH_NAME [JSON_REPORT_URL]`
   - Example: `python3 main.py Europe/Amsterdam myproj/myrepo master`
   - Note: Details about supported time zones and their constant names can be found here: [pypi.org > project > pytz > Helpers](https://pypi.org/project/pytz/#:~:text=through%20multiple%20timezones.-,Helpers,-There%20are%20two)

## Automatically via CI/CD Pipeline

### Setup Instructions

In order to run it on any GitLab repository, add the following in the `.gitlab-ci.yml` file that is in the repository:

```
include:
  - remote: 'https://raw.githubusercontent.com/abdullahkhawer/find-and-report-secrets-in-code/master/ci/.gitlab-ci.yml'

stages:
  - scan

secrets_detection:
  stage: scan
  extends:
    - .find-secrets:scan
  variables:
    CONFLUENCE_ENABLED: "1"
    CONFLUENCE_SITE: $CONFLUENCE_SITE
    CONFLUENCE_USER_EMAIL_ID: $CONFLUENCE_USER_EMAIL_ID
    CONFLUENCE_USER_TOKEN: $CONFLUENCE_USER_TOKEN
    CONFLUENCE_PAGE_TITLE: $CONFLUENCE_PAGE_TITLE
    CONFLUENCE_PAGE_SPACE: $CONFLUENCE_PAGE_SPACE
    SLACK_ENABLED: "1"
    SLACK_WEBHOOK_URL: $SLACK_WEBHOOK_URL
  retry:
    max: 2
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule" && $CI_COMMIT_REF_NAME == "master"
      when: always
      allow_failure: false
```

In the `rules` section, you specify rules for execution as `if` conditions. In the above example, the job is only allowed to execute if it is a scheduled job for the `master` branch.

The variables referred using `$` are supposed to be created on the repository under `CI/CD Settings` page.

The image used in this GitLab CI job is built using the Dockerfile that is present in this repository here: https://github.com/abdullahkhawer/find-and-report-secrets-in-code/tree/master/docker

The image used is publicly available here: https://hub.docker.com/r/abdullahkhawer/find-and-report-secrets-in-code/

## Notes

- A sample Gitleaks configuration file can be found here if interested in using it: `.gitleaks.toml`
- The Atlassian user should have access to the Confluence app, the `View` and `Add` permissions in the space on it and the `Can edit` permission on the page in that space. Also, you need to create an API token as the password won't work.

#### Any contributions, improvements and suggestions will be highly appreciated. 😊
