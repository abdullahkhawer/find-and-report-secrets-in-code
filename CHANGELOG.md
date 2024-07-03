# Changelog

All notable changes to this project will be documented in this file.

## [1.0.1] - 2024-07-03

[1.0.1]: https://github.com/abdullahkhawer/find-and-report-secrets-in-code/releases/tag/v1.0.1

### Bug Fixes

- Update code to use gitleaks v8.18.4 instead of latest and update the READMEs accordingly.

### Miscellaneous Tasks

- Update .gitleaks.toml file to remove unnecessary paths from the 'allowlist'.


## [1.0.0] - 2024-05-07

[1.0.0]: https://github.com/abdullahkhawer/find-and-report-secrets-in-code/releases/tag/v1.0.0

### Features

- [**breaking**] Develop a solution which can be executed on any macOS or Linux system either locally or on a remote server or via a CI/CD pipeline that finds secrets in a git repository using Gitleaks, generates a JSON report based on the findings from Gitleaks by extracting only the relevant information, finds the commit id and commit author for each finding, updates an Atlassian Confluence page with the secrets found based on that generated report and finally sends an alert on Slack.
