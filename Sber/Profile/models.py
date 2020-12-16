from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class MentorData(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE)
    patronymic = models.CharField('Отчество', blank=True, max_length=33)
    birthday = models.DateField('Дата рождения', blank=True, null=True)
    telephone = PhoneNumberField('Номер телефона', blank=True)
    city = models.CharField('Город', blank=True, max_length=20)
    sex = models.SmallIntegerField('Пол', choices=[(0, 'Мужской'), (1, 'Женский')], default=0)
    avatar = models.ImageField('Аватарка', upload_to='uploads/%Y/%m/%d/', default='default.jpg')

    class Meta:
        verbose_name = 'Ментор'
        verbose_name_plural = 'Менторы'

    @property
    def date_check(self):
        return self.birthday or ""


class TeamData(models.Model):
    mentor = models.ForeignKey(MentorData, related_name='teams', on_delete=models.CASCADE)
    team_name = models.CharField("Название команды", max_length=33)

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'


class TrainerData(models.Model):
    team = models.ForeignKey(TeamData, related_name='trainers', on_delete=models.CASCADE)
    vacation_start = models.DateField('Дата начала отпуска', blank=True, null=True)
    vacation_duration = models.DurationField('Длительность отпуска', blank=True, null=True)
    work_hours = models.PositiveIntegerField('Загрузка в часах', validators=[MinValueValidator(1)], null=True,
                                             blank=True)
    specialization = models.CharField('Специализация', max_length=150, null=True, blank=True)

    class Meta:
        verbose_name = 'Тренер'
        verbose_name_plural = 'Тренера'
