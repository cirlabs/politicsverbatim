from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Source(models.Model):
    """
    Source of the document being entered, whether a media outlet, candidate Web
    site, etc.
    """
    name = models.CharField(max_length=100,
                            help_text='The name of the source. Ex. San Jose Mercury News, megwhitman.com, etc.')
    slug = models.SlugField(max_length=255, unique=True,
                            help_text=(u"Built automatically. Do not change unless you know what you're doing."))
    url = models.URLField(verify_exists=True, blank=True,
                          help_text='If the source has a Web site, enter here')
    image = models.ImageField(upload_to='images/source/',
                              blank=True, help_text='Typically favicon')
    
    class Meta:
        ordering = ['name']
    
    def __unicode__(self):
        return self.name

class DocumentType(models.Model):
    """
    The type of source material being entered: A newspaper story, attack ad,
    policy paper, etc.
    """
    name = models.CharField(max_length=100,
                            help_text='The type of document you are entering. Ex. News article, live appearance, etc.')
    slug = models.SlugField(max_length=255,
                            unique=True,
                            help_text=(u"Built automatically. Do not change unless you know what you're doing."))
    
    class Meta:
        ordering = ['name']
    
    def __unicode__(self):
        return self.name

class ExcerptType(models.Model):
    """
    The type of statement being made: Promises, statements of fact, etc.
    """
    name = models.CharField(max_length=100,
                            help_text='The type of document you are entering. Ex. News article, live appearance, etc.')
    slug = models.SlugField(max_length=255,
                            unique=True,
                            help_text=(u"Built automatically. Do not change unless you know what you're doing."))
    
    class Meta:
        ordering = ['name']
    
    def __unicode__(self):
        return self.name

class Campaign(models.Model):
    """
    The campaign behind the document.
    """
    name = models.CharField(max_length=100)
    race = models.CharField(max_length=1, choices=(('G', 'Governor'), ('S', 'Senate')))
    image = models.ImageField(upload_to='images/campaigns/',
                              blank=True, help_text='Candidate mug or other image for excerpts')
    topic_image = models.ImageField(upload_to='images/campaigns/',
                                    blank=True, help_text='Larger mug for topic and candidate pages')
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=255,
                            unique=True,
                            help_text=(u"Built automatically. Do not change unless you know what you're doing."))
    
    class Meta:
        ordering = ['name']
    
    def __unicode__(self):
        return self.name

class Location(models.Model):
    """
    Event and document locations.
    """
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    lat = models.CharField(max_length=15, blank=True)
    lng = models.CharField(max_length=15, blank=True)
    slug = models.SlugField(max_length=100,
                            unique=True,
                            help_text=(u"Built automatically. Do not change unless you know what you're doing."))
    
    class Meta:
        ordering = ['state', 'city']
    
    def __unicode__(self):
        return '%s, %s' % (self.city, self.state)

class Category(models.Model):
    """
    Topical categories designed to let people drill down on the 
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255,
                            unique=True,
                            help_text=(u"Built automatically. Do not change unless you know what you're doing."))
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'
    
    def __unicode__(self):
        return self.name

class Document(models.Model):
    """
    The actual source material being entered. Newspaper story, video clip, transcript,
    policy paper, etc.
    """
    name = models.CharField(max_length=255, help_text='A title for the document')
    slug = models.SlugField(max_length=255,
                            unique=True,
                            help_text=(u"Built automatically. Do not change unless you know what you're doing.")) 
    source = models.ForeignKey(Source)
    type = models.ForeignKey(DocumentType)
    quality = models.CharField(max_length=1, choices=(('P', 'Primary'), ('S', 'Secondary')))
    source_date = models.DateField(help_text='The day the material was sourced. Publication date, event date, etc.')
    date_entered = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True,
                            help_text='If the source is a Web site or document, copy the text here')
    url = models.URLField(blank=True,
                          help_text='If the document is available on the Web, link to it here')
    file = models.FileField(upload_to='documents/',
                            blank=True,
                            help_text='If the document is a file, upload it here')
    location = models.ForeignKey(Location, blank=True, null=True)
    status = models.CharField(max_length=1, choices=(('F', 'Finished'), ('N', 'Needs processing')))
    
    class Meta:
        ordering = ['-date_entered']
    
    def __unicode__(self):
        return self.name

class PublishedExcerptManager(models.Manager):
    """
    Published excerpt manager.
    """
    def get_query_set(self):
        return super(PublishedExcerptManager, self).get_query_set().filter(document__status='F')
    
class Excerpt(models.Model):
    """
    Chunks from the documents that can be directly attributed to the candidate.
    Things like quotes, direct statements, etc.
    """
    document = models.ForeignKey(Document)
    text = models.TextField()
    category = models.ManyToManyField(Category, blank=True)
    campaign = models.ForeignKey(Campaign)
    type = models.ManyToManyField(ExcerptType, blank=True, null=True)
    date_entered = models.DateTimeField(auto_now_add=True)
    # Managers
    objects = models.Manager()
    published_objects = PublishedExcerptManager()

    class Meta:
        ordering = ['-document__source_date']
    
    def __unicode__(self):
        return '%s: %s ...' % (str(self.id), self.text[:50])
    
    @models.permalink
    def get_facebook_url(self):
        return ('excerpt_detail', (), {
            'object_id': self.id,
        })

class CampaignTopic(models.Model):
    """
    Describes the position of a candidate or campaign on a particular topic, along
    with a selection of supporting excerpts.
    """
    campaign = models.ForeignKey(Campaign)
    topic = models.ForeignKey(Category)
    position = models.TextField()
    supporting_excerpts = models.ManyToManyField(Excerpt, blank=True, null=True)
    
    class Meta:
        ordering = ['topic__name']
    
    def __unicode__(self):
        return '%s on %s' % (self.campaign, self.topic)

########## NOTE RDF MAPPING EXPERIMENT ##########

class ExcerptRelation(models.Model):
    """
    Types of relationships that can be created between excerpts. For RDF mapping.
    """
    relation_name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255,
                            unique=True,
                            help_text=(u"Built automatically. Do not change unless you know what you're doing."))

    def __unicode__(self):
        return self.display_name

class ExcerptMapping(models.Model):
    subject_excerpt = models.ForeignKey(Excerpt, related_name='subject_excerpt')
    relation = models.ForeignKey(ExcerptRelation)
    object_excerpts = models.ManyToManyField(Excerpt, related_name='object_excerpt')