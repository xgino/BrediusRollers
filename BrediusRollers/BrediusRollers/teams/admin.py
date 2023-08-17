from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Team, League, Player, Score
from .resources import TeamResource, LeagueResource, PlayerResource

class PlayerInline(admin.TabularInline):  # You can also use StackedInline
    model = Player
    ordering = ['profile__firstname']  # Specify the fields to order by
    #list_filter = ['field', 'start_time', 'league']
    extra = 0  # Set the number of empty forms to 0


class TeamAdmin(ImportExportModelAdmin):
    inlines = [PlayerInline]
    resource_classes = [TeamResource]
    list_display = ('id', 'club', 'name', 'league', 'points_earned', 'matches_played')
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


class ScoreInline(admin.TabularInline):
    model = Score
    verbose_name_plural = 'Scores'
    fields = ('profile',)  # Add other fields as needed
    #autocomplete_fields = ('profile',)  # Add autocomplete for profile selection
    extra = 0  # Set the number of empty forms to 0

    def profile_name(self, obj):
        return f"{obj.profile.firstname} {obj.profile.lastname}"  # Display first name and last name
    profile_name.short_description = 'Profile Name'
    
    def profile_email(self, obj):
        return obj.profile.user.email  # Display email
    profile_email.short_description = 'Profile Email'
    profile_email.admin_order_field = 'profile__user__email'  # Enable sorting by email



class PlayerAdmin(ImportExportModelAdmin):
    inlines = [ScoreInline]
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