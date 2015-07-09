#!/usr/bin/env python
import re
import sys
import os
import json
import urllib.request


def slugify(value):
    """
    http://stackoverflow.com/questions/5574042/string-slugification-in-python
    Converts to lowercase, removes non-word characters (alphanumerics and
    underscores) and converts spaces to hyphens. Also strips leading and
    trailing whitespace.
    """
    index = 60
    if len(value) > index:
        pos = value.rfind(' ', 0, index)
        value = value[0:pos]
    
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return re.sub('[-\s]+', '-', value)

def get_tasks(token, project_id, task_id):
    url = "%(api_endpoint)s%(project_id)s/stories?date_format=millis&with_state=unstarted" \
       % {'project_id': project_id,'api_endpoint': 'https://www.pivotaltracker.com/services/v5/projects/'}

    req = urllib.request.Request(url)
    req.add_header('X-TrackerToken', token)
    response = urllib.request.urlopen(req)
  
    ret = json.loads(response.readall().decode('utf-8'))
  
    for story in ret:
        story_id = "%s" % story['id']
        story_id = story_id[-3:]
        if not task_id:
            if story_id not in story['name']:
                story['name'] = "%s - %s" % (story_id, story['name'])
            print("%s/%s" % (story['story_type'], slugify(story['name'])))
        if task_id == story_id:
            if story_id not in story['name']:
                story['name'] = "%s - %s" % (task_id, story['name'])
            return"%s/%s" % (story['story_type'], slugify(story['name']))
  
TOKEN = os.environ.get('PIVOTAL_TRACKER_TOKEN')
PROJECT_ID = os.environ.get('PIVOTAL_PROJECT_ID')


task_id = False
if len(sys.argv) > 1:
    task_id = sys.argv[1]

print(get_tasks(TOKEN, PROJECT_ID, task_id))
sys.exit()
