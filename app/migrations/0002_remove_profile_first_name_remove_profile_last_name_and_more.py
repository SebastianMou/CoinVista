# Generated by Django 4.2.3 on 2023-07-30 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='last_name',
        ),
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.CharField(default='Hi my name is ... ', max_length=355),
        ),
    ]
