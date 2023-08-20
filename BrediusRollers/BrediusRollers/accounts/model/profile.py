from django.db import models
from queue import Empty
from django.contrib.auth import get_user_model
from .adress import Adress
import os

User = get_user_model()


def profile_image(instance, filename):
    
    ext = filename.split('.')[-1]
    filename = "%s%s.%s" % ('Profile', instance.user.id, 'jpg')
    return os.path.join('profile/user_image', filename)


def profile_avatar(instance, filename):
    
    ext = filename.split('.')[-1]
    filename = "%s%s.%s" % ('Profile', instance.user.id, 'jpg')
    return os.path.join('profile/user_avatar', filename)



class Profile(models.Model):

    GENDER_CHOICES = (
        ('Dhr', 'De heer'),
        ('Mevr', 'Mevrouw'),
    )

    user            = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, primary_key=True, null=False, related_name="profile", verbose_name="User")
    
    firstname       = models.CharField(max_length=255, blank=False, verbose_name="Voornaam")
    lastname        = models.CharField(max_length=255, null=True, blank=True, verbose_name="Achternaam")

    gender          = models.CharField(max_length=4, null=True, blank=True, choices=GENDER_CHOICES, verbose_name="Geslacht")
    phone           = models.CharField(max_length=20, null=True, blank=True, verbose_name="Mobiel nummer")
    date_of_birth   = models.DateField(null=True, blank=True, verbose_name="Geboortedatum")

    profiel         = models.ImageField(default='profile/default_image.jpg', upload_to=profile_image, verbose_name="Profiel")
    avatar          = models.ImageField(default='profile/default_avatar.jpg', upload_to=profile_avatar, verbose_name="Avatar")
    bio             = models.TextField(max_length=200, blank=True, null=True, verbose_name="Bio")
    hobby           = models.CharField(default='Rolstoel Hockey', null=True, blank=True, max_length=200, verbose_name='Hobby(s)')

    adress          = models.ForeignKey(Adress, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Adres")

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
    
    def get_full_name(self):
        return self.firstname + " " + self.lastname

    def get_short_name(self):
        if self.firstname and self.lastname != Empty:
            return self.firstname[0] + "." + " " + self.lastname

    def formatted_date_dob(self):
        if self.date_of_birth:
            date = self.date_of_birth
            return date.strftime("%d %B %Y")

    def formatted_short_dob(self):
        if self.date_of_birth:
            date = self.date_of_birth
            return date.strftime("%d %b %y")
