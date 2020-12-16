from django import forms
from django.contrib.auth.models import User
from django.forms import CharField, DateInput, FileInput, HiddenInput, ModelForm, ModelChoiceField
from django_registration.forms import RegistrationFormUniqueEmail

from .models import MentorData, TeamData, TrainerData


class UserFormMixin(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileFormMixin(ModelForm):
    class Meta:
        model = MentorData
        exclude = ['id']


class TrainerFormMixin(ModelForm):
    class Meta:
        model = TrainerData
        exclude = ['id']


class MixedRegistrationTrainerForm(UserFormMixin, ProfileFormMixin, TrainerFormMixin, RegistrationFormUniqueEmail):
    team = ModelChoiceField(queryset=TeamData.objects.all(), widget=HiddenInput())


class MixedRegistrationForm(UserFormMixin, ProfileFormMixin, RegistrationFormUniqueEmail):
    pass


class CustomClearableFileInput(FileInput):
    is_initial = False


class CustomDateInput(DateInput):
    input_type = "date"


class EditMentorForm(ModelForm):
    class Meta:
        model = MentorData
        exclude = ['id', 'owner']

        widgets = {
            "avatar": CustomClearableFileInput(),
            "birthday": CustomDateInput()
        }


class EditUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class EditProfileForm(EditUserForm, EditMentorForm):
    pass


class TeamGenerationForm(ModelForm):
    class Meta:
        model = TeamData
        fields = ['team_name']
