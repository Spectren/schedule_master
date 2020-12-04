from django.shortcuts import render
from django.contrib.auth import get_user

def home_page_views(request):

    data = {
        'user': get_user(request),
    }

    return render(request,'index.html', data)
