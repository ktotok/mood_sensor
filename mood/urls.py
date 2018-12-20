from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from mood.views import ListMood, ListCreateMoodSense, RetrieveNearestHappyPointView

urlpatterns = {
    url(r'^moods/$', ListMood.as_view(), name='moods'),
    url(r'^mood_sense/$', ListCreateMoodSense.as_view(), name='mood_sense'),
    url(r'^happy_location/$', RetrieveNearestHappyPointView.as_view(), name='nearest_happy_point'),
}

urlpatterns = format_suffix_patterns(urlpatterns)
