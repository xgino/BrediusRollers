from django.db import models
from django.urls import reverse
from multiselectfield import MultiSelectField
from accounts.model.profile import Profile
from club.models import Subscription, Season, Club, Coach


class League(models.Model):
    name  = models.CharField(max_length=56, verbose_name="League")
    shortname  = models.CharField(max_length=10, verbose_name="Short League")

    def __str__(self):
        return self.name


class Team(models.Model):
    name  = models.CharField(max_length=255, verbose_name="Team")
    points_earned  = models.IntegerField(verbose_name="Earned Points")
    matches_played  = models.IntegerField(verbose_name="Played Matches")
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Coach")

    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Season")
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Club")
    league = models.ForeignKey(League, on_delete=models.CASCADE, null=True, blank=True, verbose_name="League")

    def __str__(self):
        return f"{self.club} {self.name} {self.season}"

    def get_absolute_url(self):
        return reverse('Pages:team_filter', args=[self.id])


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
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Season")
   
    is_captain  = models.BooleanField(blank=True, verbose_name="captain")
    wish  = models.TextField(max_length=255, null=True, blank=True, verbose_name="Wish")

    def __str__(self):
        return self.profile.user.first_name + ' ' + self.profile.user.last_name + ' ' + str(self.season.name)
