# Generated by Django 3.2.13 on 2022-11-15 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0010_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='title',
            field=models.CharField(max_length=15, verbose_name='Title -> 1x naam perdag, Verander naam hier != als file naam'),
        ),
    ]
