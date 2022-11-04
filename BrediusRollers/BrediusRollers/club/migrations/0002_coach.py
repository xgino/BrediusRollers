# Generated by Django 3.2.13 on 2022-08-13 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20220813_1836'),
        ('club', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.profile', verbose_name='Coach')),
            ],
        ),
    ]
