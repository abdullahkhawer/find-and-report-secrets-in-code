#!/bin/bash

# update package lists
apt-get update

# install Git, jq, pip, Python3, Make, wget
apt install -y git jq python3-pip python3 make wget
git --version && jq --version && make --version && wget --version

# upgrade pip
pip3 install --upgrade pip
pip --version && python3 --version

# install "Python Atlassian REST API Wrapper" and "World timezone definitions, modern and historical" Python libraries
pip install atlassian-python-api pytz

# install Go (Golang)
wget https://go.dev/dl/go1.22.0.linux-amd64.tar.gz
rm -rf /usr/local/go && tar -C /usr/local -xzf go1.22.0.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
go version

# install Gitleaks
rm -rf /usr/local/gitleaks && git clone https://github.com/gitleaks/gitleaks.git /usr/local/gitleaks
cd /usr/local/gitleaks
make build
export PATH=$PATH:/usr/local/gitleaks
gitleaks version
