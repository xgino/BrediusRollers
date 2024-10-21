from import_export import resources
from .models import Coach, Role, Season, Club
        

class CoachResource(resources.ModelResource):
    class Meta:
        model = Coach
        fields = ('id', 'profile')

        widgets = {
            'published': {'format': '%d.%m.%Y'},
        }
        

class RoleResource(resources.ModelResource):
    class Meta:
        model = Role
        fields = ('id', 'profile', 'title', 'description', 'short_description')

        widgets = {
            'published': {'format': '%d.%m.%Y'},
        }
        

class SeasonResource(resources.ModelResource):
    class Meta:
        model = Season
        fields = ('id', 'name', 'members', 'start_date', 'end_date', 'first_training', 'last_training')

        widgets = {
            'published': {'format': '%d.%m.%Y'},
        }
        

class ClubResource(resources.ModelResource):
    class Meta:
        model = Club
        fields = ('id', 'name', 'city', 'season')

        widgets = {
            'published': {'format': '%d.%m.%Y'},
        }


