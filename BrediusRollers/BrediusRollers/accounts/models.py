from queue import Empty
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Email is verplicht")
        if not password:
            raise ValueError("Wachtwoord is verplicht")
        if not first_name:
            raise ValueError("first_name is verplicht")

        user_obj = self.model(
            email = self.normalize_email(email),
            first_name = first_name
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, first_name, password=None):
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            is_staff=True
        )
        return user
    
    def create_superuser(self, email, first_name, password=None):
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            is_staff=True,
            is_admin=True
        )
        return user


class User(AbstractBaseUser):
    email       = models.EmailField(unique=True, max_length=128, verbose_name="Email")

    first_name  = models.CharField(max_length=255, verbose_name="Voornaam")
    last_name   = models.CharField(max_length=255, verbose_name="Achternaam")

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Account aangemaakt")
    last_login  = models.DateTimeField(auto_now=True, verbose_name="Laatst online")

    active      = models.BooleanField(default=True)
    staff       = models.BooleanField(default=False)
    admin       = models.BooleanField(default=False)

    USERNAME_FIELD  = "email"
    REQUIRED_FIELDS = ['first_name']

    objects = UserManager()

    def __str__(self):
        return self.first_name + " " + self.last_name

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        if self.first_name and self.last_name != Empty:
            return self.first_name[0] + "." + " " + self.last_name

    def formated_date_joined(self):
        date = self.date_joined
        return date.strftime("%d %b %y om %H:%M")

    def formated_last_login(self):
        date = self.last_login
        return date.strftime("%d %b %y om %H:%M")



    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


