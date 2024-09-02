# Quick Reference

-	**Maintained by**:
	[Abdullah Khawer - LinkedIn](https://www.linkedin.com/in/abdullah-khawer)

-	**Maintained at**:
	[find-and-report-secrets-in-code - GitHub](https://github.com/abdullahkhawer/find-and-report-secrets-in-code)

-	**Where to file issues**:
	[https://github.com/abdullahkhawer/find-and-report-secrets-in-code/issues](https://github.com/abdullahkhawer/find-and-report-secrets-in-code/issues)

# Supported tags and respective `Dockerfile` links

-	[`1.3.0`, `latest`](https://github.com/abdullahkhawer/find-and-report-secrets-in-code/blob/v1.3.0/docker/Dockerfile)

# Find and Report Secrets in Code

# Introduction

This repository has a Docker image that finds secrets in a git repository using Gitleaks, generates a JSON report based on the findings from Gitleaks by extracting only the relevant information, finds the commit id and commit author for each finding, updates an Atlassian Confluence page with the secrets found based on that generated report and finally sends an alert on Slack.

❓ Where I can run this?

This solution can be executed on any macOS or Linux system either locally or on a remote server. It can also be executed on a CI/CD tool like on GitHub Actions, GitLab CI, etc, in a pipeline.

Below you can find an example of the JSON report generated:

```json
[
  {
    "Description": "Detected a Generic API Key, potentially exposing access to various services and sensitive operations.",
    "File": "scripts/main.py",
    "Line No.": "11",
    "Link": "https://gitlab.com/my-projects/my-repo/-/blob/master/scripts/main.py#L11",
    "Secret Type": "generic-api-key",
    "Commit": "__REDACTED__",
    "Author": "__REDACTED__"
  },
  {
    "Description": "Identified a HashiCorp Terraform password field, risking unauthorized infrastructure configuration and security breaches.",
    "File": "configurations/main.tf",
    "Line No.": "6",
    "Link": "https://gitlab.com/my-projects/my-repo/-/blob/master/configurations/main.tf#L6",
    "Secret Type": "hashicorp-tf-password",
    "Commit": "__REDACTED__",
    "Author": "__REDACTED__"
  }
  ...
]
```

Note: In the actual execution, you will see the actual values instead of `__REDACTED__` values.

Below you can find an example of the Slack notification messages in case of both no secrets found and 1 or more secrets found:

![image](https://github.com/user-attachments/assets/0dfa93a5-bcc4-4370-8b25-1e30c783f059)

# Usage Notes

## Manually on a Local or Remote Server

### Execution Instructions

Set the following environment variables:
   - `LOCAL_PATH_TO_GIT_REPO`
      - Description: Local path to the Git repository.
      - Example: `/Users/Abdullah.Khawer/Desktop/my-projects/my-repo`
      - Requirement: REQUIRED
   - `REMOTE_PATH_TO_GIT_REPO`
      - Description: Remote path to the Git repository.
      - Example: `https://gitlab.com/my-projects/my-repo`
      - Requirement: REQUIRED
   - `BRANCH_NAME`
      - Description: Name of the branch in the Git repository against which secrets detection tool will be executed.
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

And then simply run the following 4 commands:
- `docker run --platform linux/amd64 -it -e LOCAL_PATH_TO_GIT_REPO=$LOCAL_PATH_TO_GIT_REPO -e REMOTE_PATH_TO_GIT_REPO=$REMOTE_PATH_TO_GIT_REPO -e BRANCH_NAME=$BRANCH_NAME -e CONFLUENCE_ENABLED=$CONFLUENCE_ENABLED -e CONFLUENCE_SITE=$CONFLUENCE_SITE -e CONFLUENCE_USER_EMAIL_ID=$CONFLUENCE_USER_EMAIL_ID -e CONFLUENCE_USER_TOKEN=$CONFLUENCE_USER_TOKEN -e CONFLUENCE_PAGE_TITLE=$CONFLUENCE_PAGE_TITLE -e CONFLUENCE_PAGE_SPACE=$CONFLUENCE_PAGE_SPACE -e SLACK_ENABLED=$SLACK_ENABLED -e SLACK_WEBHOOK_URL=$SLACK_WEBHOOK_URL -v $LOCAL_PATH_TO_GIT_REPO:$LOCAL_PATH_TO_GIT_REPO abdullahkhawer/find-and-report-secrets-in-code:latest`
- `export PATH=$PATH:/usr/local/gitleaks`
- `bash /find-and-report-secrets-in-code/gitleaks.sh`
- `python3 /find-and-report-secrets-in-code/main.py TIME_ZONE REPOSITORY_NAME BRANCH_NAME [JSON_REPORT_URL]`
   - Example: `python3 /find-and-report-secrets-in-code/main.py Europe/Amsterdam my-projects/my-repo master`
   - Note: Details about supported time zones and their constant names can be found here: [pypi.org > project > pytz > Helpers](https://pypi.org/project/pytz/#:~:text=through%20multiple%20timezones.-,Helpers,-There%20are%20two)

## Automatically via a CI/CD Pipeline

### GitHub Actions - Setup Instructions

In order to run it on any GitHub repository, add the following in the `.github-workflow.yml` file under the `.github/workflows/` directory in the repository:

```
name: find-and-report-secrets-in-code

on:
  push:
    branches:
      - master

jobs:
  find-and-report-secrets-in-code:
    uses: abdullahkhawer/find-and-report-secrets-in-code/.github/workflows/.github-workflow.yml@master
    with:
      CONFLUENCE_ENABLED: "1"
      CONFLUENCE_PAGE_TITLE: ${{ vars.CONFLUENCE_PAGE_TITLE }}
      CONFLUENCE_PAGE_SPACE: ${{ vars.CONFLUENCE_PAGE_SPACE }}
      SLACK_ENABLED: "1"
    secrets:
      CONFLUENCE_SITE: ${{ secrets.CONFLUENCE_SITE }}
      CONFLUENCE_USER_EMAIL_ID: ${{ secrets.CONFLUENCE_USER_EMAIL_ID }}
      CONFLUENCE_USER_TOKEN: ${{ secrets.CONFLUENCE_USER_TOKEN }}
      SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

In the `on` section, you specify events can cause the workflow to run. In the above example, the job is only allowed to execute if something is pushed to the `master` branch.

The variables referred using `$` are supposed to be created on the repository under `Repository secrets` and `Repository variables` depending on the type of variable from here: `Settings > Security > Secrets and variables > Actions`.

### GitLab CI - Setup Instructions

In order to run it on any GitLab repository, add the following in the `.gitlab-ci.yml` file on root level in the repository:

```
include:
  - remote: 'https://raw.githubusercontent.com/abdullahkhawer/find-and-report-secrets-in-code/master/.gitlab/.gitlab-ci.yml'

stages:
  - scan

find-and-report-secrets-in-code:
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

The variables referred using `$` are supposed to be created on the repository under `CI/CD Variables` from here: `Settings > CI/CD > Variables`.

## Docker Image Details

The Docker image used is built using the Dockerfile that is present in this repository here: [Dockerfile](https://github.com/abdullahkhawer/find-and-report-secrets-in-code/tree/master/docker)

Following build command is used on the root level in the GitHub repository: `docker buildx build --platform linux/amd64 -t "abdullahkhawer/find-and-report-secrets-in-code:latest" --no-cache -f ./docker/Dockerfile .`

## Notes

- A sample Gitleaks configuration file can be found here if interested in using it: `https://github.com/abdullahkhawer/find-and-report-secrets-in-code/blob/master/.gitleaks.toml`
- The Atlassian user should have access to the Confluence app, the `View` and `Add` permissions in the space on it and the `Can edit` permission on the page in that space. Also, you need to create an API token as the password won't work.

For more details, check out the following repository on GitHub: https://github.com/abdullahkhawer/find-and-report-secrets-in-code/

## License

This project is licensed under the Apache License - see the [LICENSE](https://github.com/abdullahkhawer/find-and-report-secrets-in-code/blob/master/docker/LICENSE) file for details.

#### Any contributions, improvements and suggestions will be highly appreciated. 😊
