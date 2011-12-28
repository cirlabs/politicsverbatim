import datetime, urllib2, csv
from datetime import date
from base.models import *
from base.tools import cloudtools
from blog.models import Post
from events.models import Event
from socialmedia.tweets.models import *
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator
from django.template import RequestContext
from django.db.models import Q, Count
from django.http import HttpResponse

def homepage(request):
    """
    Front page view.
    """
    # Main section
    posts = Post.published_objects.all()[:4]
    excerpts = Excerpt.published_objects.all().order_by('-document__source_date',
                                                        '-date_entered')[:10]
    
    # Right rail
    tweets = Tweet.objects.all().order_by('-created_at')[:15]
    events = Event.objects.all().order_by('-event_datetime')[:10] 
    locations = Location.objects.all()
    category_list = Category.objects.all()

    return render_to_response('homepage.html', {
        'excerpts': excerpts,
        'events': events,
        'featured_post': posts[0],
        'posts': posts[1:4],
        'tweets': tweets}, context_instance=RequestContext(request))

def candidate_detail(request, slug):
    """
    Candidate detail pages.
    """
    candidate = get_object_or_404(Campaign, slug=slug)
    today = date.today()
    
    # Get upcoming events
    events = candidate.event_set.filter(event_datetime__gte=datetime.now()).order_by('-event_datetime')[:10]
    
    # Get paginated excerpts
    all_excerpts = candidate.excerpt_set.filter(document__status="F").order_by('-document__source_date')
    paginator = Paginator(all_excerpts, 15)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        excerpts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        excerpts = paginator.page(paginator.num_pages)
    
    # Get most recent tweets
    tweets = Tweet.objects.all().order_by('-created_at')

    # Create and render word cloud
    cloudinput = ''
    for item in all_excerpts:
        cloudinput += item.text.strip()
    cloudmaker = cloudtools.TagCloudMaker(cloudinput)
    cloud = cloudmaker.make_cloud_template()
 
    return render_to_response('base/candidate_detail.html', {
        'candidate': candidate,
        'cloud': cloud,
        'tweets': tweets[:10],
        'excerpts': excerpts,
        'events': events}, context_instance=RequestContext(request))

def topic_list(request):
    """
    Topics page list.
    """
    object_list = list(set([c.topic for c in CampaignTopic.objects.all()]))
    object_list.sort(key=lambda x: x.name.lower())

    return render_to_response('base/topic_list.html', {
        'object_list': object_list}, context_instance=RequestContext(request))
    
def topic_detail(request, slug):
    """
    Topics page detail.
    """
    topic = Category.objects.get(slug=slug)

    # Will return a CampaignTopic if it exists. Otherwise will return just a paginated list
    # of excerpts. Template accounts for this.
    campaign_topics = CampaignTopic.objects.filter(topic=topic).order_by('campaign__name')
    
    if campaign_topics:
        return render_to_response('base/topic_detail.html', {
            'campaign_topics': campaign_topics,
            'initial': campaign_topics[0],
            'topic': topic}, context_instance=RequestContext(request))
    else:
        all_excerpts = Excerpt.published_objects.filter(category__slug=topic.slug)
        
        # Get paginated excerpts
        paginator = Paginator(all_excerpts, 15)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        try:
            excerpts = paginator.page(page)
        except (EmptyPage, InvalidPage):
            excerpts = paginator.page(paginator.num_pages) 

        return render_to_response('base/topic_detail.html', {
            'topic': topic,
            'excerpts': excerpts}, context_instance=RequestContext(request))
   
def type_detail(request, slug):
    """
    Excerpt type list.
    """
    doctype = ExcerptType.objects.get(slug=slug)
    all_excerpts = get_list_or_404(Excerpt, type__slug=doctype.slug)
    all_excerpts.sort(key=lambda x: x.document.source_date, reverse=True)
    candidates = Campaign.objects.all()
    
    # Get paginated excerpts
    paginator = Paginator(all_excerpts, 15)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        excerpts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        excerpts = paginator.page(paginator.num_pages)    

    # Create and render word cloud
    cloudinput = ''
    for item in all_excerpts:
        cloudinput += item.text.strip()
    cloudmaker = cloudtools.TagCloudMaker(cloudinput)
    cloud = cloudmaker.make_cloud_template()
    
    return render_to_response('base/doctype_detail.html', {
        'doctype': doctype,
        'cloud': cloud,
        'excerpts': excerpts}, context_instance=RequestContext(request))

def search(request):
    """
    Search view.
    """
    excerpts = Excerpt.published_objects.all().order_by('-document__source_date')
    if request.GET:
        if request.GET.has_key('q'):
            qs = request.GET['q']
            if qs != '':
                from haystack.query import SearchQuerySet
                qs_unquote = urllib2.unquote(qs) 
                search_results = SearchQuerySet().auto_query(qs_unquote)
                ids = [o.pk for o in search_results]
                excerpts = excerpts.filter(id__in=ids)
        if request.GET.has_key('type'):
            type, type_slug = 'All excerpt types', 'all'
            if request.GET['type'] != 'all':
                type = ExcerptType.objects.get(slug=request.GET['type'])
                type_slug = type.slug
                excerpts = excerpts.filter(type=type)
        if request.GET.has_key('campaign'):
            campaign, campaign_slug = 'Brown and Whitman', 'all'
            if request.GET['campaign'] != 'all':
                campaign = Campaign.objects.get(slug=request.GET['campaign'])
                campaign_slug = campaign.slug
                excerpts = excerpts.filter(campaign=campaign)
        if request.GET.has_key('topic'):
            topic, topic_slug = 'All categories', 'all'
            if request.GET['topic'] != 'all':
                topic = Category.objects.get(slug=request.GET['topic'])
                topic_slug = topic.slug
                excerpts = excerpts.filter(category=topic)
        if request.GET.has_key('place'):
            location, location_slug = 'All locations', 'all'
            if request.GET['place'] != 'all':
                location = Location.objects.get(slug=request.GET['place'])
                location_slug = location.slug
                excerpts = excerpts.filter(document__location=location)
    
        getstr = 'type=%s&campaign=%s&topic=%s&place=%s' % (type_slug, campaign_slug, topic_slug, location_slug)
    
    # Return no-results page
    if len(excerpts) == 0:
        return render_to_response('base/search_results.html', {
            'type': type,
            'campaign': campaign,
            'topic': topic,
            'location': location,
            'type_slug': type_slug, 
            'campaign_slug': campaign_slug,
            'topic_slug': topic_slug,
            'location_slug': location_slug,
            'no_results': True}, context_instance=RequestContext(request))
    
    # Paginate excerpts
    paginator = Paginator(excerpts, 15)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        paginated_excerpts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        paginated_excerpts = paginator.page(paginator.num_pages) 

    # Create and render word cloud 
    cloudinput = ''
    for item in excerpts:
        cloudinput += item.text.strip()
    cloudmaker = cloudtools.TagCloudMaker(cloudinput)
    cloud = cloudmaker.make_cloud_template()

    return render_to_response('base/search_results.html', {
        'get': getstr,
        'excerpts': paginated_excerpts,
        'type_slug': type_slug, 
        'campaign_slug': campaign_slug,
        'topic_slug': topic_slug,
        'location_slug': location_slug,
        'cloud': cloud}, context_instance=RequestContext(request))

def timeline_csv(request):
    """
    View to generate CSV for right rail charts.
    """
    if request.GET.has_key('topic'):
        topic = Category.objects.get(slug=request.GET['topic'])
    else:
        topic = False
        
    if request.GET.has_key('campaign'):
        campaign = Campaign.objects.get(slug=request.GET['campaign'])
    else:
        campaign = False
    
    # Create the HTTP response
    response = HttpResponse(mimetype='text/csv')
    writer = csv.writer(response)
    
    excerpt_counts = Excerpt.objects.filter(
        document__status='F',
        category=topic,
        campaign=campaign).values('document__source_date').annotate(
        count=Count('document__source_date'))
    
    if excerpt_counts:
       for e in excerpt_counts:
            writer.writerow([e['document__source_date'], e['count']])
    else:
        writer.writerow(['2009', 0])
        writer.writerow([date.today(), 0])
    
    return response

def widget(request):
    """
    View to create embeddable widget.
    """
    excerpts = Excerpt.published_objects.order_by('-document__source_date')
    
    headline_type = 'Statements'
    # Todo: Phase out this hard-coding for database solution
    pluralize_dict = {
        'all': 'Statements',
        'attack': 'Candidate attacks',
        'assertion-fact': 'Assertions of fact',
        'promise': 'Promises',
        'no-comment': 'Deflections',
        'policy-position-proposal': 'Policy positions',
        'prediction': 'Predictions',
        'promise': 'Promises',
        'quotable': 'Quotables',
        'specific-policy-point-details': 'Policy specifics',
    }
    
    template = 'widgets/widget.html'
    
    if request.GET:
        if request.GET.has_key('campaign'):
            campaign, campaign_slug = 'Brown and Whitman', 'all'
            if request.GET['campaign'] != 'all':
                try:
                    campaign = Campaign.objects.get(slug=request.GET['campaign'])
                    campaign_slug = campaign.slug
                    excerpts = excerpts.filter(campaign=campaign).distinct()
                except:
                    pass
        if request.GET.has_key('type'):
            type, type_slug = 'All excerpt types', 'all'
            if request.GET['type'] != 'all':
                try:
                    type = ExcerptType.objects.get(slug=request.GET['type'])
                    type_slug = type.slug
                    excerpts = excerpts.filter(type=type).distinct()
                    headline_type = pluralize_dict[type_slug]
                except:
                    headline_type = 'Statements'
        logo_getstr = ''
        if request.GET.has_key('logo'):
            if request.GET['logo'] == 'small':
                template = 'widgets/widget_nologo.html'
                logo_getstr = 'logo=small&'

        paginator = Paginator(excerpts, 1)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        try:
            paginated_excerpts = paginator.page(page)
        except (EmptyPage, InvalidPage):
            paginated_excerpts = paginator.page(paginator.num_pages)
        
        getstr = 'type=%s&campaign=%s&%s' % (type_slug, campaign_slug, logo_getstr)
        
        return render_to_response(template, {
            'excerpts': paginated_excerpts,
            'getstr': getstr,
            'headline_type': headline_type,
            'campaign': campaign,
            'type': type,
            'campaign_slug': campaign_slug,
            'type_slug': type_slug}, context_instance=RequestContext(request))