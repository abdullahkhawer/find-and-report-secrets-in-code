#!/bin/bash

echo "Script Execution Started!"

# remove Gitleaks reports if they exist already
echo "Removing Gitleaks reports if they exist already..."
rm -rf ${PATH_TO_GIT_REPO}/gitleaks-report-detailed.json
rm -rf ./gitleaks-report.json

# run Gitleaks to find secrets and generate a detailed report in JSON for the secrets found
echo "Running Gitleaks to find secrets and generating a detailed report in JSON for the secrets found..."
gitleaks detect -r ${PATH_TO_GIT_REPO}/gitleaks-report-detailed.json -f json -s ${PATH_TO_GIT_REPO} --redact --no-git

# create a final report in JSON using the detailed report having relevant information only
echo "Creating a final report in JSON using the detailed report having relevant information only..."
echo "[" > ./gitleaks-report.json
cat ${PATH_TO_GIT_REPO}/gitleaks-report-detailed.json | jq -c '.[]' | while read -r line; do
    description=$(jq -r '.Description' <<< "$line")
    start_line=$(jq -r '.StartLine' <<< "$line")
    file=$(jq -r '.File' <<< "$line")
    file=$(echo "$file" | sed "s|^${PATH_TO_GIT_REPO}|.|")
    secret_type=$(jq -r '.RuleID' <<< "$line")

    # use 'git blame' to find the commit id and author for each finding
    blame=$(cd ${PATH_TO_GIT_REPO} && git blame -L "$start_line","$start_line" "$file" --porcelain)
    commit_id=$(echo "$blame" | awk 'NR==1' | awk -F ' ' '{print $1}')
    author=$(echo "$blame" | awk 'NR==2' | awk -F 'author ' '{print $2}')

    # append final JSON objects to the new report
    jq -n \
        --arg desc "$description" \
        --arg file "$file" \
        --arg line_no "$start_line" \
        --arg type "$secret_type" \
        --arg commit "$commit_id" \
        --arg author "$author" \
        '{"Description": $desc, "File": $file, "Line No.": $line_no, "Secret Type": $type, "Commit": $commit, "Author": $author}' >> ./gitleaks-report.json

    echo "," >> ./gitleaks-report.json
done
head -n $(($(wc -l < ./gitleaks-report.json) - 1)) ./gitleaks-report.json > ./temp.json && mv ./temp.json ./gitleaks-report.json
echo "]" >> ./gitleaks-report.json
cat ./gitleaks-report.json | jq > ./temp.json && mv ./temp.json ./gitleaks-report.json

echo "Script Execution Completed!"
