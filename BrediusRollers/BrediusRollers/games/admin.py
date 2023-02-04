from django.contrib import admin
from .models import Match_team, Game, Score, Game_day

from import_export.admin import ImportExportModelAdmin
from .resources import MatchTeamResource, GamedayResource, GameResource, ScoresResource


class Match_teamAdmin(ImportExportModelAdmin):
    resource_classes = [MatchTeamResource]
    list_display = ('id', 'team', 'season')
    list_display_links = ('team',)
    list_filter = ('team',)
    search_fields = ('team',)
    list_per_page = 25

class GameAdmin(ImportExportModelAdmin):
    resource_classes = [GameResource]
    list_display = ('id', 'league', 'field', 'start_time', 'end_time', 'leauge_code', 'home_team', 'home_score', 'away_team', 'away_score', 'gameday', 'season')
    list_display_links = ('home_team', 'away_team')
    list_filter = ('league', 'gameday')
    search_fields = ('league', 'leauge_code')
    list_per_page = 25

class Game_dayAdmin(ImportExportModelAdmin):
    resource_classes = [GamedayResource]
    list_display = ('id', 'sport_hall', 'date', 'adress', 'season')
    list_display_links = ('sport_hall',)
    list_filter = ('sport_hall',)
    search_fields = ('sport_hall', 'date', 'adress')
    list_per_page = 25

class ScoresAdmin(ImportExportModelAdmin):
    resource_classes = [ScoresResource]
    list_display = ('id', 'player', 'season', 'game', 'goals', 'assists')
    list_display_links = ('player',)
    list_filter = ('season',)
    search_fields = ('player', 'season', 'game')
    list_per_page = 25



admin.site.register(Match_team, Match_teamAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Game_day, Game_dayAdmin)
admin.site.register(Score, ScoresAdmin)


