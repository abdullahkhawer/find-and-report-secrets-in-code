#!/bin/bash
set -ex

# install Git, jq, Bash, pip, Python3, Gitleaks
brew install git jq bash python python@3 gitleaks
git --version && jq --version && bash --version && pip --version && python3 --version && echo -n "gitleaks " && gitleaks version

# install "Python Atlassian REST API Wrapper", "World timezone definitions, modern and historical" and "Requests" Python libraries
pip install atlassian-python-api pytz requests || pip install atlassian-python-api pytz requests --break-system-packages

echo "Installation completed successfully."
