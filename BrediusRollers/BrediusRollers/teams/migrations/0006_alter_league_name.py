# Generated by Django 3.2.13 on 2022-11-10 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0005_alter_league_shortname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='league',
            name='name',
            field=models.CharField(max_length=56, verbose_name='League'),
        ),
    ]