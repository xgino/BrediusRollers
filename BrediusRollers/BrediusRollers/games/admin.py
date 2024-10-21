from django.contrib import admin
from django.db.models import Q, Sum
from club.models import Club
from .models import Game, Score, Game_day

from import_export.admin import ImportExportModelAdmin
from django.urls import reverse
from django.utils import timezone
from club.models import Season
from django.http import HttpResponseRedirect
from .resources import GamedayResource, GameResource, ScoresResource


class ClubFilter(admin.SimpleListFilter):
    title = 'Club'
    parameter_name = 'club'

    def lookups(self, request, model_admin):
        # Return a list of club names
        clubs = Club.objects.values_list('name', flat=True).distinct()
        return [(club, club) for club in clubs]

    def queryset(self, request, queryset):
        # Filter the queryset based on selected club
        club_name = self.value()
        if club_name:
            return queryset.filter(
                Q(home_team__club__name__icontains=club_name) |
                Q(away_team__club__name__icontains=club_name)
            )
        return queryset


class GameAdmin(ImportExportModelAdmin):
    resource_classes = [GameResource]
    list_display = ('gameday_sport_hall', 'league', 'home_team_name', 'home_score', 'away_score', 'away_team_name', 'end_time', 'gameday_date', 'gameday_season')
    list_display_links = ('home_team_name', 'away_team_name')
    search_fields = ('gameday__sport_hall',)
    list_filter = [
        ('gameday__season', admin.RelatedFieldListFilter),
        ('league'),
        ClubFilter,  # Add the custom filter here
        ('gameday__sport_hall'),
    ]
    list_per_page = 25
    

class GameInline(admin.TabularInline):  # You can also use StackedInline
    model = Game
    ordering = ['start_time']  # Specify the fields to order by
    list_filter = ['field', 'start_time', 'league']
    extra = 0  # Set the number of empty forms to 0

class Game_dayAdmin(ImportExportModelAdmin):
    inlines = [GameInline]
    resource_classes = [GamedayResource]
    list_display = ('id', 'sport_hall', 'date', 'adress', 'season')
    list_display_links = ('sport_hall', 'date',)
    search_fields = ('sport_hall',)
    list_filter = [
        ('season'),
        ('sport_hall'),
    ]
    list_per_page = 25
    
    # Get the current season based on today's date
    def get_current_season(self):
        today = timezone.now().date()
        try:
            # Find the season where today's date is between start_date and end_date
            return Season.objects.get(start_date__lte=today, end_date__gte=today)
        except Season.DoesNotExist:
            return None

    # Override the queryset to filter by the current season's date range initially
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Check if the user has selected any season in the filter
        if 'season__id__exact' not in request.GET:
            # If not, default to the current season (if available)
            current_season = self.get_current_season()
            if current_season:
                return queryset.filter(season=current_season)
        return queryset

    # Preselect the current season when adding a new game day
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        current_season = self.get_current_season()

        # If this is a new object (i.e., we're adding a new Game_day), preselect the current season
        if not obj and current_season:
            form.base_fields['season'].initial = current_season
        return form


class ScoresAdmin(ImportExportModelAdmin):
    resource_classes = [ScoresResource]
    list_display = ('player', 'gameday_sport_hall', 'matching', 'goals', 'season')
    list_display_links = ('player',)
    list_filter = [
        ('player__team__club__season', admin.RelatedFieldListFilter),
    ]
    #search_fields = ('player', 'season', 'game')
    list_per_page = 25

    # Get the current season based on today's date
    def get_current_season(self):
        today = timezone.now().date()
        try:
            # Find the season where today's date is between start_date and end_date
            return Season.objects.get(start_date__lte=today, end_date__gte=today)
        except Season.DoesNotExist:
            return None

    # Override the queryset to filter by the current season's date range initially
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Check if the user has selected any season in the filter
        if 'season__id__exact' not in request.GET:
            # If not, default to the current season (if available)
            current_season = self.get_current_season()
            if current_season:
                return queryset.filter(season=current_season)
        return queryset

    # Preselect the current season when adding a new score
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        current_season = self.get_current_season()

        # If this is a new object (i.e., we're adding a new Score), preselect the current season
        if not obj and current_season:
            form.base_fields['season'].initial = current_season
        return form



#admin.site.register(Game, GameAdmin)
admin.site.register(Game_day, Game_dayAdmin)
admin.site.register(Score, ScoresAdmin)


