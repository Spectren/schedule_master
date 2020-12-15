import django.forms as forms
from django.forms import TextInput
from django_registration.forms import RegistrationForm
from django.contrib.auth.models import User
from Profile.models import MentorData

class RegisterForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User