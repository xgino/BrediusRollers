from django.contrib import admin
from .models import Club, Season, Subscription, Coach, Role, Sponsors

from import_export.admin import ImportExportModelAdmin
from .resources import CoachResource, RoleResource, SeasonResource, ClubResource, SubscriptionResource


class SponsorsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'short_description', 'logo')
    list_display_links = ('title',)
    list_per_page = 25

class ClubAdmin(ImportExportModelAdmin):
    resource_classes = [ClubResource]
    list_display = ('id', 'name', 'city', 'season')
    list_display_links = ('name',)
    list_filter = ('name', 'city', )
    search_fields = ('name', 'city', 'season')
    list_per_page = 25

class SeasonAdmin(ImportExportModelAdmin):
    resource_classes = [SeasonResource]
    list_display = ('id', 'name', 'members', 'start_date', 'end_date', 'first_training', 'last_training')
    list_display_links = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 25

class SubscriptionAdmin(ImportExportModelAdmin):
    resource_classes = [SubscriptionResource]
    list_display = ('id', 'sub_num', 'season')
    list_display_links = ('sub_num',)
    list_filter = ('sub_num', 'season',)
    search_fields = ('sub_num', 'season',)
    list_per_page = 25

class CoachAdmin(ImportExportModelAdmin):
    resource_classes = [CoachResource]
    list_display = ('id', 'profile')
    list_display_links = ('profile',)
    list_per_page = 25

class RoleAdmin(ImportExportModelAdmin):
    resource_classes = [RoleResource]
    list_display = ('id', 'profile', 'title', 'description', 'short_description')
    list_display_links = ('profile',)
    list_per_page = 25




admin.site.register(Club, ClubAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Coach, CoachAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Sponsors, SponsorsAdmin)