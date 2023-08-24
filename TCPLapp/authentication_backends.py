from django.contrib.auth.backends import ModelBackend
from .models import Registration

class RegistrationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Registration.objects.get(username=username)
            if user.check_password(password):
                return user
        except Registration.DoesNotExist:
            return None