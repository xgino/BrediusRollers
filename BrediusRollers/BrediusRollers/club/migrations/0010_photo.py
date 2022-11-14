# Generated by Django 3.2.13 on 2022-11-13 17:06

import club.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0009_about'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=15, verbose_name='Title')),
                ('description', models.TextField(blank=True, max_length=30, null=True, verbose_name='Description')),
                ('photo', models.ImageField(upload_to=club.models.capture_photo, verbose_name='Photo')),
                ('season', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='club.season', verbose_name='Season')),
            ],
        ),
    ]