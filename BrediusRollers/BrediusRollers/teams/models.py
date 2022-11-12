from django.db import models
from django.urls import reverse
from club.models import Club, Season, Coach

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