from django.db import models
from django.contrib import admin
from .models import Club, Season, Coach, Role, Sponsors, Photo
from teams.models import Team
from django.utils import timezone

from import_export.admin import ImportExportModelAdmin
from .resources import CoachResource, RoleResource, SeasonResource, ClubResource

class CoachAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'season')
    list_display_links = ('profile',)
    list_filter = [
        ('season', admin.RelatedFieldListFilter),
        ('profile__firstname'),
    ]
    list_per_page = 25

class CoachInline(admin.TabularInline):
    model = Coach
    verbose_name_plural = 'Coaches'
    fields = ('profile',)  # Add other fields as needed
    extra = 0  # Set the number of empty forms to 0

    def profile_name(self, obj):
        return f"{obj.profile.firstname} {obj.profile.lastname}"  # Display first name and last name
    profile_name.short_description = 'Profile Name'
    
    def profile_email(self, obj):
        return obj.profile.user.email  # Display email
    profile_email.short_description = 'Profile Email'
    profile_email.admin_order_field = 'profile__user__email'  # Enable sorting by email

class RoleInline(admin.TabularInline):
    model = Role
    verbose_name_plural = 'Role'
    fields = ('profile', 'title', 'short_description', 'description')  # Add other fields as needed
    extra = 0  # Set the number of empty forms to 0

class SeasonAdmin(admin.ModelAdmin):
    inlines = [CoachInline, RoleInline]
    list_display = ('id', 'start_date', 'end_date',)
    list_display_links = ('start_date', 'end_date')
    list_per_page = 25

class SponsorsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_display_links = ('title',)
    list_per_page = 25

class TeamInline(admin.TabularInline):  # You can also use StackedInline
    model = Team
    extra = 0  # Set the number of empty forms to 0
    ordering = ['name']  # Order teams by name
    show_change_link = True  # Allows clicking on inline items to edit them directly


class ClubAdmin(admin.ModelAdmin):
    inlines = [TeamInline]  # Teams inline within Club
    list_display = ['id', 'name', 'season', 'members', 'city']
    list_display_links = ['name']
    list_filter = ['season', 'name']  # Filter by season and name
    search_fields = ['name', 'city']  # Enable search by club name and city
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

    # Preselect the current season when adding a new club
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        current_season = self.get_current_season()

        # If this is a new object (i.e., we're adding a new Club), preselect the current season
        if not obj and current_season:
            form.base_fields['season'].initial = current_season
        return form


class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'title')
    list_display_links = ('profile',)
    list_filter = [
        ('season', admin.RelatedFieldListFilter),
        ('title'),
    ]
    list_per_page = 25

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'photo')
    list_display_links = ('title',)
    list_filter = ('season',)
    list_filter = [
        ('season', admin.RelatedFieldListFilter),
    ]
    list_per_page = 25

# Register the admin classes
admin.site.register(Season, SeasonAdmin)
admin.site.register(Club, ClubAdmin)
admin.site.register(Sponsors, SponsorsAdmin)
# admin.site.register(Coach, CoachAdmin)
# admin.site.register(Role, RoleAdmin)
admin.site.register(Photo, PhotoAdmin)