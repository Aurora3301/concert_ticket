# events/views.py
from django.shortcuts import render
from rest_framework.test import APIRequestFactory
from .api import EventViewSet

def events_list(request):
    factory = APIRequestFactory()
    request = factory.get('/api/events/')
    event_viewset = EventViewSet.as_view({'get': 'list'})
    response = event_viewset(request)
    events = response.data
    return render(request, 'events/events.html', {'events': events})