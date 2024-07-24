# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2024-07-24

[1.1.0]: https://github.com/abdullahkhawer/find-and-report-secrets-in-code/releases/tag/v1.1.0

### 🚀 Features

- Update shell script to prepare and add URL for each finding in the JSON report.
- Update python script to improve logging, comments, pylint score from 1.44 to 9.25/10 by refactoring code, HTML content template to add link to the file reference where secret is detected and Slack notification message along with its format in case of both no secrets found and 1 or more secrets found.

### 📚 Documentation

- Update READMEs to add 2 new ENVs, add 1 new JSON field and fix some existing commands and descriptions mentioned.

### ⚙️ Miscellaneous Tasks

- Remove unnecessary file from .gitignore.
- Add 2 new variables and use image 1.1.0
- Update version to v1.1.0

## [1.0.1] - 2024-07-03

[1.0.1]: https://github.com/abdullahkhawer/find-and-report-secrets-in-code/releases/tag/v1.0.1

### 🐛 Bug Fixes

- Update code to use gitleaks v8.18.4 instead of latest and update the READMEs accordingly.
- Remove sudo as it wasn't required in this script.

### ⚙️ Miscellaneous Tasks

- Update .gitleaks.toml file to remove unnecessary paths from the 'allowlist'.
- Update print command to fix a word.


## [1.0.0] - 2024-06-06

[1.0.0]: https://github.com/abdullahkhawer/find-and-report-secrets-in-code/releases/tag/v1.0.0

### 🚀 Features

- [**breaking**] Develop a solution which can be executed on any macOS or Linux system either locally or on a remote server or via a CI/CD pipeline that finds secrets in a git repository using Gitleaks, generates a JSON report based on the findings from Gitleaks by extracting only the relevant information, finds the commit id and commit author for each finding, updates an Atlassian Confluence page with the secrets found based on that generated report and finally sends an alert on Slack.
