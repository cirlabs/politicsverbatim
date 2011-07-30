import Image, urllib, urlparse
from django.core.files import File
from base.models import Source

sources = Source.objects.all()

for source in sources:
    if source.url:
        try:
            infile = urllib.urlretrieve('http://' + urlparse.urlparse(source.url)[1] + '/favicon.ico')
            try:
                im = Image.open(infile[0])
                source.image.save('%s.ico' % source.slug, File(open(infile[0])))
                print 'Done %s' % source.url
            except:
                source.image = ''
                source.save()
        except:
            print source.url
