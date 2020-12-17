from django.shortcuts import render


def schedule_views(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']

    return render(request, 'shedule.html')
