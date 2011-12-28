from django.contrib import admin
from socialmedia.tweets.models import *

class TwitterUserAdmin(admin.ModelAdmin):
    pass
admin.site.register(TwitterUser, TwitterUserAdmin)

class TweetAdmin(admin.ModelAdmin):
    pass
admin.site.register(Tweet, TweetAdmin)