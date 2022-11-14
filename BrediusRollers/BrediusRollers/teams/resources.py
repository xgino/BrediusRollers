from import_export import resources
from .models import Team, League

class TeamResource(resources.ModelResource):
    class Meta:
        model = Team
        fields = ('id', 'name', 'points_earned', 'matches_played', 'coach', 'season', 'club', 'league')

        widgets = {
            'published': {'format': '%d.%m.%Y'},
        }
        
class LeagueResource(resources.ModelResource):
    class Meta:
        model = League
        fields = ('id', 'name', 'shortname')
        
        widgets = {
            'published': {'format': '%d.%m.%Y'},
        }

