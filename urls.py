from django.conf.urls.defaults import *
from django.contrib import admin
from blog.models import Post
from base.models import *
from feeds.feeds import *

admin.autodiscover()

urlpatterns = patterns('',
    # Base URLs
    url(r'^$', 'base.views.homepage', name='homepage'),
    (r'^robots.txt$', 'django.views.generic.simple.direct_to_template', {'template':'robots.txt', 'mimetype':'text/plain'}),
    (r'^widget/$', 'base.views.widget'),
                       
    # Admin URLs
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^tinymce/', include('tinymce.urls')),
    
    # Search URLs
    url(r'^search/', 'base.views.search', name='search'),                   
    
    # Candidate URLs
    url(r'^candidates/(?P<slug>.+)/feed/$', CandidateFeed(), name='candidate_feed'),
    url(r'^candidates/(?P<slug>.+)/$', 'base.views.candidate_detail', name='candidate_detail'),
    url(r'^candidates/$', 'django.views.generic.list_detail.object_list', {
        'queryset': Campaign.objects.all(),
        'template_name': 'base/candidate_list.html'},
        name='candidate_list'),
    
    # Event URLs
    url(r'^event/(?P<id>\d+)/$', 'events.views.event_detail', name='event_detail'),
    url(r'^events/$', 'events.views.event_list', name='event_list'),
    url(r'^events/(?P<year>\d{4})/$', 'events.views.event_year', name='event_year'),
    url(r'^events/(?P<year>\d{4})/(?P<month>\d{2})/$', 'events.views.event_month', name='event_month'),
    url(r'^events/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 'events.views.event_day', name='event_day'),
    
    # Blog URLs (generics)
    url(r'^blog/$', 'django.views.generic.list_detail.object_list', {
        'queryset': Post.published_objects.all(),
        'paginate_by': 10,
        'template_name': 'blog/blog_home.html',
        'extra_context': {'dates': Post.published_objects.all().dates('publication_date', 'month'), 'count': Post.published_objects.all().count()}},
        name='blog_home'),
    url(r'^blog/(?P<year>\d{4})/(?P<month>.+)/$', 'django.views.generic.date_based.archive_month', {
        'queryset': Post.published_objects.all(),
        'date_field': 'publication_date',
        'template_name': 'blog/blog_home.html',
        'extra_context': {'dates': Post.published_objects.all().dates('publication_date', 'month'), 'count': Post.published_objects.all().count()}},
        name='blog_month'),
    url(r'^blog/(?P<slug>.+)/$', 'django.views.generic.list_detail.object_detail', {
        'queryset': Post.objects.all(),
        'template_name': 'blog/blog_detail.html',
        'extra_context': {'dates': Post.published_objects.all().dates('publication_date', 'month'), 'count': Post.published_objects.all().count()}},
        name='blog_detail'),
        
    # Topic URLs
    url(r'^topics/(?P<slug>.+)/feed/$', ExcerptCategoryFeed(), name='topic_feed'),
    url(r'^topics/(?P<slug>.+)/$', 'base.views.topic_detail', name='topic_detail'),
    url(r'^topics/$', 'base.views.topic_list', name='topic_detail'),

    # Type URLs
    url(r'^type/(?P<slug>.+)/feed/$', ExcerptTypeFeed(), name='type_feed'),
    url(r'^type/(?P<slug>.+)/$', 'base.views.type_detail', name='type_detail'),

    # Excerpt URLs
    url(r'^excerpt/(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', {
        'queryset': Excerpt.objects.filter(document__status='F'),
        'template_name': 'base/excerpt_detail.html'},
        name='excerpt_detail'),
    
    # Base feed URLs
    (r'^feeds/excerpts/$', LatestExcerptsFeed()),
    url(r'^feeds/blog/$', LatestPostsFeed(), name='blog_feed'),
    url(r'^feeds/events/$', LatestEventsFeed(), name='events_feed'),
    
    # Misc URLs
    url(r'^csv/', 'base.views.timeline_csv', name='csv'),  

)
