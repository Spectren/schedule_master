from django.shortcuts import render
from django.conf import settings

def shedule_views(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        
    return render(request, 'shedule.html')
