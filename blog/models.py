import datetime
from django.db import models
from django.contrib.auth.models import User
from base.models import Campaign, Excerpt, Category, Document

class PublishedManager(models.Manager):
    def get_query_set(self):
        return super(PublishedManager, self).get_query_set().filter(publication_status='P', publication_date__lte=datetime.datetime.now()).order_by('-publication_date')

class Post(models.Model):
    headline = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, help_text=(u"Built automatically. Do not change unless you know what you're doing."))
    body = models.TextField(help_text='Enter your blog post text here')
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_date = models.DateTimeField(auto_now=True, db_index=True)
    publication_date = models.DateTimeField(help_text='Set future date for delayed publishing', db_index=True)
    publication_status = models.CharField(max_length=1, choices=(('D','Draft'), ('P', 'Published')))
    author = models.ForeignKey(User)
    image = models.ImageField(upload_to='ontherecord/posts/images/', blank=True, help_text='Large horizontal image')

    # Managers
    objects = models.Manager()
    published_objects = PublishedManager()

    class Meta:
        ordering = ['-publication_date']

    def __unicode__(self):
        return self.headline

    @models.permalink
    def get_absolute_url(self):
        return ('blog_detail', [self.slug])

