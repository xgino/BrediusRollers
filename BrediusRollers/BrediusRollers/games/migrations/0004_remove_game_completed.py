# Generated by Django 3.2.13 on 2022-11-07 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_game_completed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='completed',
        ),
    ]
