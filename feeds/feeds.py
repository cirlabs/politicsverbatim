from django.contrib.syndication.views import Feed
from django.contrib.syndication.views import FeedDoesNotExist
from django.shortcuts import get_object_or_404
from base.models import *
from events.models import *
from blog.models import Post

class LatestExcerptsFeed(Feed):
    title = "Politics Verbatim | Latest excerpts"
    link = "/"
    description = "Latest excerpts added to politicsverbatim.org."

    def items(self):
        return Excerpt.objects.filter(document__status='F').order_by('-date_entered')[:25]

    def item_title(self, item):
        return str(item.campaign) + ' on ' + ', '.join([c.name.lower() for c in item.category.all()])

    def item_description(self, item):
        return item.text
    
    def item_link(self, item):
        return 'http://www.politicsverbatim.org/excerpt/%s/' % str(item.id)
    
    def item_pubdate(self,item):
        return item.date_entered


class LatestEventsFeed(Feed):
    title = "Politics Verbatim | Latest events"
    link = "/events/"
    description = "Latest events added to politicsverbatim.org."

    def items(self):
        return Event.objects.all().order_by('-created_date')[:25]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description
    
    def item_link(self, item):
        return 'http://www.politicsverbatim.org/event/%s/' % str(item.id)
    
    def item_pubdate(self,item):
        return item.created_date


class LatestPostsFeed(Feed):
    title = "Politics Verbatim | On Message blog"
    link = "/blog/"
    description = "Latest blog posts added to On Message."

    def items(self):
        return Post.published_objects.all()[:10]

    def item_title(self, item):
        return item.headline

    def item_description(self, item):
        return item.body
    
    def item_link(self, item):
        return 'http://www.politicsverbatim.org/excerpt/%s/' % str(item.slug)
    
    def item_pubdate(self,item):
        return item.publication_date


class CandidateFeed(Feed):
    def get_object(self, request, slug):
        return get_object_or_404(Campaign, slug=slug)

    def title(self, obj):
        return "Politics Verbatim | %s " % obj.name
    
    def link(self, obj):
        return 'http://www.politicsverbatim.org/candidates/%s/' % obj.slug
    
    def description(self, obj):
        return "Latest excerpts added to politicsverbatim.org about %s." % obj.name

    def items(self, obj):
        return Excerpt.objects.filter(document__status='F', campaign=obj).order_by('-date_entered')[:25]

    def item_title(self, item):
        return str(item.campaign) + ' on ' + ', '.join([c.name.lower() for c in item.category.all()])

    def item_description(self, item):
        return item.text
    
    def item_link(self, item):
        return 'http://www.politicsverbatim.org/excerpt/%s/' % str(item.id)

    def item_pubdate(self,item):
        return item.date_entered


class ExcerptCategoryFeed(Feed):
    def get_object(self, request, slug):
        return get_object_or_404(Category, slug=slug)

    def title(self, obj):
        return "Politics Verbatim | %s " % obj.name
    
    def link(self, obj):
        return 'http://www.politicsverbatim.org/topics/%s/' % obj.slug
    
    def description(self, obj):
        return "Latest excerpts added to politicsverbatim.org about %s." % obj.name.lower()

    def items(self, obj):
        return Excerpt.objects.filter(document__status='F', category=obj).order_by('-date_entered')[:25]

    def item_title(self, item):
        return str(item.campaign) + ' on ' + ', '.join([c.name.lower() for c in item.category.all()])

    def item_description(self, item):
        return item.text
    
    def item_link(self, item):
        return 'http://www.politicsverbatim.org/excerpt/%s/' % str(item.id)

    def item_pubdate(self,item):
        return item.date_entered


class ExcerptTypeFeed(Feed):
    def get_object(self, request, slug):
        return get_object_or_404(ExcerptType, slug=slug)

    def title(self, obj):
        return "Politics Verbatim | %s " % obj.name
    
    def link(self, obj):
        return 'http://www.politicsverbatim.org/type/%s/' % obj.slug
    
    def description(self, obj):
        return "Latest excerpts added to politicsverbatim.org about %s." % obj.name.lower()

    def items(self, obj):
        return Excerpt.objects.filter(document__status='F', type=obj).order_by('-date_entered')[:25]

    def item_title(self, item):
        return str(item.campaign) + ' on ' + ', '.join([c.name.lower() for c in item.category.all()])

    def item_description(self, item):
        return item.text
    
    def item_link(self, item):
        return 'http://www.politicsverbatim.org/excerpt/%s/' % str(item.id)

    def item_pubdate(self,item):
        return item.date_entered

