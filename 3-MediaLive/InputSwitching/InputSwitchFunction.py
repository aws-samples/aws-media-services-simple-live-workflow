import sys
import datetime
import time
import boto3
import json
import os
import random
import string

def lambda_handler(event, context):
    # update variable values, depending on what input switching action you want to schedule
    
    # start type could be fixed | immediate | follow
    start_type = "follow"  
    
    # replace with a UTC time on when you want switch to occur eg. 2019-08-13 20:01:00.000
    # must be at least 20 seconds in future
    # if left to None, code will set this to current time plus offset below
    fixed_time = None 
    offset = 20

    # replace with your channel id
    channel_id = "8096932" # replace with your channel ID
    
    # if doing a dynamic input switch, set to true
    # if true, must provide a dynamic_input_url
    dynamic = False # True | False
    dynamic_input_url = "techmkt-videoarchive/bbb/bbb_sunflower_1080p_30fps_normal.mp4" 

    # the name of the input we're switching to
    input_attachment_name = "MP4Input"
    
    #if switch start_type is set to follow, then must provide the name of action name to follow
    follow_action_name = "fixed_input_switch.451836"
    
    print (json.dumps(event))
    medialive = boto3.client('medialive')

    action = {}            
    action = {
        'ScheduleActionSettings': {
            'InputSwitchSettings': {
                'InputAttachmentNameReference': input_attachment_name
                
            }
        }
    }
    if dynamic == "True":
        action = {
        'ScheduleActionSettings': {
            'InputSwitchSettings': {
                'UrlPath': [dynamic_input_url],
                'InputAttachmentNameReference': input_attachment_name                
            }
        }
    }
    
    if start_type == "immediate":
        action['ActionName'] = 'immediate_input_switch.{}'.format(rand_string())
        action['ScheduleActionStartSettings'] = {'ImmediateModeScheduleActionStartSettings': {}}
    elif start_type == "follow":
        action['ActionName'] = 'follow_input_switch.{}'.format(rand_string())
        action['ScheduleActionStartSettings'] =  {'FollowModeScheduleActionStartSettings': {'FollowPoint': 'END', 'ReferenceActionName': follow_action_name}}
    else: #default is fixed
        offset_in_seconds = 20
        if fixed_time is not None:
            when = datetime.datetime.strptime(fixed_time, '%Y-%m-%d %H:%M:%S.%f')
        # doing fixed start type but time is not provided, so let's use utcnow plus offset
        else: # get utc time now + offset
            when = datetime.datetime.utcnow() + datetime.timedelta(seconds=offset_in_seconds)
        when = when.strftime('%Y-%m-%dT%H:%M:%SZ')
        action['ActionName'] = 'fixed_input_switch.{}'.format(rand_string())
        action['ScheduleActionStartSettings'] =  {'FixedModeScheduleActionStartSettings': {'Time': when}}

    print(action)
    response = medialive.batch_update_schedule(ChannelId=channel_id, Creates={'ScheduleActions':[action]})
    print("medialive schedule response: ")
    print(json.dumps(response))

def rand_string():
    s = string.digits
    return ''.join(random.sample(s,6))
