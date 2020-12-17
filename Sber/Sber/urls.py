from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls import url
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django_registration.backends.activation.views import RegistrationView
from django_registration.forms import RegistrationForm
from HomePage.views import home_page_views
from Schedule.views import sсhedule_views
from .forms import RegisterForm

import Profile.views

urlpatterns = [
    re_path(r'^auth/register/$', RegistrationView.as_view(form_class=RegisterForm, template_name='django_registration/registration_form.html', success_url='/auth/register/complete'), name='django_registration_register'),
    path('admin/', admin.site.urls),
    re_path(r'^auth/login/$', LoginView.as_view(template_name='login.html')),
    re_path(r'^auth/logout/$', LogoutView.as_view(next_page='/')),
    url(r'^auth/', include('django_registration.backends.activation.urls')),
    url(r'^auth/', include('django.contrib.auth.urls')),
    re_path(r'^profile/$', Profile.views.profile_view),
    re_path(r'^shedule/$', sсhedule_views),
    re_path(r'^$', home_page_views)
]
