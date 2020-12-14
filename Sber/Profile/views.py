from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    return render(request, 'profile.html', context={
        'user': request.user,
    })

def profile_change_view(request):
    return render(request, 'profile_change.html')