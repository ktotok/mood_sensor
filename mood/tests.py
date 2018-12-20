from django.contrib.gis.geos import Point
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.utils import json

from mood.models import MoodSense, Mood
from django.contrib.auth.models import User


class MoodSenseViewTest(APITestCase):
    client = APIClient()

    def setUp(self):
        self.mood_model_dict = {}
        # Mood creation
        for mood in Mood.MOOD_CHOICES:
            obj = Mood.objects.create(name=mood[1])
            self.mood_model_dict[mood[0]] = obj

        # Create User
        User.objects.create(username='Chet Baker')
        self.user = User.objects.get()

        self.client.force_login(user=User.objects.first())

    def test_get_mood_frequency(self):
        MoodSense.objects.create(user_id=self.user,
                                 point=Point(10.0, 10.0, srid=4326),
                                 mood_state_id=self.mood_model_dict['Happy'])
        MoodSense.objects.create(user_id=self.user,
                                 point=Point(10.0, 20.0, srid=4326),
                                 mood_state_id=self.mood_model_dict['Happy'])
        MoodSense.objects.create(user_id=self.user,
                                 point=Point(20.0, 10.0, srid=4326),
                                 mood_state_id=self.mood_model_dict['Sad'])

        response = self.client.get(
            reverse("mood_sense"),
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_content = json.loads(response.content)
        self.assertEqual(len(json_content), 2)
        happy_mood_count = [m['mood_freq'] for m in json_content if m['mood_state_id'] == 1][0]
        self.assertEqual(happy_mood_count, 2)

        sad_mood_count = [m['mood_freq'] for m in json_content if m['mood_state_id'] == 2][0]
        self.assertEqual(sad_mood_count, 1)

    def test_get_mood(self):
        response = self.client.get(
            reverse('moods'),
            format="json", )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)['results']), 3)

    def test_add_mood_sense(self):
        mood_data = {
            'location': {
                "longitude": 30.728073120118,
                "latitude": 46.509933471679,
            },
            'mood_state_id': self.mood_model_dict['Happy'].pk
        }

        response = self.client.post(
            reverse('mood_sense'),
            mood_data,
            format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        actual_user = MoodSense.objects.filter(user_id__exact=self.user)
        self.assertEqual(len(actual_user), 1)

    def test_get_nearest_happy_place(self):
        nearest = MoodSense.objects.create(user_id=self.user,
                                 point=Point(10.0, 10.0, srid=4326),
                                 mood_state_id=self.mood_model_dict['Happy'])

        MoodSense.objects.create(user_id=self.user,
                                 point=Point(11.0, 10.0, srid=4326),
                                 mood_state_id=self.mood_model_dict['Sad'])

        faraway = MoodSense.objects.create(user_id=self.user,
                                 point=Point(10.0, 20.0, srid=4326),
                                 mood_state_id=self.mood_model_dict['Happy'])

        sting_user = User.objects.create(username='Sting')
        MoodSense.objects.create(user_id=sting_user,
                                 point=Point(10.0, 10.0, srid=4326),
                                 mood_state_id=self.mood_model_dict['Happy'])

        response = self.client.get(
            reverse('nearest_happy_point'),
            {"long": 10.0, "lat": 12.0},
            format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_content = json.loads(response.content)
        self.assertEqual(json_content[0]['id'], nearest.pk)
        self.assertEqual(json_content[1]['id'], faraway.pk)
