import sys
import re
import json
import os
from atlassian import Confluence

# get branch name from the argument passed to the script
if len(sys.argv) != 2:
   print("ERROR: Invalid arguments passed.")
   print("Usage: python script.py [BRANCH NAME]")
   print("Example: python script.py master")
   sys.exit(1)
branch_name = sys.argv[1]

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
<h2>Branch: {}</h2>
<h3>Secrets Found: {}</h3>
<table data-number-column="true" data-table-width="1400" data-layout="default">
   <tbody>
      <tr>
         <th class="numberingColumn" />
         <th>
            <p><strong>Fingerprint</strong></p>
         </th>
         <th>
            <p><strong>Description</strong></p>
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
      <p><code>{}</code></p>
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

# read JSON from file
with open("./gitleaks-report.json", "r") as file:
   data = json.load(file)

# update HTML page template to add the data read from JSON file
rows = ""
rows_count = 1
for entry in data:
   fingerprint = entry["Fingerprint"]
   description = entry["Description"]
   rows += row_template.format(rows_count, fingerprint, description)
   rows_count = rows_count + 1
html_template = html_template.format(branch_name, len(data), rows)

# get current page content
page = conf.get_page_by_id(page_id, expand='body.storage')
page_content = page['body']['storage']['value']

# define the pattern to replace the respective div
pattern = r'<h2>Branch: {}.*?</table>'.format(branch_name)

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
