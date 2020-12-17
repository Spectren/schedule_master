from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import default_storage
from django.conf import settings
from .algo import SchedulerAlgorithm


def sсhedule_views(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']

        file_name = default_storage.save(myfile.name, myfile)
        sa = SchedulerAlgorithm(f"{settings.MEDIA_ROOT}/{myfile.name}", ('2020/10/1', '2021/12/31'))
        lessons_table = sa.create_schedule2()

        if isinstance(lessons_table, str):
            return render(request, 'new.html', {"data": lessons_table })

        elif not lessons_table['teachers']:
            return render(request, 'new.html', {"data": 'Учителей нет' })

        else:
            return render(request, 'new.html', {"data": lessons_table })

    return render(request, 'shedule.html')
