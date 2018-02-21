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
    

class FbGroup(object):
  name = None
  id = None
  url = None
  posts = None # FbPost list
  post_count = 0

  def __init__(self, name, id, posts, post_count):
    self.name = name
    self.id = id
    self.posts = posts
    self.post_count = post_count
    self.url = "https://www.facebook.com/" + id


def get_access_token():
  #ACCESS_TOKEN_URL = "https://graph.facebook.com/oauth/access_token?client_id=1831017710453000&client_secret=d0a5b177319e8ec5b3b414cdd544d953&grant_type=client_credentials"
  #response = requests.get(ACCESS_TOKEN_URL)
  #data = response.json()
  #access_token = data['access_token']
  return "1831017710453000|4BzULaLlMZiC3AgulMVkDKz6RkE"


def get_fb_group_posts(since, group, access_token):
  FB_GROUP_POST_RETRIEVE_URL = "https://graph.facebook.com/v2.9/{}/feed?access_token={}&since={}".format(group, access_token, since)
  
  response = requests.get(FB_GROUP_POST_RETRIEVE_URL) 
  data = response.json()
  posts = data['data']
  
  fb_posts = []
  for post in posts:
    story = ""
    message = ""
    created_time = ""
    if 'story' in post:
      story = post['story']
    
    if 'message' in post:
      message = post['message']
      
    if story != "" and message != "":
      story += "<br />"
    
    # Every facebook post always has a created_time
    created_time_keywords = post['created_time'].replace("T", " ").replace("+", " ").split(" ")
    created_time = "[{}][{}]".format(created_time_keywords[0], created_time_keywords[1])
      
    fb_posts.append(FbPost(story, message, created_time))
    
  return fb_posts

def get_fb_group_posts_number(since, group, access_token):
  posts = get_fb_group_posts(since, group, access_token)
  return len(posts)

def get_target_date():
  yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
  target_date = yesterday.strftime("%Y-%m-%d")
  return target_date
