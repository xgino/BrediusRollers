from django.contrib import admin
from django.db import models
from django.urls import reverse
from multiselectfield import MultiSelectField
from accounts.model.profile import Profile
from club.models import Subscription, Season, Club, Coach
from games.models import Player, Game, Game_day


class League(models.Model):
    LEAGUE_CHOICES = [
        ('HK', 'Hoofdklasse'),
        ('OK', 'Overgangsklasse'),
        ('1e', 'Eerste Klasse'),
        ('2e', 'Tweede Klasse'),
        ('3e', 'Derde Klasse'),
        ('4e', 'Vierde Klasse'),
    ]
    name = models.CharField(choices=LEAGUE_CHOICES, max_length=50, verbose_name="League")
    def __str__(self):
        return self.name


## TODO FIX MOVING SCORE FROM GAME MODEL TO TEAM MODEL ONLINE UNDER PLAYER

class Team(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Club")
    league = models.ForeignKey(League, on_delete=models.CASCADE, null=True, blank=True, verbose_name="League")
    name  = models.CharField(max_length=255, verbose_name="Team")
    
    points_earned  = models.IntegerField(verbose_name="Earned Points")
    matches_played  = models.IntegerField(verbose_name="Played Matches")
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Coach")

    def __str__(self):
        return f"{self.club} {self.name}"

    def get_name(self):
        return f"{self.club.name} {self.name}"

    def get_absolute_url(self):
        return reverse('Pages:team_filter', args=[self.id])



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


class Player(models.Model):
    POSITION_CHOICES = [
        ('forward', 'Forward'),
        ('midfielder', 'Midfielder'),
        ('defender', 'Defender'),
        ('goalkeeper', 'Goalkeeper'),
    ]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Profile")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Team")
    positions = MultiSelectField(choices=POSITION_CHOICES, verbose_name="Positions")
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Subscription")
    number_plate  = models.IntegerField(verbose_name="Number plate")

    is_captain  = models.BooleanField(blank=True, verbose_name="captain")
    wish  = models.TextField(max_length=255, null=True, blank=True, verbose_name="Wish")

    def __str__(self):
        return self.profile.firstname + ' ' + self.profile.lastname
