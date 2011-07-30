from geopy import geocoders
from geopy.geocoders.base import GeocoderResultError
from geopy.geocoders.google import GQueryError
from django.conf import settings
from base.models import Location

# Automatically geocodes the place and saves lat/lng
g = geocoders.Google(settings.GOOGLE_API_KEY)

for l in Location.objects.filter(lat='', lng=''):
    try:
        place, (lat, lng) = g.geocode('%s %s' % (l.city, l.state))
    except:
        lat, lng = '', ''

    l.lat = str(lat)
    l.lng = str(lng)
    l.save()
