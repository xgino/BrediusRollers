# Generated by Django 3.2.13 on 2023-08-12 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teams', '0001_initial'),
        ('club', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.IntegerField(verbose_name='Veld')),
                ('start_time', models.TimeField(verbose_name='Start tijd')),
                ('end_time', models.TimeField(verbose_name='Eindig tijd')),
                ('leauge_code', models.CharField(blank=True, max_length=10, null=True, verbose_name='Wedstrijd Code')),
                ('home_score', models.IntegerField(verbose_name='Home Goals')),
                ('away_score', models.IntegerField(verbose_name='Away Goals')),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goals', models.IntegerField(verbose_name='Goals')),
                ('assists', models.IntegerField(verbose_name='assists')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.game', verbose_name='Game')),
                ('player', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='teams.player', verbose_name='Player')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='club.season', verbose_name='Season')),
            ],
        ),
        migrations.CreateModel(
            name='Match_team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='club.season', verbose_name='Season')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.team', verbose_name='Team')),
            ],
            options={
                'unique_together': {('team', 'season')},
            },
        ),
        migrations.CreateModel(
            name='Game_day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sport_hall', models.CharField(max_length=255, verbose_name='Sporthal')),
                ('date', models.DateField(verbose_name='Datum')),
                ('adress', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.adress', verbose_name='Adres')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='club.season', verbose_name='Season')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='away_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Away_Team', to='games.match_team', verbose_name='Away'),
        ),
        migrations.AddField(
            model_name='game',
            name='gameday',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='games.game_day', verbose_name='Game_day'),
        ),
        migrations.AddField(
            model_name='game',
            name='home_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Home_Team', to='games.match_team', verbose_name='Home'),
        ),
        migrations.AddField(
            model_name='game',
            name='league',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.league', verbose_name='League'),
        ),
        migrations.AddField(
            model_name='game',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='club.season', verbose_name='Season'),
        ),
        migrations.AlterUniqueTogether(
            name='game',
            unique_together={('leauge_code', 'season')},
        ),
    ]
