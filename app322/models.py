from django.db import models
from django.utils import timezone


# Create your models here.
# models.py
# new post cumunity form 
# main/models.py
from django.db import models

from django.contrib.auth.models import User  # Import the User model

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=0)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



# like
from django.db import models
from django.contrib.auth.models import User
  # Import Post model from your app

class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"


# comment

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=0)

    def __str__(self):
        return f"Comment for {self.post.title}"
    

    # company registeration model
    # models.py
from django.db import models

# models.py
from django.db import models

class CompanyRegistration(models.Model):
    company_name = models.CharField(max_length=255)
    owners_shareholders_names = models.TextField()
    vat_registration_number = models.CharField(max_length=20)
    business_address = models.TextField()
    email_address = models.EmailField(unique=True)
    password = models.CharField(max_length=255,default=0)
    business_license_document = models.FileField(upload_to='company_documents/')

    def __str__(self):
        return self.company_name
    

# seller registertion
    # models.py
from django.db import models

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,default=0)   
    email = models.EmailField()
    company_name = models.CharField(max_length=100)
    gstin = models.CharField(max_length=15)
    document = models.FileField(upload_to='company_documents/')
    password = models.CharField(max_length=100)


# Tender_Details
    
# models.py
from django.db import models

# models.py
from django.db import models

class Tender(models.Model):
    TENDER_TYPE_CHOICES = [
        ('open', 'Open Tender'),
        ('closed', 'Closed Tender'),
        # Add more choices as needed
    ]

    TENDER_CATEGORY_CHOICES = [
        ('waste_disposal', 'Waste Disposal'),
        # Add more choices as needed
    ]

    PAYMENT_MODE_CHOICES = [
        ('offline', 'Offline Payment'),
        ('online', 'Online Payment'),
        # Add more choices as needed
    ]

    title = models.CharField(max_length=255)
    organisation_chain = models.CharField(max_length=50)
    tender_type = models.CharField(max_length=50, choices=TENDER_TYPE_CHOICES)
    tender_category = models.CharField(max_length=50, choices=TENDER_CATEGORY_CHOICES)
    reference_number = models.CharField(max_length=50)
    closing_date = models.DateField()
    bid_opening_date = models.DateField()
    payment_mode = models.CharField(max_length=50, choices=PAYMENT_MODE_CHOICES)

    def __str__(self):
        return self.title

def tender_closing_within(self):
        # Calculate the time remaining for closing
        now = timezone.now()
        time_remaining = self.closing_date - now

        # Extract days and seconds from the timedelta object
        days = time_remaining.days
        seconds = time_remaining.seconds

        # Calculate hours, minutes, and remaining seconds
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Construct the formatted string
        formatted_time = f"{days} days, {hours} hours, {minutes} minutes"

        return formatted_time