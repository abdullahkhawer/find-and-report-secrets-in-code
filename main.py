import json
import os
import pytz
import re
import requests
import sys
from atlassian import Confluence
from datetime import datetime

# get time zone, repository name and branch name from the arguments passed to the script
if len(sys.argv) < 4 or len(sys.argv) > 5:
   print("ERROR: Invalid arguments passed.")
   print("Usage: python main.py TIME_ZONE REPOSITORY_NAME BRANCH_NAME [JSON_REPORT_URL]")
   print("Example: python main.py Europe/Amsterdam myproj/myrepo master")
   sys.exit(1)
time_zone = sys.argv[1]
repo_name = sys.argv[2]
branch_name = sys.argv[3]
json_report_url = ""
if len(sys.argv) == 5:
   json_report_url = sys.argv[4]

# Get the current time in UTC and convert it into the desired time zone's time
time_now = datetime.now()
target_timezone = pytz.timezone(time_zone)
time_now = time_now.astimezone(target_timezone)
time_now = time_now.strftime('%Y-%m-%d %H:%M:%S %Z')

# get environment variables related to Confluence
confluence_enabled = os.getenv("CONFLUENCE_ENABLED")
if confluence_enabled is None:
   print("ERROR: CONFLUENCE_ENABLED environment variable is not set.")
   sys.exit(1)
elif confluence_enabled == "1":
   confluence_site = os.getenv("CONFLUENCE_SITE")
   confluence_user = os.getenv("CONFLUENCE_USER_EMAIL_ID")
   confluence_pass = os.getenv("CONFLUENCE_USER_TOKEN")
   page_title = os.getenv("CONFLUENCE_PAGE_TITLE")
   page_space = os.getenv("CONFLUENCE_PAGE_SPACE")
   if confluence_site is None:
      print("ERROR: CONFLUENCE_SITE environment variable is not set.")
      sys.exit(1)
   if confluence_user is None:
      print("ERROR: CONFLUENCE_USER_EMAIL_ID environment variable is not set.")
      sys.exit(1)
   if confluence_pass is None:
      print("ERROR: CONFLUENCE_USER_TOKEN environment variable is not set.")
      sys.exit(1)
   if page_title is None:
      print("ERROR: CONFLUENCE_PAGE_TITLE environment variable is not set.")
      sys.exit(1)
   if page_space is None:
      print("ERROR: CONFLUENCE_PAGE_SPACE environment variable is not set.")
      sys.exit(1)

# get environment variables related to Slack
slack_enabled = os.getenv("SLACK_ENABLED")
if slack_enabled is None:
   print("ERROR: SLACK_ENABLED environment variable is not set.")
   sys.exit(1)
elif slack_enabled == "1":
   slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")
   if slack_webhook_url is None:
      print("ERROR: SLACK_WEBHOOK_URL environment variable is not set.")
      sys.exit(1)

# define HTML page template
if confluence_enabled == "1":
   html_template = """
   <h2>Repository: {} - Branch: {}</h2>
   <h4>Last Scan Time: {}</h4>
   <h3>Secrets Found: {}</h3>
   <table data-number-column="true" data-table-width="1400" data-layout="default">
      <tbody>
         <tr>
            <th class="numberingColumn"/>
            <th>
               <p><strong>Description</strong></p>
            </th>
            <th>
               <p><strong>File</strong></p>
            </th>
            <th>
               <p><strong>Line No.</strong></p>
            </th>
            <th>
               <p><strong>Secret Type</strong></p>
            </th>
            <th>
               <p><strong>Commit ID</strong></p>
            </th>
            <th>
               <p><strong>Commit Author</strong></p>
            </th>
         </tr>
         {}
      </tbody>
   </table>
   """

# define HTML row template
if confluence_enabled == "1":
   row_template = """
   <tr>
      <td class="numberingColumn">
         {}
      </td>
      <td>
         <p>{}</p>
      </td>
      <td>
         <p>{}</p>
      </td>
      <td>
         <p>{}</p>
      </td>
      <td>
         <p>{}</p>
      </td>
      <td>
         <p>{}</p>
      </td>
      <td>
         <p>{}</p>
      </td>
   </tr>
   """

# connect to Confluence
if confluence_enabled == "1":
   confluence = Confluence(url=confluence_site, username=confluence_user, password=confluence_pass)

# resolve page ID
if confluence_enabled == "1":
   page_id = confluence.get_page_id(page_space, page_title)

# get current page content
if confluence_enabled == "1":
   page = confluence.get_page_by_id(page_id, expand='body.storage')
   page_content = page['body']['storage']['value']

# read JSON from file
with open("./gitleaks-report.json", "r") as file:
   data = json.load(file)

# update HTML page template and find unique commit authors from the data read from JSON file
authors = []
rows = ""
rows_count = 1
for entry in data:
   author = entry["Author"]
   if confluence_enabled == "1":
      description = entry["Description"]
      file = entry["File"]
      line_no = entry["Line No."]
      secret_type = entry["Secret Type"]
      commit = entry["Commit"]
      rows += row_template.format(rows_count, description, file, line_no, secret_type, commit, author)
   if slack_enabled == "1":
      authors.append(author)
   rows_count = rows_count + 1
if confluence_enabled == "1":
   html_template = html_template.format(repo_name, branch_name, time_now, len(data), rows)
if slack_enabled == "1":
   authors = list(set(authors))
   authors.sort()

# define the pattern to replace the respective div
if confluence_enabled == "1":
   pattern = r'<h2>Repository: {} - Branch: {}.*?</table>'.format(repo_name, branch_name)

# Check if pattern is found or not and update the page content accordingly
if confluence_enabled == "1":
   new_page_content = page_content
   if re.search(pattern, page_content, flags=re.DOTALL):
      # pattern found; replace matching pattern in the existing content with the new HTML page template
      new_page_content = re.sub(pattern, html_template, page_content, flags=re.DOTALL)
   else:
      # pattern not found; add the new HTML page template at the end of the existing content
      new_page_content = new_page_content + "\n" + html_template

# update page with new content
if confluence_enabled == "1":
   try:
      confluence.update_page(page_id, page_title, new_page_content, type='page', representation='storage', minor_edit=False, full_width=True)
      print("Confluence page updated successfully.")
   except Exception as err:
      print("ERROR: Failed to update Confluence page.")
      print(f'ERROR: {err}')
      sys.exit(1)

# send notification to Slack
if slack_enabled == "1":
   message = "*Secrets Detection Notification*"
   message += f'\n>:file_folder: *Repository:* `{repo_name}`'
   message += f'\n>:git: *Branch:* `{branch_name}`'
   message += f'\n>:clock1: *Last Scan Time:* `{time_now}`'
   message += f'\n>:warning: *Secrets Found:* `{len(data)}`'
   message += f'\n>:technologist: *Commit Authors:* \n>• *{'*\n>• *'.join(authors)}*'
   if confluence_enabled == "1":
      message += f'\n:link: More details can be found here: <{confluence_site}/wiki/spaces/{page_space}/pages/{page_id}/{page_title}|Confluence Page>'
   if json_report_url != "":
      message += f'\n:link: JSON report can be found here: <{json_report_url}|JSON Report>'
   slack_data = {
      "blocks": [
         {
            "type": "section",
            "text": {
               "type": "mrkdwn",
               "text": message
            }
         }
      ]
   }
   headers = {'Content-Type': "application/json"}
   try:
      response = requests.post(slack_webhook_url, data=json.dumps(slack_data), headers=headers)
      response.raise_for_status()
      print("Notification sent to Slack successfully.")
   except Exception as err:
      print("ERROR: Failed to send notification to Slack.")
      print(f'ERROR: {err}')
      sys.exit(1)
