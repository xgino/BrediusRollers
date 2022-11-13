from django.db import models
from accounts.model.adress import Adress


class Trainings_time(models.Model):
    start_time  = models.TimeField(verbose_name="Start Time")
    end_time  = models.TimeField(verbose_name="End Time")

    def __str__(self):
        return f'{self.start_time} {self.end_time}'


class Trainings_location(models.Model):
    adress = models.ForeignKey(Adress, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Adres")

    def __str__(self):
        return self.adress.get_street()


class Training(models.Model):
    training_time = models.ForeignKey(Trainings_time, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Training_time")
    training_location = models.ForeignKey(Trainings_location, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Training_location")
    date = models.DateField(verbose_name="Date")
    

    def __str__(self):
        return f'{self.training_time} {self.training_location}'


