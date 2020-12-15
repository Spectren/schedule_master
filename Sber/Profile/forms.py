from django.forms import ModelForm
from django.contrib.auth.models import User
from django_registration.forms import RegistrationFormUniqueEmail
from .models import MentorData

class UserFormMixin(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileFormMixin(ModelForm):
    class Meta:
        model = MentorData
        exclude = ['id']

class MixedRegistrationForm(UserFormMixin, ProfileFormMixin, RegistrationFormUniqueEmail):
    pass

class EditMentorForm(ModelForm):
    class Meta:
        model  = MentorData
        exclude = ['id', 'owner']

class EditUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class EditProfileForm(EditUserForm, EditMentorForm):
    pass