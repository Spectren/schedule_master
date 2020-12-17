from django.urls import path

from .views import ProfileChangeView, ProfileView, TeamDetailView, TeamGenerationView

urlpatterns = [
    path('create_team/', TeamGenerationView.as_view(), name='team-create'),
    path('team/<int:pk>/', TeamDetailView.as_view(), name='team-detail'),
    path('change/', ProfileChangeView.as_view(), name='profile-change'),
    path('', ProfileView.as_view(), name='profile-view'),
]
