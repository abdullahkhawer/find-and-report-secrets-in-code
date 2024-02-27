#!/bin/bash
set -ex

# update package lists
apk update

# install Git, jq, Bash, Make, wget, Python3, pip, Go (Golang)
apk add git jq bash make wget python3 py3-pip go
git --version && jq --version && bash --version && make --version && wget --version && python3 --version && pip --version && go version

# install "Python Atlassian REST API Wrapper", "World timezone definitions, modern and historical" and "Requests" Python libraries
pip install atlassian-python-api pytz requests --break-system-packages

# install Gitleaks
rm -rf /usr/local/gitleaks && git clone https://github.com/gitleaks/gitleaks.git /usr/local/gitleaks
cd /usr/local/gitleaks
make build
cd /
export PATH=$PATH:/usr/local/gitleaks
echo -n "gitleaks " && gitleaks version

echo "Installation completed successfully."
