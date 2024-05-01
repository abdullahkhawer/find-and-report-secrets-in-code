import sys
import re
import json
import os
from atlassian import Confluence
from datetime import datetime
import pytz

# get time zone, repository name and branch name from the arguments passed to the script
if len(sys.argv) != 4:
   print("ERROR: Invalid arguments passed.")
   print("Usage: python script.py [BRANCH NAME]")
   print("Example: python script.py master")
   sys.exit(1)
time_zone = sys.argv[1]
repo_name = sys.argv[2]
branch_name = sys.argv[3]

# Get the current time in UTC and convert it into the desired time zone's time
time_now = datetime.now()
target_timezone = pytz.timezone(time_zone)
time_now = time_now.astimezone(target_timezone)
time_now = time_now.strftime('%Y-%m-%d %H:%M:%S %Z')

# get environment variables related to confluence
conf_site = os.getenv("CONFLUENCE_SITE")
conf_user = os.getenv("CONFLUENCE_USER_EMAIL_ID")
conf_pass = os.getenv("CONFLUENCE_USER_TOKEN")
page_title = os.getenv("CONFLUENCE_PAGE_TITLE")
page_space = os.getenv("CONFLUENCE_PAGE_SPACE")
if conf_site is None:
   print("ERROR: CONFLUENCE_SITE environment variable is not set.")
   sys.exit(1)
if conf_user is None:
   print("ERROR: CONFLUENCE_USER_EMAIL_ID environment variable is not set.")
   sys.exit(1)
if conf_pass is None:
   print("ERROR: CONFLUENCE_USER_TOKEN environment variable is not set.")
   sys.exit(1)
if page_title is None:
   print("ERROR: CONFLUENCE_PAGE_TITLE environment variable is not set.")
   sys.exit(1)
if page_space is None:
   print("ERROR: CONFLUENCE_PAGE_SPACE environment variable is not set.")
   sys.exit(1)

# define HTML page template
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
            <p><strong>Author</strong></p>
         </th>
      </tr>
      {}
   </tbody>
</table>
"""

# define HTML row template
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
conf = Confluence(url=conf_site, username=conf_user, password=conf_pass)

# resolve page ID
page_id = conf.get_page_id(page_space, page_title)

# get current page content
page = conf.get_page_by_id(page_id, expand='body.storage')
page_content = page['body']['storage']['value']

# read JSON from file
with open("./gitleaks-report.json", "r") as file:
   data = json.load(file)

# update HTML page template to add the data read from JSON file
rows = ""
rows_count = 1
for entry in data:
   description = entry["Description"]
   file = entry["File"]
   line_no = entry["Line No."]
   secret_type = entry["Secret Type"]
   commit = entry["Commit"]
   author = entry["Author"]
   rows += row_template.format(rows_count, description, file, line_no, secret_type, commit, author)
   rows_count = rows_count + 1
html_template = html_template.format(repo_name, branch_name, time_now, len(data), rows)

# define the pattern to replace the respective div
pattern = r'<h2>Repository: {} - Branch: {}.*?</table>'.format(repo_name, branch_name)

# Check if pattern is found or not and update the page content accordingly
new_page_content = page_content
if re.search(pattern, page_content, flags=re.DOTALL):
   # pattern found; replace matching pattern in the existing content with the new HTML page template
   new_page_content = re.sub(pattern, html_template, page_content, flags=re.DOTALL)
else:
   # pattern not found; add the new HTML page template at the end of the existing content
   new_page_content = new_page_content + "\n" + html_template

# update page with new content
conf.update_page(page_id, page_title, new_page_content, type='page', \
                 representation='storage', minor_edit=False, full_width=True)
