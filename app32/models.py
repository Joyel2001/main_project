from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, default=None)
    mobile_number = models.CharField(max_length=20, default="None")

    def __str__(self):
        return self.user.username


    

# addevent

from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    max_participants = models.IntegerField(default=0)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    event_id = models.CharField(max_length=20, primary_key=True, default=None)
    category = models.CharField(max_length=50, default=None, choices=[
        ('category1', 'Environmental Cleanup Campaign'),
        ('category2', 'Waste Management Seminar'),
        ('category3', 'Expo'),
        ('category4', 'Composting Workshop'),
        ('category5', 'Environmental Hackathon'),
        # Add more category options as needed
    ])
    def __str__(self):
        return self.event_id






# addbin
from django.db import models

class Bin(models.Model):
    
    bin_id = models.CharField(max_length=20, primary_key=True)  # Set as primary key
    title = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    capacity = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    def __str__(self):
        return self.title
    from django.db import models

class BinEvent(models.Model):
    bin_id = models.CharField(max_length=20, primary_key=True)  # Set as primary key
    title = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    capacity = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='bin_images/', null=True, blank=True)

    def __str__(self):
        return self.title


from django.db import models
from django.contrib.auth.models import User

class BinBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bin = models.ForeignKey(Bin, on_delete=models.CASCADE, related_name='bookings')
    house_number = models.CharField(max_length=50)
    landmark = models.CharField(max_length=100, default=None)  # New field for nearby landmark
    pin_code = models.CharField(max_length=10)
    bin_size = models.CharField(max_length=20)
    bin_capacity = models.CharField(max_length=20)
    collection_period = models.CharField(max_length=20, default=None)  # New field for collection period
    booking_id = models.CharField(max_length=5,default=None)  # New field for booking ID

    def __str__(self):
        return f"Booking {self.booking_id} for Bin {self.bin_id}: {self.bin.size} - {self.bin.capacity}"


    # eventbooking


from django.db import models
from django.contrib.auth.models import User  # If you're using Django's built-in User model
from .models import Event
from django.db import models
from django.contrib.auth.models import User  # Assuming User is the user model

class EventBooking(models.Model):
    booking_id = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=None)
    attendees = models.PositiveIntegerField()

    # Add any other fields you need for booking details

    def __str__(self):
        return f"Booking ID: {self.booking_id}, Event: {self.event.event_id}, User: {self.user.username}"

