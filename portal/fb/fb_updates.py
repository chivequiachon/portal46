import requests
import datetime

class FbPost(object):
  created_time = ""
  message = ""
  story = ""
  
  def __init__(self, story, message, created_time):
    self.story = story
    self.message = message
    self.created_time = created_time
    

def get_access_token(fb_client_id, fb_client_secret):
  ACCESS_TOKEN_URL = "https://graph.facebook.com/oauth/access_token?client_id={}&client_secret={}&grant_type=client_credentials".format(fb_client_id, fb_client_secret)
  response = requests.get(ACCESS_TOKEN_URL)
  data = response.json()
  access_token = data['access_token']
  return access_token


def get_target_date():
  yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
  target_date = yesterday.strftime("%Y-%m-%d")
  return target_date
