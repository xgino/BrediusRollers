from django.db import models
from accounts.model.profile import Profile

class Coach(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Coach")

    def __str__(self):
        return str(self.profile)


class Season(models.Model):
    name  = models.CharField(max_length=255, verbose_name="Season")
    members  = models.IntegerField(verbose_name="Members")
    start_date  = models.DateField(max_length=255, verbose_name="Start Date")
    end_date  = models.DateField(max_length=255, verbose_name="End Date")

    first_training  = models.DateField(max_length=255, verbose_name="Start training")
    last_training  = models.DateField(max_length=255, verbose_name="Last training")

    def __str__(self):
        return self.name


class Club(models.Model):
    name  = models.CharField(max_length=255, verbose_name="Club")
    city   = models.CharField(max_length=255, verbose_name="Stad")
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Season")

    def __str__(self):
        return self.name



class Subscription(models.Model):
    sub_num  = models.CharField(max_length=255, verbose_name="Lid Nummer")
    fee   = models.FloatField(verbose_name="Cost")
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Season")

    def __str__(self):
        return self.sub_num