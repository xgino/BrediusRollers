from django.contrib import admin
from .models import Training, Trainings_location, Trainings_time

admin.site.register(Training)
admin.site.register(Trainings_location)
admin.site.register(Trainings_time)
