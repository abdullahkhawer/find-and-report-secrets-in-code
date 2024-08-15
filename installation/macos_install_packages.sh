#!/bin/bash
set -ex

# install Git, jq, Bash, pip, Python3
brew install git jq bash python python@3
git --version && jq --version && bash --version && pip --version && python3 --version

# install "Python Atlassian REST API Wrapper", "World timezone definitions, modern and historical" and "Requests" Python libraries
pip install --no-cache-dir atlassian-python-api pytz requests || pip install atlassian-python-api pytz requests --break-system-packages

# install Gitleaks
sudo rm -rf /usr/local/gitleaks && sudo git clone https://github.com/gitleaks/gitleaks.git /usr/local/gitleaks
cd /usr/local/gitleaks
git config --global --add safe.directory /usr/local/gitleaks
sudo git checkout tags/v8.18.4
sudo make build
cd /
export PATH=$PATH:/usr/local/gitleaks
echo -n "gitleaks " && gitleaks version

echo "Installation completed successfully."
