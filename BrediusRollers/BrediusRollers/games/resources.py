from import_export import resources
from .models import Match_team, Game_day, Game, Score


class MatchTeamResource(resources.ModelResource):
    class Meta:
        model = Match_team
        fields = ('id', 'team')

        widgets = {
            'published': {'format': '%d.%m.%Y'},
        }
        

class GamedayResource(resources.ModelResource):
    class Meta:
        model = Game_day
        fields = ('id', 'sport_hall', 'date', 'adress')

        widgets = {
            'published': {'format': '%d.%m.%Y'},
        }
        

class GameResource(resources.ModelResource):
    class Meta:
        model = Game
        fields = ('id', 'league', 'field', 'start_time', 'end_time', 'leauge_code', 'home_team', 'home_score', 'away_team', 'away_score', 'gameday')

        widgets = {
            'published': {'format': '%d.%m.%Y'},
        }

class ScoresResource(resources.ModelResource):
    class Meta:
        model = Score
        fields = ('id', 'season', 'player', 'game', 'goals', 'assists')
        
        widgets = {
            'published': {'format': '%d.%m.%Y'},
        }
        

