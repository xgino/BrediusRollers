from django.db import models

from accounts.model.profile import Profile
from teams.models import Team
from club.models import Subscription, Season


class Position(models.Model):
    name  = models.CharField(max_length=255, verbose_name="Name")
    short_name   = models.CharField(max_length=255, verbose_name="Korte Naam")

    def __str__(self):
        return self.name


class Player(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Profile")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Team")
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Possition")
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Subscription")
    number_plate  = models.IntegerField(verbose_name="Number plate")
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Season")
   
    is_captain  = models.BooleanField(blank=True, verbose_name="captain")
    wish  = models.TextField(max_length=255, null=True, blank=True, verbose_name="Wish")

    def __str__(self):
        return self.profile.user.first_name + ' ' + self.profile.user.last_name + ' ' + str(self.season.name)


