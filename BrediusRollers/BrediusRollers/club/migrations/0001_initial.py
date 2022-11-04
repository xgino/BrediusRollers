# Generated by Django 3.2.13 on 2022-08-13 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Season')),
                ('members', models.IntegerField(verbose_name='Members')),
                ('start_date', models.DateField(max_length=255, verbose_name='Start Date')),
                ('end_date', models.DateField(max_length=255, verbose_name='End Date')),
                ('first_training', models.DateField(max_length=255, verbose_name='Start training')),
                ('last_training', models.DateField(max_length=255, verbose_name='Last training')),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_num', models.CharField(max_length=255, verbose_name='Lid Nummer')),
                ('fee', models.FloatField(verbose_name='Cost')),
                ('season', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='club.season', verbose_name='Season')),
            ],
        ),
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Club')),
                ('city', models.CharField(max_length=255, verbose_name='Stad')),
                ('season', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='club.season', verbose_name='Season')),
            ],
        ),
    ]
