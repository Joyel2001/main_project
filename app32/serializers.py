# serializers.py

from rest_framework import serializers
from .models import Feedback
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']  # Include any other fields you want to serialize

class FeedbackSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Use the UserSerializer to serialize the user field

    class Meta:
        model = Feedback
        fields = ['id', 'user', 'star_rating', 'message']



from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'subscription_expiration', 'subscription_duration']



# serializers.py
from rest_framework import serializers
from .models import EventBooking

class EventBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventBooking
        fields = ['booking_id', 'user', 'event', 'attendees']


