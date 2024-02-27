FROM --platform=linux/amd64 alpine:3.20.0

COPY installation/linux_install_packages.sh .gitleaks.toml gitleaks.sh main.py ./find-and-report-secrets-in-code/

RUN sh ./find-and-report-secrets-in-code/linux_install_packages.sh
