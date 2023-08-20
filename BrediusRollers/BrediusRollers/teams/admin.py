from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Team, League, Player
from .resources import TeamResource, LeagueResource, PlayerResource

class PlayerInline(admin.TabularInline):  # You can also use StackedInline
    model = Player
    ordering = ['profile__firstname']  # Specify the fields to order by
    #list_filter = ['field', 'start_time', 'league']
    extra = 0  # Set the number of empty forms to 0


class TeamAdmin(ImportExportModelAdmin):
    inlines = [PlayerInline]
    resource_classes = [TeamResource]

    def players_count(self, obj):
        return obj.player_set.count()
    players_count.short_description = "Number of Players"

    list_display = ('id', 'club', 'name', 'league', 'points_earned', 'matches_played', 'players_count')
    list_display_links = ('club', 'name',)
    list_filter = [
        ('club__season', admin.RelatedFieldListFilter),
        ('club__name'),
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
    list_display = ('id', 'profile', 'team', 'positions', 'subscription', 'number_plate', 'season_goals', 'season_assists')
    list_display_links = ('profile',)
    list_filter = [
        ('team__club__season', admin.RelatedFieldListFilter),
        ('team__club__name'),
        ('team__name'),
        ('profile'),
    ]
    search_fields = ('profile__user__first_name',)
    list_per_page = 25

    def season_goals(self, obj):
        return obj.calculate_total_goals_current_season()
    season_goals.short_description = 'Total Goals'
    def season_assists(self, obj):
        return obj.calculate_total_assist_current_season()
    season_assists.short_description = 'Total Assists'

admin.site.register(Player, PlayerAdmin)