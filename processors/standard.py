from django.conf import settings
from base.models import Campaign, Category, Document, Excerpt, Location, ExcerptType, CampaignTopic

def basic_context(request):
    '''
    A context processor to add several basic features common to each page
    '''
    
    guide_topics = list(set([c.topic for c in CampaignTopic.objects.all()]))
    guide_topics.sort(key=lambda x: x.name.lower())
    
    campaigns = Campaign.objects.all()
    categories = Category.objects.all()
    locations = Location.objects.all()
    types = ExcerptType.objects.all()
    document_count = Document.objects.filter(status="F").count()
    excerpt_count = Excerpt.objects.filter(document__status='F').count()
    return {'campaigns': campaigns,
            'categories': categories,
            'nav_categories': guide_topics[:10],
            'locations': locations,
            'types': types,
            'document_count': document_count,
            'excerpt_count': excerpt_count,
            'google_api_key': settings.GOOGLE_API_KEY,
            'facebook_app_id': settings.FACEBOOK_APP_ID}
