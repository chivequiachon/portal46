import requests
import datetime


class FbGroup(object):
  name = None
  id = None
  url = None
  post_count = 0

  def __init__(self, name, id, post_count):
    self.name = name
    self.id = id
    self.post_count = post_count
    self.url = "https://www.facebook.com/" + id


# id:fb_page_name
FB_GROUPS = {
  'nogizaka46':'乃木坂46 (nogizaka46)',
  'ngzk46sg':'乃木坂46 - Nogizaka46 Singapore Page',
  'HoshiminaID':'Hoshino Minami - 星野みなみ Indonesia Fanspage',
  'NaachanTHFanpageN46':'Nishino Nanase Thai Fanpage',
  'ShimaiyanID':'Shiraishi Mai - 白石麻衣 Indonesia Fansclub',
}

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
  return posts

def get_fb_group_posts_number(since, group, access_token):
  posts = get_fb_group_posts(since, group, access_token)
  return len(posts)

def get_target_date():
  yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
  target_date = yesterday.strftime("%Y-%m-%d")
  return target_date
