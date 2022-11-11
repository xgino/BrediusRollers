from import_export import resources
from .models import Player, Position

class PlayerResource(resources.ModelResource):
    class Meta:
        model = Player
        fields = ('id', 'profile', 'team', 'position', 'subscription', 'number_plate', 'is_captain', 'wish')

        widgets = {
            'published': {'format': '%d.%m.%Y'},
        }
        
class PositionResource(resources.ModelResource):
    class Meta:
        model = Position
        fields = ('id', 'name', 'short_name')
        
        widgets = {
            'published': {'format': '%d.%m.%Y'},
        }


