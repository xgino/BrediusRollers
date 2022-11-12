from django.db import models
from accounts.model.profile import Profile
import os

def sponsor_logo(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s%s.%s" % ('sponsor', instance.user.id, 'png')
    return os.path.join('sponsor/sponsors', filename)


class Sponsors(models.Model):
    title  = models.CharField(max_length=255, verbose_name="Title")
    description = models.TextField(max_length=200, blank=True, null=True, verbose_name="Description")
    short_description = models.TextField(max_length=20, blank=True, null=True, verbose_name="Short description")
    logo = models.ImageField(default='sponsor/default.jpg', upload_to=sponsor_logo, verbose_name="Logo")

    def __str__(self):
        return str(self.title)


class Coach(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Coach")

    def __str__(self):
        return str(self.profile)


class Season(models.Model):
    name  = models.IntegerField(verbose_name="Season")
    members  = models.IntegerField(verbose_name="Members")
    start_date  = models.DateField(max_length=255, verbose_name="Start Date")
    end_date  = models.DateField(max_length=255, verbose_name="End Date")

    first_training  = models.DateField(max_length=255, verbose_name="Start training")
    last_training  = models.DateField(max_length=255, verbose_name="Last training")

    def __str__(self):
        return f"{self.name}"


class Role(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Role")
    title  = models.CharField(max_length=255, verbose_name="Title")
    short_description = models.TextField(max_length=50, blank=True, null=True, verbose_name="Short description")
    description = models.TextField(max_length=200, blank=True, null=True, verbose_name="Description")
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Season")

    def __str__(self):
        return str(self.profile)


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