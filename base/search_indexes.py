from haystack import indexes
from haystack import site
from base.models import Excerpt

class ExcerptIndex(indexes.RealTimeSearchIndex):
    text = indexes.CharField(document=True, use_template=True)

    def get_queryset(self):
        return Excerpt.objects.filter(document__status='F')

site.register(Excerpt, ExcerptIndex)
