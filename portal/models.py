from django.db import models
from django.conf import settings

from portal import endecoder
from portal.fb.fb_updates import FbPost

import requests


class SubtitleFile(models.Model):
    subtitle_name = models.CharField(max_length=100)
    subtitle_download_link = models.CharField(max_length=100)

    def publish(self):
        self.save()

    def __str__(self):
        return self.subtitle_name


class Credential(models.Model):
    username = models.CharField(max_length=500)
    password = models.CharField(max_length=500)
    forum = models.CharField(max_length=30)
    
    def save(self, *args, **kwargs):
        self.username = endecoder.encode(self.username)
        self.password = endecoder.encode(self.password)
    
        super(Credential, self).save(*args, **kwargs)
    
    def publish(self):
        self.save()
        
    def __str__(self):
        return self.username


class FbPage(models.Model):
    page_id = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    img_url = models.CharField(max_length=100, default='to_be_changed')
    cookie_ref_idx = models.CharField(max_length=3, default='0')
    posts = None
    post_count = None

    def retrieve_posts(self, access_token, target_date):
        # retrieve fb posts
        FB_GROUP_POST_RETRIEVE_URL = "https://graph.facebook.com/v2.9/{}/feed?access_token={}&since={}".format(self.page_id, access_token, target_date)

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

        self.posts = fb_posts
        self.post_count = len(self.posts)
    

    def __str__(self):
        return "[{}] {} : {} : {}".format(self.cookie_ref_idx, self.name, self.page_id, self.img_url)
