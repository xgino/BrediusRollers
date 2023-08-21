from django.contrib import admin
from django.db import models
from django.urls import reverse
from multiselectfield import MultiSelectField
from accounts.model.profile import Profile
from club.models import Subscription, Season, Club, Coach
from datetime import date

class League(models.Model):
    LEAGUE_CHOICES = [
        ('Hoofdklasse', 'Hoofdklasse'),
        ('Overgangsklasse', 'Overgangsklasse'),
        ('Eerste Klasse', 'Eerste Klasse'),
        ('Tweede Klasse', 'Tweede Klasse'),
        ('Derde Klasse', 'Derde Klasse'),
        ('Vierde Klasse', 'Vierde Klasse'),
    ]
    name = models.CharField(choices=LEAGUE_CHOICES, max_length=50, verbose_name="League")
    def __str__(self):
        return self.name

class Team(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Club", limit_choices_to={'season__start_date__lte': date.today(), 'season__end_date__gte': date.today()})
    league = models.ForeignKey('teams.League', on_delete=models.CASCADE, verbose_name="League")
    name  = models.CharField(max_length=255, verbose_name="Team")
    
    points_earned  = models.IntegerField(verbose_name="Earned Points")
    matches_played  = models.IntegerField(verbose_name="Played Matches")
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Coach", limit_choices_to={'season__start_date__lte': date.today(), 'season__end_date__gte': date.today()})

    def __str__(self):
        return f"{self.club} {self.name}"

    def get_name(self):
        return f"{self.club.name} {self.name}"

    def get_absolute_url(self):
        return reverse('Pages:team_filter', args=[self.id])

class Player(models.Model):
    POSITION_CHOICES = [
        ('middenvelder', 'Middenvelder'),
        ('aanvaller', 'Aanvaller'),
        ('verdediger', 'Verdediger'),
        ('goalkeeper', 'Goalkeeper'),
    ]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Profile")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Team", limit_choices_to={'club__season__start_date__lte': date.today(), 'club__season__end_date__gte': date.today()})
    positions = MultiSelectField(choices=POSITION_CHOICES, verbose_name="Positions")
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Subscription", limit_choices_to={'season__start_date__lte': date.today(), 'season__end_date__gte': date.today()})
    number_plate  = models.IntegerField(verbose_name="Number plate")

    is_captain  = models.BooleanField(blank=True, verbose_name="captain")
    wish  = models.TextField(max_length=255, null=True, blank=True, verbose_name="Wish")

    def __str__(self):
        return self.profile.firstname + ' ' + self.profile.lastname

    def calculate_total_goals_current_season(self):
        current_date = date.today()
        current_season = Season.objects.get(start_date__lte=current_date, end_date__gte=current_date)
        return self.score_set.filter(season=current_season).aggregate(total_goals=models.Sum('goals'))['total_goals']

    def calculate_total_assist_current_season(self):
        current_date = date.today()
        current_season = Season.objects.get(start_date__lte=current_date, end_date__gte=current_date)
        return self.score_set.filter(season=current_season).aggregate(total_assists=models.Sum('assists'))['total_assists']
