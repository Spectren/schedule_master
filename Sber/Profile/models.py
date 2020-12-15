from django.db import models
from django.conf import settings

class MentorData(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE)

    patronymic = models.CharField('Отчество', null=True, blank=True, max_length=33)
    birthday = models.DateField('Дата рождения', null=True, blank=True)
    telephone = models.CharField('Номер телефона', null=True, blank=True, max_length=11)
    city = models.CharField('Город', null=True, blank=True, max_length=20)
    sex = models.SmallIntegerField('Пол', choices = [(0, 'Мужской'), (1, 'Женский')], default=0)
    avatar = models.ImageField('Аватарка', upload_to ='uploads/%Y/%m/%d/', default='default.jpg')

    class Meta:
        verbose_name = 'Ментор'
        verbose_name_plural = 'Менторы'