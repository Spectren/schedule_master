from django.urls import path

from .views import generate_team, profile_change_view, profile_view, team_detail

urlpatterns = [
    path('create_team/', generate_team, name='team-create'),
    path('team/<int:pk>/', team_detail, name='team-detail'),
    path('change/', profile_change_view, name='profile-change'),
    path('', profile_view, name='profile-view'),
]
