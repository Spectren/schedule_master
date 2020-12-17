from django.shortcuts import render

<<<<<<< HEAD:Sber/Schedule/views.py
def schedule_views(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        
    return render(request, 'schedule.html')


=======

def schedule_views(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']

    return render(request, 'shedule.html')
>>>>>>> master:Sber/Shedule/views.py
