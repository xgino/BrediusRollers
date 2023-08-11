from email.headerregistry import Address
from django.db import models
from club.models import Season
from teams.models import League, Team
from players.models import Player
from accounts.model.adress import Adress

class Match_team(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name="Team")
    season = models.ForeignKey(Season, on_delete=models.CASCADE, verbose_name="Season")

    def __str__(self):
        return f"{self.team}"
    
    class Meta:
        unique_together = ["team", "season"]
    


class Game_day(models.Model):
    sport_hall   = models.CharField(max_length=255, verbose_name="Sporthal")
    date = models.DateField(auto_now=False, auto_now_add=False, verbose_name="Datum")
    adress = models.ForeignKey(Adress, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Adres")
    season = models.ForeignKey(Season, on_delete=models.CASCADE, verbose_name="Season")

    def __str__(self):
        return self.sport_hall

    def formated_date(self):
        date = self.date
        return date.strftime("%Y-%m-%d")
    


class Game(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE, verbose_name="League")
    field  = models.IntegerField(verbose_name="Veld")

    start_time = models.TimeField(auto_now=False, auto_now_add=False, verbose_name="Start tijd")
    end_time = models.TimeField(auto_now=False, auto_now_add=False, verbose_name="Eindig tijd")
    
    leauge_code   = models.CharField(max_length=10, verbose_name="Wedstrijd Code", null=True, blank=True)
    home_team = models.ForeignKey(Match_team, on_delete=models.CASCADE, verbose_name="Home", related_name='Home_Team')
    home_score = models.IntegerField(verbose_name="Home Goals")
    away_team = models.ForeignKey(Match_team, on_delete=models.CASCADE, verbose_name="Away", related_name='Away_Team')
    away_score = models.IntegerField(verbose_name="Away Goals")

    gameday = models.ForeignKey(Game_day, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Game_day")
    season = models.ForeignKey(Season, on_delete=models.CASCADE, verbose_name="Season")

    class Meta:
        unique_together = ["leauge_code", "season"]

    def __str__(self):
        return f'{self.home_team} VS {self.away_team}'

    def formated_starttime(self):
        date = self.start_time
        return date.strftime("%H:%M")

    def long_formated_starttime(self):
        date = self.start_time
        return date.strftime("%H:%M:%S")

    def formated_endtime(self):
        date = self.end_time
        return date.strftime("%H:%M")

    def get_long_datetime(self):
        date = self.gameday.formated_date()
        time = self.long_formated_starttime()
        return f'{date} {time}'


class Score(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, verbose_name="Season")
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Player")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name="Game")
    goals  = models.IntegerField(verbose_name="Goals")
    assists = models.IntegerField(verbose_name="assists")

    def __str__(self):
        return str(self.goals)

