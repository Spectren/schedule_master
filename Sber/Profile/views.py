from django.shortcuts import render

def profile_view(request):
    return render(request, 'profile.html')

def profile_change_view(request):
    return render(request, 'profile-change.html')
