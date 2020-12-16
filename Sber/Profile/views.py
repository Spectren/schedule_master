from pprint import pprint

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django_registration.backends.activation.views import RegistrationView

from .forms import EditMentorForm, EditUserForm, MixedRegistrationForm, MixedRegistrationTrainerForm, TeamGenerationForm
from .models import MentorData, TeamData, TrainerData


@login_required
def profile_view(request):
    return render(request, 'profile.html', context={
        'username': request.user,
    })


def profile_change_view(request):
    if request.method == "POST":
        user_form = EditUserForm(data=request.POST, instance=request.user)
        mentor_form = EditMentorForm(data=request.POST, files=request.FILES, instance=request.user.profile)

        if user_form.is_valid() and mentor_form.is_valid():
            user_form.save()
            mentor_form.save()
            return HttpResponseRedirect(reverse('profile'))
    else:
        user_form = EditUserForm(instance=request.user)
        mentor_form = EditMentorForm(instance=request.user.profile)

    return render(request, 'profile_change.html', context={
        "user_form": user_form,
        "mentor_form": mentor_form,
        "avatar": request.user.profile.avatar.url,
    })


class SberRegistrationView(RegistrationView):
    form_class = MixedRegistrationForm
    success_url = reverse_lazy("django_registration_complete")

    def register(self, form):
        user = super().register(form)

        profile_data = MentorData(**{
            field: value
            for field, value in form.cleaned_data.items()
            if field in {*MentorData._meta.get_fields()} - {'owner'}
        })

        profile_data.owner = user
        profile_data.save()

        return user


class TrainerRegistrationView(RegistrationView):
    form_class = MixedRegistrationTrainerForm
    success_url = reverse_lazy("django_registration_complete")

    def register(self, form):
        print('Test me')
        user = super().register(form)

        profile_data = MentorData(**{
            field: value
            for field, value in form.cleaned_data.items()
            if field in MentorData._meta.get_fields()
        })

        profile_data.owner = user
        profile_data.save()

        trainer_data = TrainerData(**{
            field: value
            for field, value in form.cleaned_data.items()
            if value in {*TrainerData._meta.get_fields()} - {'team'}
        })

        trainer_data.team = form.cleaned_data['team']
        trainer_data.save()

        return user

    def get_form(self, form_class=None):
        form_class = form_class or self.get_form_class()
        form = super().get_form(form_class=form_class)
        form.fields['team'].initial = TeamData.objects.get(pk=self.kwargs.get('team_pk'))

        return form


@login_required
def generate_team(request):
    user = request.user

    if request.method == 'POST':
        form = TeamGenerationForm(data=request.POST)

        if form.is_valid():
            new_team = form.save(commit=False)
            new_team.mentor = user.profile
            new_team.save()

            return render(request, 'generate_team_response.html', {
                'team': new_team.pk,
            })
    else:
        form = TeamGenerationForm()

    return render(request, 'generate_team.html', {
        'form': form
    })
