# Generated by Django 3.2.13 on 2022-11-15 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0011_alter_photo_title'),
        ('games', '0004_remove_game_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='season',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='club.season', verbose_name='Season'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game_day',
            name='season',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='club.season', verbose_name='Season'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='match_team',
            name='season',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='club.season', verbose_name='Season'),
            preserve_default=False,
        ),
    ]