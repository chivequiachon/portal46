from django.db import models

class SubtitleFile(models.Model):
    subtitle_name = models.CharField(max_length=100)
    subtitle_download_link = models.CharField(max_length=100)

    def publish(self):
        self.save()

    def __str__(self):
        return self.subtitle_name
