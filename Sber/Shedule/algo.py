import pandas as pd
from random import choice
import numpy as np
from collections import defaultdict
from operator import itemgetter
from json import dumps

# tmp_table = pd.read_excel("./Таблица с переменными и данными.xlsx", sheet_name='Таблица с занятиями')
#
# del tmp_table['lesson_id']
#
#
# specs = ['csgo', 'dota', 'apex', 'wot']
#
#
# a = [None]*340
# for i in range(len(a)):
#     a[i] = choice(specs)
#
#
# tmp_table['lesson_specialization'] = a
#
#
# tmp_table.to_excel('таблица занятий.xlsx')


class SchedulerAlgorithm:
    def preprocess_file(self, lessons_excel: str):
        lesson_table = pd.read_excel(lessons_excel, sheet_name='Sheet1')
        return lesson_table

    def set_teacher_id_to_workdays(self, teachers_table):
        teacher_id_to_workdays_ = {}
        planning_range = ('2020/10/1', '2020/12/31')
        ru_holidays_2021 = pd.to_datetime(['2021.01.01', '2021.01.02', '2021.01.03', '2021.01.04', '2021.01.05',
                                           '2021.01.06', '2021.01.07', '2021.01.08', '2021.02.23', '2021.03.08',
                                           '2021.05.01', '2021.05.09', '2021.06.12', '2021.11.04', '2020.11.04'])

        for teacher_id, teacher in teachers_table.iterrows():
            holidays = teacher['trainer_vacation']
            teacher_id_to_workdays_[teacher_id] = self.create_workday_list2(planning_range, holidays, ru_holidays_2021)

        return teacher_id_to_workdays_

    def __init__(self, excel_file_path_name: str):
        self.lesson_table = self.preprocess_file(excel_file_path_name)
        self.lesson_table = pd.read_excel(excel_file_path_name, sheet_name='Sheet1')
        self.teachers_table = pd.read_excel(r'C:\Users\DIVANCO\PycharmProjects\schedule_master\Sber\Shedule\таблица учителей.xlsx')
        self.teachers_table['teachers_load'] = 0
        self.teacher_id_to_workdays = self.set_teacher_id_to_workdays(self.teachers_table)
        self.np_lesson_table = np.array(self.lesson_table)

    def create_workday_list2(self, range_of_planning, worker_holidays, country_holidays):
        p_start, p_end = range_of_planning

        if worker_holidays != worker_holidays: # If worker_holidays == nan
            return pd.bdate_range(start=p_start, end=p_end, holidays=country_holidays, freq='C').to_list()

        else:
            h_start, h_end = worker_holidays.split('-')
            holidays_list = pd.date_range(start=h_start, end=h_end).tolist()
            holidays_list += country_holidays
            return pd.bdate_range(start=p_start, end=p_end, holidays=holidays_list, freq='C').to_list()


#teachers_table.at[2, 'teachers_load'] = 1 # Добавление значения в конкретную ячейку

# Выборка по специализиции учителя
# csgo = teachers_table[teachers_table['trainer_specialization'].str.contains('csgo')]#.copy(deep=False)

    def create_schedule(self, random=False):
        if random:
            np.random.shuffle(self.np_lesson_table)  # Перетасовывание массива для случайного распределения занятий

        ret = defaultdict(list)
        #ret = {i: [] for i in self.teachers_table.index}

        for lesson in self.np_lesson_table:
            lesson_id = lesson[0] # Id занятия
            lesson_specialization = lesson[1] # Специализация занятия
            lesson_duration_days = lesson[2] # Длительность занятия в днях
            lesson_duration_hours = lesson[3] # Длительность занятия в часах
            number_of_trainers = lesson[4] # Количество тренеров, которые будут проводить занятие
            # = lesson[5] # Название урока и доп инфа

            suitable_teachers = self.teachers_table[self.teachers_table['trainer_specialization'].str.contains(lesson_specialization)]
            suitable_teacher_id = [] # Id тренера или тренеров, которым назначено занятие
            lesson_date_time = [] # Дата или даты (если урок идёт несколько дней) проведения уроков

            if number_of_trainers == 1:
                suitable_teacher_id.append(suitable_teachers['teachers_load'].idxmin())

                suitable_time = self.teachers_table.iloc[suitable_teacher_id[0]]['lesson_start']
                h = suitable_time.hour
                m = suitable_time.minute

                for part_of_the_lesson in range(lesson_duration_days):
                    lesson_date = self.teacher_id_to_workdays[suitable_teacher_id[0]].pop(0)
                    lesson_date = lesson_date.replace(hour=h, minute=m)
                    lesson_date_time.append(lesson_date)
                    self.teachers_table.at[suitable_teacher_id[0], 'teachers_load'] += lesson_duration_hours / lesson_duration_days

            else:
                suitable_teacher_id = suitable_teachers.nsmallest(number_of_trainers, 'teachers_load').index
                each_teacher_workdays = []

                for st_id in suitable_teacher_id:
                        each_teacher_workdays.append(set(self.teacher_id_to_workdays[st_id]))

                workdays_intersection = each_teacher_workdays[0]

                for i in range(1, len(each_teacher_workdays)):
                    workdays_intersection = workdays_intersection.intersection(each_teacher_workdays[i])

                suitable_time = max(suitable_teachers.loc[suitable_teacher_id, 'lesson_start'])
                h = suitable_time.hour
                m = suitable_time.minute

                for part_of_the_lesson in range(lesson_duration_days):
                    selected_lesson_workday = min(workdays_intersection)
                    lesson_date = selected_lesson_workday.replace(hour=h, minute=m)
                    lesson_date_time.append(lesson_date)
                    workdays_intersection.remove(selected_lesson_workday)

                    for st_id in suitable_teacher_id:
                        self.teacher_id_to_workdays[st_id].remove(selected_lesson_workday)
                        self.teachers_table.at[st_id, 'teachers_load'] += lesson_duration_hours / lesson_duration_days

            print('Учителю/лям с id =', *suitable_teacher_id, 'назначено занятие с id =', lesson_id,
                  'и специализацией', lesson_specialization, 'на', *list(map(str, lesson_date_time)))

            for t_id in suitable_teacher_id:
                ret[t_id].extend(
                    (lesson_id, lesson_specialization, timestamp.strftime("%m/%d/%Y, %H:%M:%S"))
                    for timestamp in lesson_date_time
                )

        pandas_source = []

        for t_id in ret.keys():
            for datum in ret[t_id]:
                pandas_source.append((t_id, *datum))

        ret = pd.DataFrame(pandas_source, columns=['Teacher', 'Lesson', 'Spec', 'Date'])
        return ret

    def create_schedule2(self):
        ret = []
        for lesson in self.np_lesson_table:
            lesson_id = lesson[0]  # Id занятия
            lesson_specialization = lesson[1]  # Специализация занятия
            lesson_duration_days = lesson[2]  # Длительность занятия в днях
            lesson_duration_hours = lesson[3]  # Длительность занятия в часах
            number_of_trainers = lesson[4]  # Количество тренеров, которые будут проводить занятие
            lesson_title = lesson[5] # Название урока и доп инфа

            suitable_teachers = self.teachers_table[
                self.teachers_table['trainer_specialization'].str.contains(lesson_specialization)]
            suitable_teacher_id = []  # Id тренера или тренеров, которым назначено занятие
            lesson_date_time = []  # Дата или даты (если урок идёт несколько дней) проведения уроков

            if number_of_trainers == 1:
                suitable_teacher_id.append(suitable_teachers['teachers_load'].idxmin())

                suitable_time = self.teachers_table.iloc[suitable_teacher_id[0]]['lesson_start']
                h = suitable_time.hour
                m = suitable_time.minute

                for part_of_the_lesson in range(lesson_duration_days):
                    lesson_date = self.teacher_id_to_workdays[suitable_teacher_id[0]].pop(0)
                    lesson_date = lesson_date.replace(hour=h, minute=m)
                    lesson_date_time.append(lesson_date)
                    self.teachers_table.at[
                        suitable_teacher_id[0], 'teachers_load'] += lesson_duration_hours / lesson_duration_days

                    # return
                    ret.append([suitable_teacher_id[0], lesson_id, lesson_specialization, lesson_date, lesson_title,
                                self.teachers_table.at[suitable_teacher_id[0], 'trainer_name']])

            elif number_of_trainers > 1:
                suitable_teacher_id = suitable_teachers.nsmallest(number_of_trainers, 'teachers_load').index
                each_teacher_workdays = []

                for st_id in suitable_teacher_id:
                    each_teacher_workdays.append(set(self.teacher_id_to_workdays[st_id]))

                workdays_intersection = each_teacher_workdays[0]

                for i in range(1, len(each_teacher_workdays)):
                    workdays_intersection = workdays_intersection.intersection(each_teacher_workdays[i])

                suitable_time = max(suitable_teachers.loc[suitable_teacher_id, 'lesson_start'])
                h = suitable_time.hour
                m = suitable_time.minute

                for part_of_the_lesson in range(lesson_duration_days):
                    selected_lesson_workday = min(workdays_intersection)
                    lesson_date = selected_lesson_workday.replace(hour=h, minute=m)
                    lesson_date_time.append(lesson_date)
                    workdays_intersection.remove(selected_lesson_workday)

                    for st_id in suitable_teacher_id:
                        self.teacher_id_to_workdays[st_id].remove(selected_lesson_workday)
                        self.teachers_table.at[st_id, 'teachers_load'] += lesson_duration_hours / lesson_duration_days

                        # return
                        ret.append([st_id, lesson_id, lesson_specialization, lesson_date, lesson_title,
                                    self.teachers_table.at[st_id, 'trainer_name']])

            else:
                print('Количество учителей не может быть меньше 1')
                break

            print('Учителю/лям с id =', *suitable_teacher_id, 'назначено занятие с id =', lesson_id,
                  'и специализацией', lesson_specialization, 'на', *list(map(str, lesson_date_time)))

        json_ret = {'teachers': []}
        prev_r = None
        i = -1
        for r in sorted(ret, key=itemgetter(0, 3)):
            if r[0] != prev_r:
                i += 1
                prev_r = r[0]
                json_ret["teachers"].append(
                    {
                        "teacher_id": r[0],
                        "teacher_name": r[4],
                        # "specializations": "wot, csgo",
                        # "trainer_vacation": null,
                        # "lesson_start": "10:00:00",
                        # "load": 108,
                        "lessons": [
                            {
                                "lesson_id": r[1],
                                "lesson_datetime": r[3],
                                "lesson_specialization": r[2],
                                "lesson_title": r[5]
                            }
                        ]
                    }
                )

            elif r[0] == prev_r:
                json_ret["teachers"][i]["lessons"].append(
                    {
                        "lesson_id": r[1],
                        "lesson_datetime": r[3],
                        "lesson_specialization": r[2],
                        "lesson_title": r[5]
                    }
                )

        # def np_encoder(object):
        #     if isinstance(object, np.generic):
        #         return object.item()

        # ret_string = json.dumps(json_ret, default=np_encoder)

        return json_ret


if __name__ == '__main__':
    SA = SchedulerAlgorithm("./таблица занятий с несколькими учителями.xlsx")
    res = SA.create_schedule()
    print(res)

