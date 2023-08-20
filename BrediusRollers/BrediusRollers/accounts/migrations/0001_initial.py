# Generated by Django 3.2.13 on 2023-08-20 15:04

import accounts.model.profile
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=128, unique=True, verbose_name='Email')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Account aangemaakt')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='Laatst online')),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Adress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=128, verbose_name='Straat')),
                ('house_number', models.CharField(max_length=128, verbose_name='Huisnummer')),
                ('zipcode', models.CharField(max_length=5, verbose_name='Postcodenummers')),
                ('zipcode_number', models.CharField(max_length=128, verbose_name='Postcode letters')),
                ('place', models.CharField(max_length=64, verbose_name='Woonplaats')),
            ],
            options={
                'verbose_name_plural': 'Adressen',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to='accounts.user', verbose_name='User')),
                ('firstname', models.CharField(max_length=255, verbose_name='Voornaam')),
                ('lastname', models.CharField(blank=True, max_length=255, null=True, verbose_name='Achternaam')),
                ('gender', models.CharField(blank=True, choices=[('Dhr', 'De heer'), ('Mevr', 'Mevrouw')], max_length=4, null=True, verbose_name='Geslacht')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Mobiel nummer')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Geboortedatum')),
                ('profiel', models.ImageField(default='profile/default_image.jpg', upload_to=accounts.model.profile.profile_image, verbose_name='Profiel')),
                ('avatar', models.ImageField(default='profile/default_avatar.jpg', upload_to=accounts.model.profile.profile_avatar, verbose_name='Avatar')),
                ('bio', models.TextField(blank=True, max_length=200, null=True, verbose_name='Bio')),
                ('hobby', models.CharField(blank=True, default='Rolstoel Hockey', max_length=200, null=True, verbose_name='Hobby(s)')),
                ('adress', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.adress', verbose_name='Adres')),
            ],
        ),
    ]
