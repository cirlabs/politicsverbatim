import datetime
from base.models import *
from base.tools import cloudtools
from events.models import Event
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator
from django.template import RequestContext

def event_list(request):
    """
    Standard list view for campaign events. We just as easily could have done
    all of these event views as generics, but we planned to add more advanced
    calendar functionality (though we never actually did).
    """
    all_events = Event.upcoming_events.all().order_by('-event_datetime')
    dates = Event.objects.all().dates('event_datetime', 'month')

    paginator = Paginator(all_events, 15)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        paginated_events = paginator.page(page)
    except (EmptyPage, InvalidPage):
        paginated_events = paginator.page(paginator.num_pages)
    
    return render_to_response('events/event_list.html', {
        'paginated_events': paginated_events,
        'all_events': all_events,
        'dates': dates}, context_instance=RequestContext(request))

def event_year(request, year):
    """
    Events by year.
    """
    all_events = Event.objects.filter(event_datetime__year=year).order_by('-event_datetime')
    dates = all_events.dates('event_datetime', 'month')

    paginator = Paginator(all_events, 15)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        paginated_events = paginator.page(page)
    except (EmptyPage, InvalidPage):
        paginated_events = paginator.page(paginator.num_pages)
    
    return render_to_response('events/event_list.html', {
        'paginated_events': paginated_events,
        'all_events': all_events,
        'dates': dates}, context_instance=RequestContext(request))

def event_month(request, year, month):
    """
    Events by month.
    """
    all_events = Event.objects.filter(event_datetime__year=year,
                                      event_datetime__month=month).order_by('-event_datetime')
    dates = all_events.dates('event_datetime', 'month')

    paginator = Paginator(all_events, 15)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        paginated_events = paginator.page(page)
    except (EmptyPage, InvalidPage):
        paginated_events = paginator.page(paginator.num_pages)
    
    return render_to_response('events/event_list.html', {
        'paginated_events': paginated_events,
        'all_events': all_events,
        'dates': dates}, context_instance=RequestContext(request))

def event_day(request, year, month, day):
    """
    Events by day.
    """
    all_events = Event.objects.filter(event_datetime__year=year,
                                      event_datetime__month=month,
                                      event_datetime__day=day).order_by('-event_datetime')
    dates = all_events.dates('event_datetime', 'month')

    paginator = Paginator(all_events, 15)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        paginated_events = paginator.page(page)
    except (EmptyPage, InvalidPage):
        paginated_events = paginator.page(paginator.num_pages)
    
    return render_to_response('events/event_list.html', {
        'paginated_events': paginated_events,
        'all_events': all_events,
        'dates': dates}, context_instance=RequestContext(request))
    
def event_detail(request, id):
    """
    Single event detail view.
    """
    all_events = Event.upcoming_events.all()
    event = Event.objects.get(pk=id)
    dates = Event.objects.all().dates('event_datetime', 'month')
    
    return render_to_response('events/event_detail.html', {
        'event': event,
        'events': all_events,
        'dates': dates}, context_instance=RequestContext(request))