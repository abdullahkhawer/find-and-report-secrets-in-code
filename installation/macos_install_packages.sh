#!/bin/bash
set -ex

# install Git, jq, Bash, pip, Python3
brew install git jq bash python python@3
git --version && jq --version && bash --version && pip --version && python3 --version

# install "Atlassian", "World timezone definitions", "Requests" and "Slack" Python libraries
pip install --no-cache-dir atlassian-python-api pytz requests slack-sdk || pip install atlassian-python-api pytz requests slack-sdk --break-system-packages

# install Gitleaks
sudo rm -rf /usr/local/gitleaks && sudo git clone https://github.com/gitleaks/gitleaks.git /usr/local/gitleaks
cd /usr/local/gitleaks
git config --global --add safe.directory /usr/local/gitleaks
sudo git checkout tags/v8.27.0
sudo make build
cd /
export PATH=$PATH:/usr/local/gitleaks
echo -n "Gitleaks v" && gitleaks version

echo "Installation completed successfully."
