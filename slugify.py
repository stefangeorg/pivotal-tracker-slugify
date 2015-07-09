#!/usr/bin/env python
import re
import sys

def slugify(value):
    """
    http://stackoverflow.com/questions/5574042/string-slugification-in-python
    Converts to lowercase, removes non-word characters (alphanumerics and
    underscores) and converts spaces to hyphens. Also strips leading and
    trailing whitespace.
    """
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return re.sub('[-\s]+', '-', value)

def get_tasks(token, project_id):
  headers = [
    ['X-TrackerToken', token]
  ]
  url = "https://www.pivotaltracker.com/services/v5/projects/%(project_id)s/stories?date_format=millis&with_state=unstarted"
       % {'project_id':project_id}

TOKEN = os.environ.get('PIVOTAL_TRACKER_TOKEN')
PROJECT_ID = os.environ.get('PIVOTAL_PROJECT_ID')

text = " ".join(sys.argv[1:]).trim()
replacements = [
  ['bug-', 'bug/'],
  ['feature-', 'feature/'],
  ['fix-', 'fix/']
]
text = slugify(text)
for r in replacements:
  text = text.replace(r[0], r[1])
print(text)
sys.exit()
