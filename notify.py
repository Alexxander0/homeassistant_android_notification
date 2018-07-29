import argparse
import json
import requests
import datetime

from oauth2client.service_account import ServiceAccountCredentials

PROJECT_ID = 'XXXXXXXXXXXX' # EDIT YOUR PROJECT ID HERE e.g. "project-XXXXXXXXXXXX"

# The domain of your component. Should be equal to the name of your component.
DOMAIN = 'notify'

ATTR_TITLE = 'title'
ATTR_MESSAGE = 'message'
ATTR_TYPE = 'type'

BASE_URL = 'https://fcm.googleapis.com'
FCM_ENDPOINT = 'v1/projects/' + PROJECT_ID + '/messages:send'
FCM_URL = BASE_URL + '/' + FCM_ENDPOINT
FCM_SCOPE = 'https://www.googleapis.com/auth/firebase.messaging'
FCM_TOPIC = 'homeassistant'

import logging
logger = logging.getLogger(__name__)

def setup(hass, config):
    """Set up is called when Home Assistant is loading our component."""


    def handle_service(call):
        
        _get_access_token()
        
        msg_title = call.data.get(ATTR_TITLE, '')
        msg_text = call.data.get(ATTR_MESSAGE,'')
        msg_type = call.data.get(ATTR_TYPE,'unkown')

        msg = _build_common_message(msg_title, msg_text,msg_type)

        json.dumps(msg, indent=2)
        res = _send_fcm_message(msg)
        if(res):
            return True
        else:
            return False

    hass.services.register(DOMAIN, 'android', handle_service)

    # Return boolean to indicate that initialization was successfully.
    return True



# [START retrieve_access_token]
def _get_access_token():
    """Retrieve a valid access token that can be used to authorize requests.
    :return: Access token.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        '/home/homeassistant/.homeassistant/custom_components/service-account.json', FCM_SCOPE)
    access_token_info = credentials.get_access_token()
    logger.debug("Using token: " + access_token_info.access_token)
    return access_token_info.access_token
    # [END retrieve_access_token]

    """Server Side FCM sample.
    Firebase Cloud Messaging (FCM) can be used to send messages to clients on iOS,
    Android and Web.
    This sample uses FCM to send two types of messages to clients that are subscribed
    to the `news` topic. One type of message is a simple notification message (display message).
    The other is a notification message (display notification) with platform specific
    customizations. For example, a badge is added to messages that are sent to iOS devices.
    """

def _send_fcm_message(fcm_message):
  """Send HTTP request to FCM with given message.
  Args:
    fcm_message: JSON object that will make up the body of the request.
  """
  # [START use_access_token]
  headers = {
    'Authorization': 'Bearer ' + _get_access_token(),
    'Content-Type': 'application/json; UTF-8',
  }
  # [END use_access_token]
  resp = requests.post(FCM_URL, data=json.dumps(fcm_message), headers=headers)

  logger.debug("Request answer, Status Code: " + str(resp.status_code))
  logger.debug("Request answer, Text: " + resp.text)

  if resp.status_code == 200:
    print('Message sent to Firebase for delivery, response:')
    print(resp.text)
    return True
  else:
    print('Unable to send message to Firebase')
    print(resp.text)
    return False

def _build_common_message(msg_title,msg_text,msg_type):
  """Construct common notifiation message.
  Construct a JSON object that will be used to define the
  common parts of a notification message that will be sent
  to any app instance subscribed to the news topic.
  """
  data = {
    'message': {
      "topic" : '',
      'data': {
        'title': '',
        'message': '',
        'type' : ''
      }
    }
  }
  data['message']['topic'] = FCM_TOPIC
  data['message']['data']['title'] = msg_title
  data['message']['data']['message'] = datetime.datetime.now().strftime("%H:%M:%S") + " " + msg_text
  data['message']['data']['type'] = msg_type
  return data
