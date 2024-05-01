#!/bin/bash

# install Git, jq, pip, Python3, Gitleaks
brew install git jq python python@3 gitleaks
git --version && jq --version && gitleaks version

# upgrade pip
pip install --upgrade pip
pip --version && python3 --version

# install "Python Atlassian REST API Wrapper" and "World timezone definitions, modern and historical" Python libraries
pip install atlassian-python-api pytz
