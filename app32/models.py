from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, default="", blank=True)
    mobile_number = models.CharField(max_length=20, default="None")
    subscribed=models.BooleanField(default=False)
    subscription_expiration = models.DateField(null=True, blank=True)
    subscription_duration = models.PositiveIntegerField(default=0)

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
    number_of_bins = models.PositiveIntegerField(default=0)  
    def __str__(self):
        return self.title
    from django.db import models

from django.db import models

class BinEvent(models.Model):
    bin_id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    capacity = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='bin_images/', null=True, blank=True)
    number_of_bins = models.PositiveIntegerField(default=0)  # Add this field

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
    booking_id = models.CharField(primary_key=True,max_length=5)  # New field for booking ID

    def __str__(self):
        return f"{self.booking_id}"  # Only return the booking ID
                                                                       


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
    

    # bookingststus
from django.db import models
from app32.models import Bin  # Assuming you have a 'Bin' model defined in your 'app32' app

class BookedBinStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    booking = models.ForeignKey('BinBooking', on_delete=models.CASCADE, related_name='statuses')
    fill_level = models.PositiveIntegerField(choices=[(20, '20%'), (40, '40%'), (50, '50%'), (70, '70%'), (90, '90%')], null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.status_id)

  # Convert status_id to a string and return it


# notification

from django.db import models

class Message(models.Model):
    # Fields for the message model
    description = models.TextField()
    
    def __str__(self):
        return f"Message {self.id}"



# wastefill_status
from django.db import models

class WasteCollection(models.Model):
    id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(BinBooking, on_delete=models.CASCADE)
    collection_status = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now=True)  # Auto-generate timestamp on creation
    datestamp = models.DateField(auto_now=True)      # Auto-generate datestamp on creation

    def __str__(self):
        return f"Collection ID: {self.id}"


    
# model for bin booking for home
class BinBookingEvent(models.Model):
    booking_id = models.AutoField(primary_key=True)  # Primary key for the booking
    bin = models.ForeignKey(BinEvent, on_delete=models.CASCADE)  # ForeignKey to link to a Bin
    event_date_time = models.DateTimeField()
    event_location = models.CharField(max_length=255)
    delivery_time = models.DateTimeField()
    pickup_time = models.DateTimeField()
    number_of_bins_needed = models.PositiveIntegerField()  # New field for the number of bins needed

    def __str__(self):
        return str(self.booking_id) 
    


# payment

# models.py

from django.db import models
from django.contrib.auth.models import User

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=255,default=None)
    payment_id = models.CharField(max_length=255)
    signature = models.CharField(max_length=255,default=None)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment by {self.user.username}"


    
    


# Feedback
from django.db import models
from django.contrib.auth.models import User  # Import the User model

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Add a foreign key to User
    star_rating = models.IntegerField()
    message = models.TextField()

    def __str__(self):
        return f"Feedback ID: {self.id}"




# waste_classifier/models.py


# coin
    
from django.db import models
from django.contrib.auth.models import User

class SuperCoin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)

    def __str__(self):
        return f"Super Coins - {self.user.username}"
