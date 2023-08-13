from email.headerregistry import Address
from django.db import models
from club.models import Season
from teams.models import League, Team, Player
from accounts.model.adress import Adress
   


class Game_day(models.Model):
    sport_hall   = models.CharField(max_length=255, verbose_name="Sporthal")
    date = models.DateField(auto_now=False, auto_now_add=False, verbose_name="Datum")
    adress = models.ForeignKey(Adress, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Adres")
    season = models.ForeignKey(Season, on_delete=models.CASCADE, verbose_name="Season")

    def __str__(self):
        return f"{self.sport_hall} {self.season.start_date.year}-{self.season.end_date.year}"

    def formated_date(self):
        date = self.date
        return date.strftime("%Y-%m-%d")
    


class Game(models.Model):
    gameday = models.ForeignKey(Game_day, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Game_day")
    league = models.ForeignKey(League, on_delete=models.CASCADE, verbose_name="League")
    leauge_code   = models.CharField(max_length=10, verbose_name="Wedstrijd Code", null=True, blank=True)

    field  = models.IntegerField(verbose_name="Veld")
    start_time = models.TimeField(auto_now=False, auto_now_add=False, verbose_name="Start tijd")
    end_time = models.TimeField(auto_now=False, auto_now_add=False, verbose_name="Eindig tijd")
    
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name="Home", related_name='Home_Team')
    home_score = models.IntegerField(verbose_name="Home Goals")
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name="Away", related_name='Away_Team')
    away_score = models.IntegerField(verbose_name="Away Goals")

    def __str__(self):
        return f'{self.home_team} VS {self.away_team}'

    def gameday_sport_hall(self):
        return self.gameday.sport_hall
    
    def gameday_date(self):
        return self.gameday.date.strftime("%d-%m-%Y")

    def gameday_season(self):
        return self.gameday.season
    
    def home_team_name(self):
        return self.home_team.get_name()
    
    def away_team_name(self):
        return self.away_team.get_name()

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

    def gameday_sport_hall(self):
        return self.game.gameday.sport_hall

    def matching(self):
        return f"{self.game.home_team.club.name} {self.game.home_team.name} VS {self.game.away_team.club.name} {self.game.away_team.name}"