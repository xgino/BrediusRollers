from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Team, League, Player
from .resources import TeamResource, LeagueResource, PlayerResource
from django.utils import timezone
from club.models import Season
from accounts.model.profile import Profile

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
    list_display = ('id', 'profile', 'team', 'positions', 'number_plate', 'season_goals')
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

    # Get the current season based on today's date
    def get_current_season(self):
        today = timezone.now().date()
        try:
            # Find the season where today's date is between start_date and end_date
            return Season.objects.get(start_date__lte=today, end_date__gte=today)
        except Season.DoesNotExist:
            return None

    # Override the queryset to filter by the current season initially
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Check if the user has selected any season in the filter
        if 'team__club__season__id__exact' not in request.GET:
            current_season = self.get_current_season()
            if current_season:
                return queryset.filter(team__club__season=current_season)
        return queryset

    # Preselect the current season when adding a new player and filter profiles/teams by season
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        current_season = self.get_current_season()

        if current_season:
            # Filter profiles by those that are associated with the current season
            form.base_fields['profile'].queryset = Profile.objects.filter(
                player__team__club__season=current_season
            )

            # Filter teams by those that are part of clubs in the current season
            form.base_fields['team'].queryset = Team.objects.filter(
                club__season=current_season
            )

        return form

admin.site.register(Player, PlayerAdmin)