from django.db.models import Sum, Q, Count  # Django Filter OR
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from datetime import date, datetime

# Import from models
from games.models import Game_day, Game, Score
from club.models import Club, Role, Sponsors, Season, Photo
from teams.models import Team, Player
from trainings.models import Training


now = timezone.now()

# Return Current season
def get_current_season():
    current_date = date.today()
    try:
        current_season = Season.objects.get(start_date__lte=current_date, end_date__gte=current_date)
        return current_season
    except ObjectDoesNotExist:
        print("No Current Season Found")
        return None


# Return Past bredius games Current season
def get_club_games_in_current_season(club_name):

    current_season = get_current_season()
    if current_season:
        try:
            home_team_games = Game.objects.filter(
                gameday__season=current_season,
                home_team__club__name__icontains=club_name,
            )
            
            away_team_games = Game.objects.filter(
                gameday__season=current_season,
                away_team__club__name__icontains=club_name,
            )
            
            club_games = home_team_games | away_team_games  # Combine home and away games
            return club_games
        except Game.DoesNotExist:
            return None
    return None

# Return Games of bredius All seasons
def get_club_games(club_name):
    try:
        home_team_games = Game.objects.filter(
            home_team__club__name__icontains=club_name
        )
        
        away_team_games = Game.objects.filter(
            away_team__club__name__icontains=club_name
        )
        
        club_games = home_team_games | away_team_games  # Combine home and away games
        return club_games
    except Game.DoesNotExist:
        return None

# Return past num games
def get_past_bredius_games(club_name, num):
    try:
        bredius_games = get_club_games(club_name)
        if bredius_games is not None:
            # Get the most recent past 7 "Bredius" games
            past_7_bredius_games = bredius_games.filter(
                gameday__date__lt = date.today()
            ).order_by('-gameday__date', '-start_time')[:num]

            return past_7_bredius_games
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

# Return future 7 games
def get_future_bredius_games(club_name):
    try:
        bredius_games = get_club_games(club_name)
        if bredius_games is not None:
            # Get the next 7 "Bredius" games
            next_7_bredius_games = bredius_games.filter(
                gameday__date__gte=date.today()
            ).order_by('gameday__date', 'start_time')[:7]

            return next_7_bredius_games
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Get the Future upcomming Game Day
def get_next_game_day(club_name):
    try:
        today = timezone.now().date()
        next_game_day = Game_day.objects.filter(date__gte=today).order_by('date').first()
        return next_game_day
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

# Get the next upcomming bredius Game
def get_next_bredius_game(club_name):
    try:
        bredius_games = get_club_games(club_name)
        if bredius_games is not None:
            # Get the next "Bredius" game from today onwards
            today = date.today()
            next_bredius_game = bredius_games.filter(
                gameday__date__gte=today
            ).order_by('gameday__date', 'start_time').first()

            return next_bredius_game
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
# Get the position of the players
def get_player_position_season(club_name, position):
    current_season = get_current_season()

    if current_season:
        try:
            keeper_players = Player.objects.filter(
                team__club__name__icontains=club_name,
                team__club__season=current_season,
                positions__icontains=position
            ).order_by('profile__firstname', 'profile__lastname')

            return keeper_players
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    return None


def get_goals_by_position_in_season(club_name):
    current_season = get_current_season()

    if current_season:
        try:
            player_goal_counts = {}
            scores = Score.objects.filter(
                player__team__club__name__icontains=club_name,
                player__team__club__season=current_season
            )
            
            for score in scores:
                player_id = score.player.id
                goals = score.goals
                
                if player_id in player_goal_counts:
                    player_goal_counts[player_id] += goals
                else:
                    player_goal_counts[player_id] = goals
            
            return player_goal_counts
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    return None




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
        club = Club.objects.get(name__startswith='Bredius')
        teams = Team.objects.filter(club=club)
        keepers = Player.objects.filter(team__in=teams, positions__contains=['goalkeeper'], season=season).order_by('-team')
    except Club.DoesNotExist:
        keepers = None
    return keepers


# Return all players == defenders
def get_defenders(season):
    try: 
        team = Team.objects.filter(club__in=Club.objects.filter(name__startswith='Bredius'))
        defenders = Player.objects.filter( team__in=team ).filter(positions='defender').filter(season=season).order_by('-team')
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

