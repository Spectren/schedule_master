from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, request
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, FormView, TemplateView
from django_registration import signals
from django_registration.backends.activation.views import RegistrationView
from django.core.files.storage import default_storage
from django.conf import settings

from .forms import EditMentorForm, EditTrainerForm, EditUserForm, MentorRegistrationForm, TeamGenerationForm, \
    TrainerRegistrationForm
from .models import MentorData, TeamData, TrainerData
from Schedule.algo import SchedulerAlgorithm


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return {**context, **{
            'user': self.request.user,
            'teams': self.request.user.profile.teams.all(),
        }}


class ProfileChangeView(LoginRequiredMixin, TemplateView):
    template_name = 'profile_change.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        return {**context, **{
            'user_form': EditUserForm(instance=user),
            'mentor_form': EditMentorForm(instance=user.profile),
            'trainer_form': user.profile.is_trainer and EditTrainerForm(instance=user.trainer_profile) or None,
            'avatar': self.request.user.profile.avatar.url,
        }}

    def post(self, request, *args, **kwargs):
        user_form = EditUserForm(request.POST, instance=request.user)
        mentor_form = EditMentorForm(request.POST, request.FILES, instance=request.user.profile)
        trainer_form = (
                request.user.profile.is_trainer and
                EditTrainerForm(request.POST, instance=request.user.trainer_profile)
                or None
        )

        all_valid = (
                user_form.is_valid() and
                mentor_form.is_valid() and
                (trainer_form is None or trainer_form.is_valid())
        )

        if all_valid:
            user_form.save()
            mentor_form.save()
            trainer_form and trainer_form.save()
            return HttpResponseRedirect(reverse('profile-view'))
        else:
            return self.render_to_response({
                **self.get_context_data(**kwargs),
                **{
                    'user_form': user_form,
                    'mentor_form': mentor_form,
                    'trainer_form': trainer_form,
                }
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


@method_decorator(user_passes_test(lambda u: not u.profile.is_trainer), name='dispatch')
class TeamGenerationView(LoginRequiredMixin, FormView):
    template_name = 'generate_team.html'
    form_class = TeamGenerationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return {**context, **{
            'form': TeamGenerationForm()
        }}

    def form_valid(self, form):
        new_team = form.save(commit=False)
        new_team.mentor = self.request.user.profile
        new_team.save()

        return HttpResponseRedirect(reverse('team-detail', args=(new_team.pk,)))


class TeamDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'team'
    template_name = 'team.html'

    def get_queryset(self):
        return self.request.user.profile.teams.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return {**context, **{
            'user': self.request.user,
            'trainers_list': context['team'].trainers.all(),
        }}

    def post(self, request, *args, **kwargs):
        myfile = request.FILES['myfile']

        _ = default_storage.save(myfile.name, myfile)
        sa = SchedulerAlgorithm(f"{settings.MEDIA_ROOT}/{myfile.name}", ('2020/10/1', '2021/12/31'))
        lessons_table, _ = sa.create_schedule2()

        self.object = self.get_object()

        if isinstance(lessons_table, str):
            return self.render_to_response({**self.get_context_data(), **{"data": lessons_table}})

        elif not lessons_table['teachers']:
            return self.render_to_response({**self.get_context_data(), **{"data": 'Учителей нет'}})

        else:

            return self.render_to_response({**self.get_context_data(), **{"data": lessons_table}})
