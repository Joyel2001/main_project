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

from django.contrib.auth.models import User
from django.db import models

class CompanyApplyForTender(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE)
    application_date = models.DateField(auto_now_add=True)
    
    # Registration details
    amount = models.PositiveIntegerField()
    license_number = models.CharField(max_length=50)
    nature_of_business = models.CharField(max_length=50)
    legal_entity_type = models.CharField(max_length=50)
    
    # Approval status
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} applied for {self.tender.title} on {self.application_date}"



class ApprovedTender(models.Model):
    registration = models.OneToOneField('CompanyApplyForTender', on_delete=models.CASCADE, primary_key=True)
    approval_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.registration.user.username}'s tender registration approved on {self.approval_date}"

class RejectedTender(models.Model):
    registration = models.OneToOneField(CompanyApplyForTender, on_delete=models.CASCADE, primary_key=True)
    rejection_date = models.DateField(auto_now_add=True)
    rejection_reason = models.TextField()

    def __str__(self):
        return f"{self.registration.user.username}'s tender registration rejected on {self.rejection_date}"





from django.db import models
from .models import Tender

class Waste(models.Model):
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE,default=0)
    average_waste = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    recyclable_waste = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    e_waste = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    hazardous_waste = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    organic_waste = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    other_category = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Waste for Tender: {self.tender.title}"



# product caegory
    
class Category(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    image = models.ImageField(upload_to="category_images", null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0=default,1=Hidden")
    trending = models.BooleanField(default=False, help_text="0=default,1=Hidden")
    description = models.CharField(max_length=500, null=False, blank=False, default="Default description")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# sub  product caegory
    
class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=500, null=False, blank=False, default="Default subcategory description")
    image = models.ImageField(upload_to="subcategory_images", null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False, help_text="0=default, 1=Hidden")
    trending = models.BooleanField(default=False, help_text="0=default, 1=Trending")

    def __str__(self):
        return self.name



# add product 
    

from django.db import models

class Product(models.Model):
    subcategory = models.ForeignKey('Subcategory', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=0)
    name = models.CharField(max_length=100, null=False, blank=False)
    product_image = models.ImageField(upload_to="product_images", null=False, blank=False)
    description = models.CharField(max_length=500, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    original_price = models.FloatField(null=False, blank=False)
    selling_price = models.FloatField(null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0=default,1=Hidden")
    trending = models.BooleanField(default=False, help_text="0=default,1=Trending")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    
    image = models.ImageField(upload_to='cart_item_images/', blank=True, null=True)  # Add image field

    def _str_(self):
        return f"{self.user.username}'s Cart Item - {self.product.product_name}"

    # def save(self, *args, **kwargs):
    #     # Calculate the price based on the product's price per kg and the quantity
    #     self.price = self.product.product_price * self.quantity
    #     super().save(*args, **kwargs)


    
from django.db import models

class Student(models.Model):
    stuname = models.CharField(max_length=100)
    eemail = models.CharField(max_length=100)  # Corrected typo in max_length

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Add any additional fields you want for your custom user model here
    # For example:
    # bio = models.TextField(max_length=500, blank=True)

    # Provide unique related_name attributes for groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_permissions'
    )




from django.db import models
from django.contrib.auth.models import User

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'product']  # Ensures a product can only be added to the wishlist once per user

    def __str__(self):
        return f"{self.user.username}'s Wishlist - {self.product.name}"
