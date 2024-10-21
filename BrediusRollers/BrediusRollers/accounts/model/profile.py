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
    profiel         = models.ImageField(default='profile/default_image.jpg', upload_to=profile_image, verbose_name="Profiel")
    avatar          = models.ImageField(default='profile/default_avatar.jpg', upload_to=profile_avatar, verbose_name="Avatar")
    adress          = models.ForeignKey(Adress, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Adres")

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
    
    def get_full_name(self):
        return self.firstname + " " + self.lastname

    def get_short_name(self):
        if self.firstname and self.lastname != Empty:
            return self.firstname[0] + "." + " " + self.lastname

