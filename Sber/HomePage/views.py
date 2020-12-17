from django.contrib.auth import get_user
from django.shortcuts import render


def home_page_views(request):
    data = {
        'user': get_user(request),
    }

    return render(request, 'index.html', data)
