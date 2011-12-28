from datetime import datetime
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from socialmedia.tweets.constants import TWITTER_USER_TYPES
from base.models import Campaign

class TwitterUser(models.Model):
    candidate = models.ForeignKey(Campaign)
    screen_name = models.CharField(max_length=100)
    type = models.CharField(max_length=25, choices=TWITTER_USER_TYPES)
    location = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=255, blank=True)
    profile_image_url = models.CharField(max_length=255, blank=True)
    url = models.URLField(verify_exists=True, blank=True)
    followers_count = models.IntegerField(blank=True, null=True)
    friends_count = models.IntegerField(blank=True, null=True)
    statuses_count = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='images/twitter/', blank=True, help_text='Twitter account image')
    
    class Meta:
        ordering = ['screen_name']
    
    def __unicode__(self):
        return '%s | %s' % (self.screen_name, self.type)

class Tweet(models.Model):
    tweet_id = models.CharField(max_length=20)
    twitter_user = models.ForeignKey(TwitterUser)
    text = models.CharField(max_length=200)
    created_at = models.DateTimeField()

    @property
    def datetime(self):
        return datetime.fromtimestamp(self.time)

    @property
    def tweeter(self):
        return self.twitter_user.candidate
    
    def __unicode__(self):
        return self.text