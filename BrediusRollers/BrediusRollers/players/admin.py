from django.contrib import admin
from .models import Player, Position

from import_export.admin import ImportExportModelAdmin
from .resources import PlayerResource, PositionResource


class PlayerAdmin(ImportExportModelAdmin):
    resource_classes = [PlayerResource]
    list_display = ('id', 'profile', 'team', 'position', 'subscription', 'number_plate')
    list_display_links = ('profile',)
    list_filter = ('profile',)
    search_fields = ('profile',)
    list_per_page = 25

class PositionAdmin(ImportExportModelAdmin):
    resource_classes = [PositionResource]
    list_display = ('id', 'name', 'short_name')
    list_display_links = ('name',)
    list_per_page = 25


admin.site.register(Player, PlayerAdmin)
admin.site.register(Position, PositionAdmin)


