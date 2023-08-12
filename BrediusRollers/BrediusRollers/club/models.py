from django.db import models
from accounts.model.profile import Profile
import os
from datetime import datetime

def sponsor_logo(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s%s.%s" % ('sponsor', instance.user.id, 'png')
    return os.path.join('sponsor/sponsors', filename)

def about_image(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s%s.%s" % ('about', instance.season.name, 'png')
    return os.path.join('about/image', filename)

def capture_photo(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s%s.%s" % (instance.title, f"-{datetime.now().strftime('%d')}{datetime.now().strftime('%m')}-{datetime.now().strftime('%y')}", 'png')
    return os.path.join('about/photo', filename)


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
    start_date  = models.DateField(max_length=255, verbose_name="Start Date")
    end_date  = models.DateField(max_length=255, verbose_name="End Date")
    members  = models.IntegerField(verbose_name="Members")

    def __str__(self):
        return f"{self.start_date.year}-{self.end_date.year}"


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


class About(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Season")
    description = models.TextField(max_length=200, blank=True, null=True, verbose_name="Description")
    photo = models.ImageField(default='about/default_image.jpg', upload_to=about_image, verbose_name="Image")

    def __str__(self):
        return f"{self.season}"

class Photo(models.Model):
    title  = models.CharField(max_length=15, verbose_name="Title -> 1x naam perdag, Verander naam hier != als file naam")
    description = models.TextField(max_length=30, blank=True, null=True, verbose_name="Description")
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Season")
    photo = models.ImageField(upload_to=capture_photo, verbose_name="Photo")

    def __str__(self):
        return f"{self.title} {self.season.name}"