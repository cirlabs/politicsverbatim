import datetime
from django import template
from events.models import Event

register = template.Library()

@register.tag
def events_per_month(parser, token):
    bits = token.contents.split()
    if len(bits) != 2:
        raise template.TemplateSyntaxError(u'%s requires a date object')
    
    return EventsPerMonthNode(bits[1])

class EventsPerMonthNode(template.Node):
    def __init__(self, date):
        self.date = template.Variable(date)
    
    def render(self, context):
        date = self.date.resolve(context)
        return Event.objects.filter(event_datetime__year=date.year, event_datetime__month=date.month).count()
