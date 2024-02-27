GITLEAKS_VERSION="v8.18.2"

rm -rf ${PATH_TO_GIT_REPO}/gitleaks-report-detailed.json

docker run --rm -v ${PATH_TO_GIT_REPO}:/path zricethezav/gitleaks:${GITLEAKS_VERSION} \
    detect -r /path/gitleaks-report-detailed.json -f json --no-git -s /path

cat ${PATH_TO_GIT_REPO}/gitleaks-report-detailed.json | \
    jq 'map({Description: .Description, Fingerprint: .Fingerprint})' \
    > ./gitleaks-report.json
