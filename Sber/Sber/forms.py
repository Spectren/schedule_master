import django.forms as forms
from django_registration.forms import RegistrationForm
from Profile.models import Mentors

class RegisterForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = Mentors
        fields = ['username', 'email', 'first_name', 'last_name', 'patronymic', 'password1']
        labels = {
            "password1": "Пароль"
        }