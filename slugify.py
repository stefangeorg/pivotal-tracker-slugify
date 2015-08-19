#!/usr/bin/env python
import re
import sys
import os
import json
import urllib.request


MAXIMUM_CHARACTERS = 60

def slugify(value):
    """
    http://stackoverflow.com/questions/5574042/string-slugification-in-python
    Converts to lowercase, removes non-word characters (alphanumerics and
    underscores) and converts spaces to hyphens. Also strips leading and
    trailing whitespace.
    """
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return re.sub('[-\s]+', '-', value)

def preprocessing_story_name(story_name):
    if len(story_name) > MAXIMUM_CHARACTERS:
        pos = story_name.rfind(' ', 0, MAXIMUM_CHARACTERS)
        story_name = story_name[0:pos]
        
    return slugify(story_name)


def make_story_name(story, task_id):
    if not story['name'][0].isdigit():
        story['name'] = "%s - %s" % (task_id, story['name'])
        
    return"%s/%s" % (story['story_type'], preprocessing_story_name(story['name']))
        

def pivotal_client(token, project_id, task_id):
    url = "%(api_endpoint)s%(project_id)s/stories?date_format=millis&filter=state:unstarted,started" \
       % {'project_id': project_id,'api_endpoint': 'https://www.pivotaltracker.com/services/v5/projects/'}

    req = urllib.request.Request(url)
    req.add_header('X-TrackerToken', token)
    response = urllib.request.urlopen(req)
  
    ret = json.loads(response.readall().decode('utf-8'))
    
    return ret
    
def get_tasks(token, project_id, task_id):
    ret = pivotal_client(token, project_id, task_id)
    
    for story in ret:
        story_id = str(story['id'])
        
        if not task_id:
            print(make_story_name(story, story_id[-3:]))
            
        if story_id.endswith(str(task_id)) or story['name'].lower().startswith(str(task_id)):
            print(make_story_name(story, task_id))

  
TOKEN = os.environ.get('PIVOTAL_TRACKER_TOKEN')
PROJECT_ID = os.environ.get('PIVOTAL_PROJECT_ID')


task_id = False
if len(sys.argv) > 1:
    task_id = sys.argv[1]

get_tasks(TOKEN, PROJECT_ID, task_id)
sys.exit()
