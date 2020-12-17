from django.contrib import admin

from .models import MentorData, TeamData, TrainerData

admin.site.register([MentorData, TeamData, TrainerData])
