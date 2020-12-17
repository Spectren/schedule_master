from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path

from HomePage.views import home_page_views
from Profile.views import MentorRegistrationView, TrainerRegistrationView
from Schedule.views import sсhedule_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', include('Profile.urls')),
    path('auth/register/train_ref/<int:team_pk>/', TrainerRegistrationView.as_view(), name='team-ref'),
    path('auth/register/', MentorRegistrationView.as_view(), name='django_registration_register'),
    path('auth/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('auth/logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('auth/', include('django_registration.backends.activation.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path(r'schedule/', sсhedule_views),
    path(r'', home_page_views, name='home')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
