from django.contrib.gis.db.models.functions import Distance
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from django.db.models import Count
from rest_framework import status, viewsets, permissions
from rest_framework import generics
from rest_framework.response import Response

from mood.models import Mood, MoodSense
from mood.serializers import MoodSerializer, MoodSenseSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ListMood(generics.ListAPIView):
    queryset = Mood.objects.all()
    serializer_class = MoodSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ListCreateMoodSense(generics.ListCreateAPIView):
    queryset = MoodSense.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user_model = request.user
        longitude = request.data['location']['longitude']
        latitude = request.data['location']['latitude']
        point_object = Point(longitude, latitude, srid=4326)

        mood_id = request.data['mood_state_id']
        mood_model = Mood.objects.filter(id__exact=mood_id)
        if len(mood_model) == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        MoodSense.objects.create(user_id=user_model, point=point_object, mood_state_id=mood_model[0])

        return Response(status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        user_model = request.user

        result = MoodSense.objects.filter(user_id__exact=user_model) \
            .values('mood_state_id'). \
            annotate(mood_freq=Count('mood_state_id'))

        return Response(list(result))


class RetrieveNearestHappyPointView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user_model = self.request.user
        latitude = self.request.query_params.get('lat')
        longitude = self.request.query_params.get('long')

        target_point = Point(float(longitude), float(latitude), srid=4326)

        happy_mood = Mood.objects.get(name="happy")
        queryset = MoodSense.objects.filter(user_id=user_model,
                                                   mood_state_id=happy_mood) \
            .annotate(distance=Distance("point", target_point)) \
            .order_by("distance")
        return queryset

    def list(self, request, *args, **kwargs):
        happy_locations = self.get_queryset()
        serializer = MoodSenseSerializer(happy_locations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
