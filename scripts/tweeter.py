import twitter, datetime, random, cPickle
from base.models import *
from django.conf import settings
from utils import bitly

def shorten_link(id):
    try:
        bitly_api = bitly.Api(login=settings.BITLY_USER, apikey=settings.BITLY_API_KEY) 
        shortened_link = bitly_api.shorten('http://www.politicsverbatim.org/excerpt/%s/' % str(id))
    except:
        return False

def tweet(text):
#    try:
    print settings.TWITTER_USER
    print settings.TWITTER_PASSWORD
    twitter_api = twitter.Api(username=settings.TWITTER_USER, password=settings.TWITTER_PASSWORD)
    twitter_api.PostUpdate(update_txt)
    return True
#    except:
#        return False

if __name__ == '__main__':    
    if random.randint(1, 100) % 2 <> 0:
        print 'no'
        exit()

    if not settings.TWITTER_USER or not settings.TWITTER_PASSWORD:
        exit()


    excerpts = Excerpt.objects.filter(date_entered__year=datetime.date.today().year,
                                      date_entered__month=datetime.date.today().month,
                                      date_entered__day=datetime.date.today().day)    
    
    # Get previously tweeted items from pickle
    try:
        tweet_pickle = open(settings.TWEET_PICKLE_PATH, 'r')
        already_tweeted = cPickle.load(tweet_pickle)
        tweet_pickle.close()
    except EOFError:
        already_tweeted = []
    
    for e in excerpts:
        if e.id not in already_tweeted:
            update_txt = '%s: ' % e.campaign.name
            update_len = len(update_txt) + 20 # To account for 20-char bitly URL
            excerpt_snippet = e.text[:(130-update_len)]
            update_txt = update_txt + '%s ... %s' % (excerpt_snippet, shorten_link(e.id))
    
            tweeted = tweet(update_txt)            
            if tweeted:
                print 'asa'
                already_tweeted.append(e.id)
    
    # Repickle tweeted items
    tweet_pickle = open(settings.TWEET_PICKLE_PATH, 'w')
    cPickle.dump(already_tweeted, tweet_pickle)
    tweet_pickle.close()
