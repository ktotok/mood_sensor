from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.db.models import CASCADE


class Mood(models.Model):
    MOOD_CHOICES = (
        ('Happy', 'happy'),
        ('Sad', 'sad'),
        ('Neutral', 'neutral')
    )

    name = models.CharField(
        max_length=12,
        choices=MOOD_CHOICES
    )

    def __str__(self):
        return f"{self.name}"


class MoodSense(models.Model):
    user_id = models.ForeignKey(User, on_delete=CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    point = models.PointField()
    mood_state_id = models.ForeignKey(Mood, on_delete=CASCADE)
