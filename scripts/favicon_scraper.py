import Image, urllib, urlparse
from django.core.files import File
from base.models import Source

# This script pulls favicons from the websites listed in base.models.Source
# In practice, we only had to run it a couple of times.

if __name__ == '__main__':
    sources = Source.objects.all()
    for source in sources:
        if source.url:
            try:
                # Go get the favicon from the base URL and try to save it
                infile = urllib.urlretrieve('http://%s/favicon.ico' % urlparse.urlparse(source.url)[1])
                try:
                    im = Image.open(infile[0])
                    source.image.save('%s.ico' % source.slug, File(open(infile[0])))
                    print 'Done %s' % source.url
                except:
                    # If anything at all goes wrong, fail silently (grabbing
                    # favicons isn't all that important annyway)
                    source.image = ''
                    source.save()
            except:
                # Print to stdout on failure
                print source.url