from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import default_storage
from json2html import json2html
from django.conf import settings
from .algo import SchedulerAlgorithm


def shedule_views(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        #print(myfile)
        file_name = default_storage.save(myfile.name, myfile)
        sa = SchedulerAlgorithm(f"{settings.MEDIA_ROOT}/{myfile.name}", ('2020/10/1', '2021/12/31'))
        lessons_table = sa.create_schedule2()
        # lessons_table = SA.create_schedule()
        # names = {0: "Газизова Зубаржат",
        #          1: "Гончарова Ирина",
        #          2: "Каракачан Евгения",
        #          3: "Матусевич Илья",
        #          4: "Мошкина Марагарита",
        #          5: "Некрасова Ольга",
        #          6: "Патаров Пархат",
        #          7: "Проскурина Юлия",
        #          8: "Смагина Наталья",
        #          9: "Стрелкова Елена",
        #          10: "Сурина Ирина",
        #          11: "Сычев Геннадий",
        #          12: "Тимофеева Наталья",
        #          13: "Филиппов Денис",
        #          14: "Ханжин Александр",
        #          15: "Шилова Татьяна",
        #          16: "Щербич Марина"}
        #
        # for i in range(17):
        #     lessons_table.loc[lessons_table['Teacher'] == i, 'Teacher'] = names[i]

        #lessons_table = lessons_table.sample(frac=1)
        # return render(request, 'new.html', {
        #     "data": lessons_table.to_html(index=False, classes='table table-striped', justify='center'),
        # })
        if isinstance(lessons_table, str):
            return render(request, 'new.html', {"data": lessons_table, })

        elif not lessons_table['teachers']:
            return render(request, 'new.html', {"data": 'Учителей нет', })

        else:
            return render(request, 'new.html', {"data": json2html.convert(json=lessons_table), })

    return render(request, 'shedule.html')
