from django.db import models
from django.contrib.auth.models import AbstractUser

class Mentors(AbstractUser):
    patronymic = models.CharField('Отчество', max_length=33)
    email      = models.EmailField('Почта', unique=True)
    avatar     = models.ImageField('Аватарка', null=True)

    class Meta:
        verbose_name = 'Ментор'
        verbose_name_plural = 'Менторы'