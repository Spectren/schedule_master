import pandas as pd
from random import choice
import numpy as np
from collections import defaultdict
from operator import itemgetter
from json import dumps, dump
import holidays

class SchedulerAlgorithm:
    def preprocess_file(self, lessons_excel: str):
        try:
            return pd.read_excel(lessons_excel)  # , sheet_name='Sheet1')
        except:
            return []

    def set_teacher_id_to_workdays(self, teachers_table, planning_range):
        teacher_id_to_workdays_ = {}
        ru_holidays = holidays.RU()

        for teacher_id, teacher in teachers_table.iterrows():
            trainer_vacation = teacher['trainer_vacation']
            teacher_id_to_workdays_[teacher_id] = self.create_workday_list2(planning_range, trainer_vacation,
                                                                            ru_holidays[planning_range[0]:
                                                                                        planning_range[1]])

        return teacher_id_to_workdays_

    def __init__(self, excel_file_path_name: str, planning_range):
        self.lesson_table = self.preprocess_file(excel_file_path_name)
        self.teachers_table = pd.read_excel(r'./Schedule/таблица учителей.xlsx')
        self.teachers_table['teachers_load'] = 0
        self.teacher_id_to_workdays = self.set_teacher_id_to_workdays(self.teachers_table, planning_range)
        self.np_lesson_table = np.array(self.lesson_table)

    def create_workday_list2(self, range_of_planning, worker_holidays, country_holidays):
        p_start, p_end = range_of_planning

        if (worker_holidays != worker_holidays):
            return pd.bdate_range(start=p_start, end=p_end, holidays=country_holidays, freq='C').to_list()
        else:
            h_start, h_end = worker_holidays.split('-')
            holidays_list = pd.date_range(start=h_start, end=h_end).tolist()
            holidays_list += country_holidays
            return pd.bdate_range(start=p_start, end=p_end, holidays=holidays_list, freq='C').to_list()

    def create_schedule2(self):
        ret = []
        if len(self.np_lesson_table) == 0:
            return {'teachers': []}, []

        if self.np_lesson_table.shape[1] != 6:
            return 'Ваша таблица имеет неверное количество столбцов'

        # free_teachers_id = [i for i in range(len(self.teachers_table))]
        # last_lesson_id = -1

        for lesson in self.np_lesson_table:
            # if len(free_teachers_id) == 0:
            #     last_lesson_id = lesson[0]
            #     break

            lesson_id = lesson[0]  # Id занятия
            lesson_specialization = lesson[1]  # Специализация занятия
            lesson_duration_days = lesson[2]  # Длительность занятия в днях
            lesson_duration_hours = lesson[3]  # Длительность занятия в часах
            number_of_trainers = lesson[4]  # Количество тренеров, которые будут проводить занятие
            lesson_title = lesson[5]  # Название урока и доп инфа

            #free_teachers = self.teachers_table.loc[self.teachers_table.index.isin(free_teachers_id)]
            # suitable_teachers = self.teachers_table.loc[self.teachers_table.index.isin(free_teachers_id)][
            #    self.teachers_table['trainer_specialization'].str.contains(lesson_specialization)]
            suitable_teachers = self.teachers_table[
                self.teachers_table['trainer_specialization'].str.contains(lesson_specialization)]
            lesson_date_time = []  # Дата или даты (если урок идёт несколько дней) проведения уроков
            # Id свободного тренера или тренеров, которым назначено занятие
            suitable_teacher_id = []

            if number_of_trainers == 1:
                try:
                    suitable_teacher_id.append(suitable_teachers['teachers_load'].idxmin())
                except:
                    continue
                    # print("Нет подходящих учителей")
                    # return "Нет подходящих учителей под одно из занятий"

                suitable_time = self.teachers_table.iloc[suitable_teacher_id[0]]['lesson_start']
                h = suitable_time.hour
                m = suitable_time.minute

                for part_of_the_lesson in range(lesson_duration_days):
                    try:
                        lesson_date = self.teacher_id_to_workdays[suitable_teacher_id[0]].pop(0)
                    except:
                        #free_teachers_id.remove(suitable_teacher_id[0])
                        break

                        # print("слишком мало учителей")

                    lesson_date = lesson_date.replace(hour=h, minute=m)
                    lesson_date_time.append(lesson_date)

                    lesson_duration = lesson_duration_hours / lesson_duration_days

                    self.teachers_table.at[
                        suitable_teacher_id[0], 'teachers_load'] += lesson_duration

                    # return
                    ret.append(
                        [suitable_teacher_id[0], lesson_id, lesson_specialization, str(lesson_date), lesson_title,
                         self.teachers_table.at[suitable_teacher_id[0], 'trainer_name'], lesson_duration])

            elif number_of_trainers > 1:
                try:
                    suitable_teacher_id = suitable_teachers.nsmallest(number_of_trainers, 'teachers_load').index
                except:
                    continue
                    # print("Нет подходящих учителей")
                    # return "Нет подходящих учителей под одно из занятий"

                each_teacher_workdays = []

                for st_id in suitable_teacher_id:
                    each_teacher_workdays.append(set(self.teacher_id_to_workdays[st_id]))

                try:
                    workdays_intersection = each_teacher_workdays[0]
                except:
                    continue

                for i in range(1, len(each_teacher_workdays)):
                    workdays_intersection = workdays_intersection.intersection(each_teacher_workdays[i])

                suitable_time = max(suitable_teachers.loc[suitable_teacher_id, 'lesson_start'])
                h = suitable_time.hour
                m = suitable_time.minute

                for part_of_the_lesson in range(lesson_duration_days):
                    try:
                        selected_lesson_workday = min(workdays_intersection)
                    except:
                        break

                    lesson_date = selected_lesson_workday.replace(hour=h, minute=m)
                    lesson_date_time.append(lesson_date)
                    workdays_intersection.remove(selected_lesson_workday)

                    for st_id in suitable_teacher_id:
                        self.teacher_id_to_workdays[st_id].remove(selected_lesson_workday)
                        lesson_duration = lesson_duration_hours / lesson_duration_days
                        self.teachers_table.at[st_id, 'teachers_load'] += lesson_duration

                        # return
                        ret.append([st_id, lesson_id, lesson_specialization, str(lesson_date), lesson_title,
                                    self.teachers_table.at[st_id, 'trainer_name'], lesson_duration])

            # print('Учителю/лям с id =', *suitable_teacher_id, 'назначено занятие с id =', lesson_id,
            #       'и специализацией', lesson_specialization, 'на', *list(map(str, lesson_date_time)))

        json_ret = {'teachers': []}
        prev_r = None
        i = -1

        sorted_list_ret = sorted(ret, key=itemgetter(0, 3))

        for r in sorted_list_ret:
            # print(r)
            if r[0] != prev_r:
                i += 1
                prev_r = r[0]
                json_ret["teachers"].append(
                    {
                        "teacher_id": r[0],
                        "teacher_name": r[5],
                        # "specializations": "wot, csgo",
                        # "trainer_vacation": null,
                        # "lesson_start": "10:00:00",
                        "load": self.teachers_table.at[r[0], 'teachers_load'],
                        "lessons": [
                            {
                                #"lesson_id": r[1],
                                "lesson_datetime": r[3],
                                "lesson_duration": r[6],
                                "lesson_specialization": r[2],
                                "lesson_title": r[4],
                            }
                        ]
                    }
                )
            elif r[0] == prev_r:
                json_ret["teachers"][i]["lessons"].append(
                    {
                        #"lesson_id": r[1],
                        "lesson_datetime": r[3],
                        "lesson_duration": r[6],
                        "lesson_specialization": r[2],
                        "lesson_title": r[4],
                    }
                )

        # def np_encoder(object):
        #     if isinstance(object, np.generic):
        #         return object.item()

        # ret_string = json.dumps(json_ret, default=np_encoder)

        return json_ret, sorted_list_ret


if __name__ == '__main__':
    SA = SchedulerAlgorithm("./таблица занятий с несколькими учителями.xlsx")
    res, _ = SA.create_schedule2()