from django_registration.backends.activation.views import RegistrationView 
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .models import MentorData
from .forms import EditMentorForm, MixedRegistrationForm, EditProfileForm, EditUserForm

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
            if field not in {'username', 'password1', 'password2', 'email', 'first_name', 'last_name'}
        })

        profile_data.owner = user
        profile_data.save()

        return user