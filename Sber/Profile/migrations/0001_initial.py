# Generated by Django 3.1.4 on 2020-12-17 14:36

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MentorData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patronymic', models.CharField(blank=True, max_length=33, verbose_name='Отчество')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('telephone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='Номер телефона')),
                ('city', models.CharField(blank=True, max_length=20, verbose_name='Город')),
                ('sex', models.SmallIntegerField(choices=[(0, 'Мужской'), (1, 'Женский')], default=0, verbose_name='Пол')),
                ('avatar', models.ImageField(default='default.jpg', upload_to='uploads/%Y/%m/%d/', verbose_name='Аватарка')),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Ментор',
                'verbose_name_plural': 'Менторы',
            },
        ),
        migrations.CreateModel(
            name='TeamData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=33, verbose_name='Название команды')),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='Profile.mentordata')),
            ],
            options={
                'verbose_name': 'Команда',
                'verbose_name_plural': 'Команды',
            },
        ),
        migrations.CreateModel(
            name='TrainerData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vacation_start', models.DateField(blank=True, null=True, verbose_name='Дата начала отпуска')),
                ('vacation_duration', models.DurationField(blank=True, null=True, verbose_name='Длительность отпуска')),
                ('work_hours', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Загрузка в часах')),
                ('specialization', models.CharField(blank=True, max_length=150, verbose_name='Специализация')),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='trainer_profile', to=settings.AUTH_USER_MODEL)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trainers', to='Profile.teamdata')),
            ],
            options={
                'verbose_name': 'Тренер',
                'verbose_name_plural': 'Тренера',
            },
        ),
    ]