from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls import url
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from HomePage.views import home_page_views
from Shedule.views import shedule_views
from .forms import RegisterForm
from django.conf import settings
from django.conf.urls.static import static

import Profile.views

urlpatterns = [
    re_path(r'^auth/register/$', Profile.views.SberRegistrationView.as_view(), name='django_registration_register'),
    path('admin/', admin.site.urls),
    re_path(r'^auth/login/$', LoginView.as_view(template_name='login.html')),
    re_path(r'^auth/logout/$', LogoutView.as_view(next_page='/')),
    url(r'^auth/', include('django_registration.backends.activation.urls')),
    url(r'^auth/', include('django.contrib.auth.urls')),
    re_path(r'^profile/$', Profile.views.profile_view, name='profile'),
    re_path(r'^progile_change/$', Profile.views.profile_change_view, name='profile_change'),
    re_path(r'^shedule/$', shedule_views),
    re_path(r'^$', home_page_views, name='home')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
