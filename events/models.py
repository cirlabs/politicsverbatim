import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.managers import CurrentSiteManager
from django.conf import settings
from base.models import Campaign, Document

class Type(models.Model):
    """
    The type of event being entered: A fund-raiser, speech, etc.
    """
    name = models.CharField(max_length=100, help_text='The type of event you are entering. Ex. Fund-raiser, speech, etc.')
    slug = models.SlugField(max_length=255, unique=True, help_text=(u"Built automatically. Do not change unless you know what you're doing."))
    
    class Meta:
        ordering = ['name']
    
    def __unicode__(self):
        return self.name


class UpcomingEventsManager(models.Manager):
    def get_query_set(self):
        return super(UpcomingEventsManager, self).get_query_set().filter(event_datetime__gte=datetime.datetime.now()).order_by('-event_datetime')


class Event(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, help_text=(u"Built automatically. Do not change unless you know what you're doing."))
    description = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    event_datetime = models.DateTimeField()
    type = models.ForeignKey(Type)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=2, blank=True)
    lat = models.CharField(max_length=12, blank=True)
    lng = models.CharField(max_length=12, blank=True)
    candidate = models.ForeignKey(Campaign)
    covered = models.BooleanField()
    assigned_to = models.CharField(max_length=255, blank=True)
    
    # Managers
    objects = models.Manager()
    upcoming_events = UpcomingEventsManager()

    class Meta:
        ordering = ['event_datetime']

    def __unicode__(self):
        return self.title
    
    def save(self):
        from geopy import geocoders
        from geopy.geocoders.base import GeocoderResultError
        from geopy.geocoders.google import GQueryError
        
        # Automatically geocodes the place and saves lat/lng
        g = geocoders.Google(settings.GOOGLE_API_KEY)
        try:
            place, (lat, lng) = g.geocode('%s %s %s' % (self.address, self.city, self.state))
        except (GeocoderResultError, GQueryError):
            try:
                place, (lat, lng) = g.geocode('%s %s' % (self.city, self.state))
            except:
                lat, lng = '', ''
        except:
            lat, lng = '', ''
        
        self.lat = str(lat)
        self.lng = str(lng)
        
        super(Event, self).save()
