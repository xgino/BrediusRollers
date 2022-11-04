# Generated by Django 3.2.13 on 2022-08-13 16:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teams', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('club', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('short_name', models.CharField(max_length=255, verbose_name='Korte Naam')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_plate', models.IntegerField(verbose_name='Number plate')),
                ('is_captain', models.BooleanField(blank=True, verbose_name='captain')),
                ('wish', models.TextField(blank=True, max_length=255, null=True, verbose_name='Wish')),
                ('position', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='players.position', verbose_name='Possition')),
                ('subscription', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='club.subscription', verbose_name='Subscription')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='teams.team', verbose_name='Team')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
