from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Team, League, Player
from .resources import TeamResource, LeagueResource, PlayerResource

class TeamAdmin(ImportExportModelAdmin):
    resource_classes = [TeamResource]
    list_display = ('id', 'club', 'name', 'league', 'points_earned', 'matches_played')
    list_display_links = ('club', 'name',)
    list_filter = [
        ('club__season', admin.RelatedFieldListFilter),
        ('league'),
        ('name'),
    ]
    search_fields = ('name',)
    list_per_page = 25

admin.site.register(Team, TeamAdmin)


class LeagueAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('name',)
    list_per_page = 25

admin.site.register(League, LeagueAdmin)


class PlayerAdmin(ImportExportModelAdmin):
    resource_classes = [PlayerResource]
    list_display = ('id', 'profile', 'team', 'positions', 'subscription', 'number_plate')
    list_display_links = ('profile',)
    list_filter = [
        ('team__club__season', admin.RelatedFieldListFilter),
        ('team__club__name'),
        ('team__name'),
    ]
    search_fields = ('profile__user__first_name',)
    list_per_page = 25

admin.site.register(Player, PlayerAdmin)