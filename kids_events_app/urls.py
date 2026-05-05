from django.urls import path
from .views import calendar_view, get_data, get_places, get_events

urlpatterns = [
    path('', calendar_view, name='calendar'),
    path('api/data', get_data, name='get_data'),
    path("api/places", get_places, name="get_places"),
    path("api/events", get_events, name="get_events"),

]