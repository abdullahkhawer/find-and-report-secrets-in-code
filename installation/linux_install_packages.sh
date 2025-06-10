#!/bin/bash
set -ex

# install Git, jq, Bash, Make, wget, Python3, pip, Go (Golang)
apk add --no-cache git jq bash make wget python3 py3-pip go
git --version && jq --version && bash --version && make --version && wget --version && python3 --version && pip --version && go version

# install "Atlassian", "World timezone definitions", "Requests" and "Slack" Python libraries
pip install --no-cache-dir atlassian-python-api pytz requests slack-sdk || pip install atlassian-python-api pytz requests slack-sdk --break-system-packages

# install Gitleaks
rm -rf /usr/local/gitleaks && git clone https://github.com/gitleaks/gitleaks.git /usr/local/gitleaks
cd /usr/local/gitleaks
git config --global --add safe.directory /usr/local/gitleaks
git checkout tags/v8.27.0
make build
cd /
export PATH=$PATH:/usr/local/gitleaks
echo -n "Gitleaks v" && gitleaks version

echo "Installation completed successfully."
