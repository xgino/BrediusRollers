from django.contrib import admin
from django.utils import timezone
from club.models import Season
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

    # Get the current season based on today's date
    def get_current_season(self):
        today = timezone.now().date()
        try:
            return Season.objects.get(start_date__lte=today, end_date__gte=today)
        except Season.DoesNotExist:
            return None

    # Override the queryset to filter by the current season initially
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if 'season__id__exact' not in request.GET:
            current_season = self.get_current_season()
            if current_season:
                return queryset.filter(season=current_season)
        return queryset

    # Preselect the current season when adding a new training session
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        current_season = self.get_current_season()

        if current_season:
            # Preselect the current season for the season field
            form.base_fields['season'].initial = current_season

        return form


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
