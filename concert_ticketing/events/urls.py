# events/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import EventViewSet, TicketViewSet  # Import from events/api.py
from django.urls import path
from . import views  # Add this import statement

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'tickets', TicketViewSet)

urlpatterns = [
    path('', views.events_list, name='events_list'),  # Your existing view
    path('api/', include(router.urls)),  # Add API endpoints here
]