from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import CompanyRegistration

class CompanyBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Use Q objects to perform a case-insensitive search on company_name or email_address
            user = CompanyRegistration.objects.get(Q(company_name__iexact=username) | Q(email_address__iexact=username))
        except CompanyRegistration.DoesNotExist:
            return None

        # Check the password using the correct method for your custom model
        if user.password == password:
            return user
        return None
