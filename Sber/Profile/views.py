from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django_registration import signals
from django_registration.backends.activation.views import RegistrationView

from .forms import EditMentorForm, EditTrainerForm, EditUserForm, MentorRegistrationForm, TeamGenerationForm, \
    TrainerRegistrationForm
from .models import MentorData, TeamData, TrainerData


@login_required
def profile_view(request):
    return render(request, 'profile.html', context={
        'username': request.user,
        'teams': request.user.profile.teams.all(),
    })


def profile_change_view(request):
    trainer_form = None

    if request.method == "POST":
        user_form = EditUserForm(data=request.POST, instance=request.user)
        mentor_form = EditMentorForm(data=request.POST, files=request.FILES, instance=request.user.profile)

        if user_form.is_valid() and mentor_form.is_valid():
            user_form.save()
            mentor_form.save()
            trainer_form.save()

        if request.user.profile.is_trainer:
            trainer_form = EditTrainerForm(data=request.POST, instance=request.user.trainer_profile)
            if trainer_form.is_valid():
                trainer_form.save()

        return HttpResponseRedirect(reverse('profile'))
    else:
        user_form = EditUserForm(instance=request.user)
        mentor_form = EditMentorForm(instance=request.user.profile)
        if request.user.profile.is_trainer:
            trainer_form = EditTrainerForm(instance=request.user.trainer_profile)

    return render(request, 'profile_change.html', context={
        "user_form": user_form,
        "mentor_form": mentor_form,
        "trainer_form": trainer_form,
        "avatar": request.user.profile.avatar.url,
    })


class MentorRegistrationView(RegistrationView):
    form_class = MentorRegistrationForm
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

        signals.user_registered.send(
            sender=self.__class__, user=user, request=self.request
        )

        return user


class TrainerRegistrationView(RegistrationView):
    form_class = TrainerRegistrationForm
    success_url = reverse_lazy("django_registration_complete")

    def register(self, form):
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
        trainer_data.owner = user
        trainer_data.save()

        signals.user_registered.send(
            sender=self.__class__, user=user, request=self.request
        )

        return user

    def get_form(self, form_class=None):
        form_class = form_class or self.get_form_class()
        form = super().get_form(form_class=form_class)
        form.fields['team'].initial = TeamData.objects.get(pk=self.kwargs.get('team_pk'))

        return form


@login_required
def generate_team(request):
    user = request.user

    if user.profile.is_trainer:
        return HttpResponse('Вы - тренер, вы не имеете права создавать команды.')

    if request.method == 'POST':
        form = TeamGenerationForm(data=request.POST)

        if form.is_valid():
            new_team = form.save(commit=False)
            new_team.mentor = user.profile
            new_team.save()

            return HttpResponseRedirect(reverse('team-detail', args=(new_team.pk,)))
    else:
        form = TeamGenerationForm()

    return render(request, 'generate_team.html', {
        'form': form
    })


@login_required
def team_detail(request, pk):
    user = request.user
    team = get_object_or_404(TeamData, pk=pk)

    if not user.profile.teams.filter(pk=team.pk).exists():
        raise Http404

    return render(request, 'team.html', {
        'team': team,
        'user': user,
        'trainers_list': team.trainers.all(),
    })
