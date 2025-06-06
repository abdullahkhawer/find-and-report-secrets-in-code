# build stage
FROM golang:1.23.0-alpine3.20 AS build

RUN apk add --no-cache git make \
    && git clone https://github.com/gitleaks/gitleaks.git /usr/local/gitleaks \
    && cd /usr/local/gitleaks \
    && git config --global --add safe.directory /usr/local/gitleaks \
    && git checkout tags/v8.27.0 \
    && make build

# final stage
FROM python:3.12.5-alpine3.20

COPY --from=build /usr/local/gitleaks/gitleaks /usr/local/gitleaks/gitleaks

COPY .gitleaks.toml gitleaks.sh main.py ./find-and-report-secrets-in-code/

RUN apk add --no-cache git bash jq \
    && pip install --no-cache-dir atlassian-python-api pytz requests slack-sdk

CMD ["sh"]
