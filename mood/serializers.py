from rest_framework import serializers
from django.contrib.auth.models import User

from mood.models import Mood, MoodSense


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class MoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mood
        fields = '__all__'


class MoodSenseSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()

    def get_distance(self, obj):
        return str(getattr(obj, 'distance', 'no ref point'))

    class Meta:
        model = MoodSense
        fields = '__all__'
