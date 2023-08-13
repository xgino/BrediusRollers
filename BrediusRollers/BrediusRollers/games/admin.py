from django.contrib import admin
from .models import Game, Score, Game_day

from import_export.admin import ImportExportModelAdmin
from .resources import GamedayResource, GameResource, ScoresResource


class GameAdmin(ImportExportModelAdmin):
    resource_classes = [GameResource]
    list_display = ('gameday_sport_hall', 'league', 'home_team_name', 'home_score', 'away_score', 'away_team_name', 'gameday_date', 'gameday_season')
    list_display_links = ('home_team_name', 'away_team_name')
    search_fields = ('gameday__sport_hall',)
    list_filter = [
        ('gameday__season', admin.RelatedFieldListFilter),
        ('league'),
        ('home_team__club__name'),
        ('gameday__sport_hall'),
    ]
    list_per_page = 25

class Game_dayAdmin(ImportExportModelAdmin):
    resource_classes = [GamedayResource]
    list_display = ('id', 'sport_hall', 'date', 'adress', 'season')
    list_display_links = ('sport_hall',)
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



admin.site.register(Game, GameAdmin)
admin.site.register(Game_day, Game_dayAdmin)
admin.site.register(Score, ScoresAdmin)


