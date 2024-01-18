from django.db import models

# Create your models here.
# models.py
# new post cumunity form 
# main/models.py
from django.db import models

class Post(models.Model):
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

class Company(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    company_name = models.CharField(max_length=100)
    gstin = models.CharField(max_length=15)
    document = models.FileField(upload_to='company_documents/')
    password = models.CharField(max_length=100)


