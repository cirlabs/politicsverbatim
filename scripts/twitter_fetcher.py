import twitter, urllib2, time, datetime
from socialmedia.tweets.models import *

twitter_users = TwitterUser.objects.all()

for u in twitter_users:
    api = twitter.Api() 
    try:
        statuses = api.GetUserTimeline(u.screen_name, count=1000)
    except urllib2.HTTPError:
        statuses = None
    if statuses:
        for s in statuses:
            date = datetime.strptime(s.created_at.replace(' +0000', ''), "%a %b %d %H:%M:%S %Y").strftime("%Y-%m-%d %H:%M:%S")
            tweet, created = Tweet.objects.get_or_create(tweet_id=s.id, twitter_user=u, text=s.text, created_at=date)
            tweet.save()
            # Shortcut to update twitter profile information when new tweets are entered
            if created:
                u.followers_count = s.user.followers_count
                u.friends_count = s.user.friends_count
                u.statuses_count = s.user.statuses_count
                u.save()
        time.sleep(5)
