from django.contrib import admin

from .models import Training, Trainings_location, Trainings_time
from import_export.admin import ImportExportModelAdmin
from .resources import TrainingResource, TrainingsLocationResource, TrainingsTimeResource


class TrainingAdmin(ImportExportModelAdmin):
    resource_classes = [TrainingResource]
    list_display = ('training_location', 'training_time', 'date', 'season')
    list_display_links = ('training_location',)
    list_filter = [
        ('season', admin.RelatedFieldListFilter),
    ]
    list_per_page = 25


class Trainings_locationAdmin(ImportExportModelAdmin):
    resource_classes = [TrainingsLocationResource]
    list_display = ('id', 'adress')
    list_display_links = ('adress',)
    list_per_page = 25


class Trainings_timeAdmin(ImportExportModelAdmin):
    resource_classes = [TrainingsTimeResource]
    list_display = ('id', 'start_time', 'end_time')
    list_display_links = ('id',)
    list_per_page = 25


admin.site.register(Training, TrainingAdmin)
admin.site.register(Trainings_location, Trainings_locationAdmin)
admin.site.register(Trainings_time, Trainings_timeAdmin)
