from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Team, League
from .resources import TeamResource, LeagueResource

class TeamAdmin(ImportExportModelAdmin):
    resource_classes = [TeamResource]
    list_display = ('id', 'name', 'points_earned', 'matches_played', 'coach', 'season', 'club', 'league')
    list_display_links = ('name',)
    list_filter = ('name', 'season')
    search_fields = ('name', 'season', 'league')
    list_per_page = 25

class LeagueAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'shortname')
    list_display_links = ('name',)
    list_per_page = 25


admin.site.register(Team, TeamAdmin)
admin.site.register(League, LeagueAdmin)
