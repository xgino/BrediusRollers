from django.contrib import admin
from django.db.models import Q, Sum
from club.models import Club
from .models import Game, Score, Game_day

from import_export.admin import ImportExportModelAdmin
from django.urls import reverse
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
        ('season', admin.RelatedFieldListFilter),
        ('sport_hall'),
    ]
    list_per_page = 25
    


class ScoresAdmin(ImportExportModelAdmin):
    resource_classes = [ScoresResource]
    list_display = ('player', 'gameday_sport_hall', 'matching', 'goals', 'assists', 'season')
    list_display_links = ('player',)
    list_filter = [
        ('season', admin.RelatedFieldListFilter),
        ('player'),
    ]
    #search_fields = ('player', 'season', 'game')
    list_per_page = 25



#admin.site.register(Game, GameAdmin)
admin.site.register(Game_day, Game_dayAdmin)
admin.site.register(Score, ScoresAdmin)


