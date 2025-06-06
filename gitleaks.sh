#!/bin/bash
# shellcheck disable=SC2002
echo "Script Execution Started!"

# remove Gitleaks reports if they exist already
echo "Removing Gitleaks reports if they exist already..."
rm -rf "${LOCAL_PATH_TO_GIT_REPO}/gitleaks-report-detailed.json"
rm -rf ./gitleaks-report.json

# run Gitleaks to find secrets and generate a detailed report in JSON for the secrets found
echo "Running Gitleaks to find secrets and generating a detailed report in JSON for the secrets found..."
echo -n "Gitleaks v" && gitleaks version
gitleaks detect -r "${LOCAL_PATH_TO_GIT_REPO}/gitleaks-report-detailed.json" -f json -s "${LOCAL_PATH_TO_GIT_REPO}" --redact --no-git

# create a final report in JSON using the detailed report having relevant information only
echo "Creating a final report in JSON using the detailed report having relevant information only..."
file_contents=$(cat "${LOCAL_PATH_TO_GIT_REPO}/gitleaks-report-detailed.json")
if [ "${file_contents}" != "[]" ]; then
    echo "[" > ./gitleaks-report.json
    cat "${LOCAL_PATH_TO_GIT_REPO}/gitleaks-report-detailed.json" | jq -c '.[]' | while read -r line; do
        description=$(jq -r '.Description' <<< "${line}")
        start_line=$(jq -r '.StartLine' <<< "${line}")
        file=$(jq -r '.File' <<< "${line}")
        file="${file#"${LOCAL_PATH_TO_GIT_REPO}"/}"
        secret_type=$(jq -r '.RuleID' <<< "${line}")
        url="${REMOTE_PATH_TO_GIT_REPO}/-/blob/${BRANCH_NAME}/${file}"
        url="${url// /%20}"

        if [[ "${start_line}" == "0" ]]; then
            # use 'git log' to find the commit id, commit author and commit author's email for the finding
            git_log=$(cd "${LOCAL_PATH_TO_GIT_REPO}" && git log -1 ./"${file}")
            commit_id=$(echo "${git_log}" | awk 'NR==1' | awk -F ' ' '{print $2}')
            commit_author=$(echo "${git_log}" | awk 'NR==2' | awk -F 'Author: ' '{print $2}' | awk -F ' <' '{print $1}')
            commit_author_email=$(echo "${git_log}" | awk 'NR==2' | awk -F 'Author: ' '{print $2}' | awk -F ' <' '{print $2}')
            commit_author_email="${commit_author_email%>}"
        else
            url="${url}#L${start_line}"
            # use 'git blame' to find the commit id, commit author and commit author's email for the finding
            git_blame=$(cd "${LOCAL_PATH_TO_GIT_REPO}" && git blame -L "${start_line}","${start_line}" ./"${file}" --porcelain)
            commit_id=$(echo "${git_blame}" | awk 'NR==1' | awk -F ' ' '{print $1}')
            commit_author=$(echo "${git_blame}" | awk 'NR==2' | awk -F 'author ' '{print $2}')
            commit_author_email=$(echo "${git_blame}" | awk 'NR==3' | awk -F 'author-mail <' '{print $2}')
            commit_author_email="${commit_author_email%>}"
        fi

        # append final JSON objects to the new report
        jq -n \
            --arg desc "${description}" \
            --arg file "${file}" \
            --arg line_no "${start_line}" \
            --arg url "${url}" \
            --arg type "${secret_type}" \
            --arg commit_id "${commit_id}" \
            --arg commit_author "${commit_author}" \
            --arg commit_author_email "${commit_author_email}" \
            '{"Description": $desc, "File": $file, "Line No.": $line_no, "Link": $url, "Secret Type": $type, "Commit ID": $commit_id, "Commit Author": $commit_author, "Commit Author Email": $commit_author_email}' >> ./gitleaks-report.json

        echo "," >> ./gitleaks-report.json
    done
    head -n $(($(wc -l < ./gitleaks-report.json) - 1)) ./gitleaks-report.json > ./temp.json && mv ./temp.json ./gitleaks-report.json
    echo "]" >> ./gitleaks-report.json
    cat ./gitleaks-report.json | jq > ./temp.json && mv ./temp.json ./gitleaks-report.json
else
    echo "[]" > ./gitleaks-report.json
fi

echo "Script Execution Completed!"
