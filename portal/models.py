from django.db import models
from django.conf import settings

from portal import endecoder


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

	def __str__(self):
		return "{} : {}".format(self.name, self.page_id)
