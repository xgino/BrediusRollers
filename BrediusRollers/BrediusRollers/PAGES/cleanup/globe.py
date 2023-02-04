from django.db.models import Sum, Q, Count  # Django Filter OR
from django.utils import timezone

# Import from models
from games.models import Game_day, Game, Match_team, Score
from club.models import Club, Role, Sponsors, Season, About, Photo
from teams.models import Team
from players.models import Player
from trainings.models import Training


now = timezone.now()

# Return Latest added season
def season():
    try:
        season = Season.objects.latest("name")
    except:
        season = None

    return season


# Returns all teammembers of Bredius
def brediusTeam(season):
    try: 
        BrediusTeam3 = Role.objects.filter(season=season).order_by('-profile')[:3]
    except:
        BrediusTeam3 = None
    
    try: 
        BrediusTeam6 = Role.objects.filter(season=season).order_by('-profile')[3:6]
    except:
        BrediusTeam6 = None
    
    try: 
        BrediusTeam9 = Role.objects.filter(season=season).order_by('-profile')[6:9]
    except:
        BrediusTeam9 = None
    
    try: 
        BrediusTeam12 = Role.objects.filter(season=season).order_by('-profile')[9:12]
    except:
        BrediusTeam12 = None
    
    try: 
        BrediusTeam15 = Role.objects.filter(season=season).order_by('-profile')[12:15]
    except:
        BrediusTeam15 = None

    return BrediusTeam3, BrediusTeam6, BrediusTeam9, BrediusTeam12, BrediusTeam15


# Return Past bredius games 1, 2, 3
def pastBredius():
    get_past_games = (Game_day.objects.filter(date__lt=now).order_by('date'))
    get_bredius_games = (Q(home_team__in=Match_team.objects.filter(team__in=Team.objects.filter(club__in=Club.objects.filter(name__startswith='Bredius')))) | Q(away_team__in=Match_team.objects.filter(team__in=Team.objects.filter(club__in=Club.objects.filter(name__startswith='Bredius')))))

    try:
        past_bredius1 = Game.objects.filter(get_bredius_games).filter(season=season).filter(gameday__in=get_past_games)[0]
    except:
        past_bredius1 = None

    try:
        past_bredius2 = Game.objects.filter(get_bredius_games).filter(season=season).filter(gameday__in=get_past_games)[1]
    except:
        past_bredius2 = None

    try:
        past_bredius3 = Game.objects.filter(get_bredius_games).filter(season=season).filter(gameday__in=get_past_games)[1:2]
    except:
        past_bredius3 = None

    try:
        past_bredius = Game.objects.filter(get_bredius_games).filter(gameday__in=get_past_games).filter(season=season).order_by('end_time')[:5]
    except:
        past_bredius = None

    return past_bredius1, past_bredius2, past_bredius3, past_bredius


# Return Top 7 goals, playername
def top_goals(season):
    try:
        top_goals = Score.objects.filter(player__in=Player.objects.filter(team__in=Team.objects.filter(club__in=Club.objects.filter(name__startswith='Bredius')))).filter(season=season).order_by('-goals')[:7]
    except:
        top_goals = None
    return top_goals


# Return top 7 assists, playername
def top_assists(season):
    try:
        top_assists = Score.objects.filter(player__in=Player.objects.filter(team__in=Team.objects.filter(club__in=Club.objects.filter(name__startswith='Bredius')))).filter(season=season).order_by('-assists')[:7]
    except:
        top_assists = None
    return top_assists


# Return all players == keepers
def get_keepers(season):
    try:
        keepers = Player.objects.filter( team__in=Team.objects.filter(club__in=Club.objects.filter(name__startswith='Bredius')) ).filter(season=season).filter(position__short_name='GK')
    except:
        keepers = None
    return keepers


# Return all players == defenders
def get_defenders(season):
    try: 
        defenders = Player.objects.filter( team__in=Team.objects.filter(club__in=Club.objects.filter(name__startswith='Bredius')) ).filter(season=season).filter(position__short_name='DF')
    except:
        defenders = None
    return defenders


# Return first upcomming match
def upcomming_matchday(season):
    try:
        upcomming_matchday = Game_day.objects.filter(season=season).filter(date__gte=now).order_by('date').latest('-date')
    except:
        upcomming_matchday = None
    return upcomming_matchday


# Get players in Bredius
def get_bredius_players(season):
    try:
        bredius_players =  Player.objects.filter( team__in=Team.objects.filter(club__in=Club.objects.filter(name__startswith='Bredius')) ).filter(season=season)
    except:
        bredius_players = None
    return bredius_players


# Get list of games upcomming
def get_future_games():
    try:
        get_future_games = (Game_day.objects.filter(date__gte=now).order_by('date'))
    except:
        get_future_games = None
    return get_future_games


# Get list of games played
def get_past_games():
    try:
        get_past_games = (Game_day.objects.filter(date__lt=now).order_by('date'))
    except:
        get_past_games = None
    return get_past_games


# count players in Bredius
def count_players(season):
    player_count_H1 = Player.objects.filter( season=season).filter(team__in=Team.objects.filter(name='H1').filter(club__in=Club.objects.filter(name__startswith='Bredius')) )
    player_count_H2 = Player.objects.filter( season=season).filter(team__in=Team.objects.filter(name='H2').filter(club__in=Club.objects.filter(name__startswith='Bredius')) )
    player_count_H3 = Player.objects.filter( season=season).filter(team__in=Team.objects.filter(name='H3').filter(club__in=Club.objects.filter(name__startswith='Bredius')) )
    player_count_H4 = Player.objects.filter( season=season).filter(team__in=Team.objects.filter(name='H4').filter(club__in=Club.objects.filter(name__startswith='Bredius')) )
    player_count_H5 = Player.objects.filter( season=season).filter(team__in=Team.objects.filter(name='H5').filter(club__in=Club.objects.filter(name__startswith='Bredius')) )
    
    club_player_count = len(player_count_H1) + len(player_count_H2) + len(player_count_H3) + len(player_count_H4) + len(player_count_H5)
    return club_player_count

