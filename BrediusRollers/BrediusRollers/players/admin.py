from django.contrib import admin
from .models import Player

from import_export.admin import ImportExportModelAdmin
from .resources import PlayerResource


class PlayerAdmin(ImportExportModelAdmin):
    resource_classes = [PlayerResource]
    list_display = ('id', 'profile', 'team', 'position', 'subscription', 'number_plate', 'season')
    list_display_links = ('profile',)
    list_filter = ('team', 'position', 'season',)
    #search_fields = ('profile',)
    list_per_page = 25




admin.site.register(Player, PlayerAdmin)


