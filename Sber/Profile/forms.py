from django.contrib.auth.models import User
from django.forms import DateInput, FileInput, HiddenInput, ModelChoiceField, ModelForm
from django_registration.forms import RegistrationFormUniqueEmail

from .models import MentorData, TeamData, TrainerData


class UserFormMixin(ModelForm):
    class Meta:
        model = User
        exclude = ['id', 'date_joined', 'password']


class MentorFormMixin(ModelForm):
    class Meta:
        model = MentorData
        fields = ['patronymic']


class TrainerFormMixin(ModelForm):
    class Meta:
        model = TrainerData
        exclude = ['id']


class MentorRegistrationForm(UserFormMixin, MentorFormMixin, RegistrationFormUniqueEmail):
    pass


class TrainerRegistrationForm(MentorRegistrationForm, TrainerFormMixin):
    team = ModelChoiceField(queryset=TeamData.objects.all(), widget=HiddenInput())


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


class EditTrainerForm(ModelForm):
    class Meta:
        model = TrainerData
        exclude = ['id', 'owner', 'team']
        widgets = {
            "vacation_start": CustomDateInput()
        }


class TeamGenerationForm(ModelForm):
    class Meta:
        model = TeamData
        fields = ['team_name']
