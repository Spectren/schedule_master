import django.forms as forms
from django_registration.forms import RegistrationForm

class RegisterForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        fields = ['username', 'email', 'first_name', 'last_name', 'password1']
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "password1": "Пароль"
        }