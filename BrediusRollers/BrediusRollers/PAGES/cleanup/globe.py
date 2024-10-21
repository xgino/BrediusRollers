from django.db.models import Sum, Q, F, Count  # Django Filter OR
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import date, datetime
import random

# Import from models
from games.models import Game_day, Game, Score
from club.models import Club, Role, Sponsors, Season, Coach
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

# Get player goal count of the season, separated by team, limited by num
def get_player_goals_by_team(club_name, num):
    current_season = get_current_season()  # Ensure you have a method to get the current season
    if current_season:
        try:
            # Get teams for the specified club
            teams = Team.objects.filter(club__season=current_season, club__name__icontains=club_name)

            player_goals_by_team = {}
            for team in teams:
                players = Player.objects.filter(
                    team=team
                ).annotate(
                    total_goals=Sum('score__goals', filter=Q(score__season=current_season))
                ).order_by(F('total_goals').desc())[:num]  # Limit to num players

                player_goals_by_team[team] = players  # Store players by team

            return player_goals_by_team
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    return None
    

# Get players of a game
def get_players_in_game(club_name, game_id):
    current_season = get_current_season()  # Replace with your logic to get the current season
    if current_season:
        
        game = Game.objects.get(pk=game_id)
        home_team = game.home_team
        away_team = game.away_team
        clubs_with_name = Club.objects.filter(name__icontains=club_name, season=current_season)
        matching_club = clubs_with_name.first()

        if home_team.club.name == matching_club.name:
            players = Player.objects.filter(
                team=home_team
            )
        elif away_team.club.name == matching_club.name:
            players = Player.objects.filter(
                team=away_team
            )
        else:
            players = Player.objects.none()

        return players
     
    return None

# Return All Team of Bredius and All Players below it
def get_teams_players(club_name):
    current_season = get_current_season()  # Replace with your logic to get the current season
    players_by_team = {}

    if current_season:
        try:
            teams = Team.objects.filter(
                club__name__icontains=club_name,
                club__season=current_season
            )

            for team in teams:
                players = Player.objects.filter(
                    team=team,
                    team__club__season=current_season
                ).order_by('profile__firstname', 'profile__lastname')
                
                players_by_team[team] = players

            return players_by_team
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    return None

# Get 4 sponsors Random display
def get_random_sponsors(count=4):
    sponsors = Sponsors.objects.all()
    random_sponsors = random.sample(list(sponsors), min(count, len(sponsors)))
    return random_sponsors

# Get Club Roles
def get_club_roles():
    current_season = get_current_season()
    if current_season:
        roles = Role.objects.filter(
            season=current_season
        ).order_by('profile__firstname', 'profile__lastname')
        
        roles_list = list(roles)  # Convert QuerySet to a list
        
        if roles_list:
            return roles_list
        
    return []

# Get Club Coaches
def get_club_coaches():
    current_season = get_current_season()
    if current_season:
        coaches = Coach.objects.filter(
            season=current_season
        ).order_by('profile__firstname', 'profile__lastname')
        
        coaches_list = list(coaches)  # Convert QuerySet to a list
        
        if coaches_list:
            return coaches_list
        
    return []

# Get all teams
def get_team_names_for_club(club_name):
    current_season = get_current_season()  # Replace this with the actual way you get the current season
    if current_season:
        team_names_queryset = Team.objects.filter(
            club__name__icontains=club_name,  # Use icontains for case-insensitive search
            club__season=current_season
        )
        team_names = [team.name for team in team_names_queryset]
        formatted_team_names = ", ".join(team_names)
        return formatted_team_names
        
    return ""

# Get counter of members
def count_members_in_club(club_name):
    current_season = get_current_season()  # Replace this with the actual way you get the current season
    
    if current_season:
        member_count = Player.objects.filter(
            team__club__name__icontains=club_name,
            team__club__season=current_season
        ).count()
        return member_count
        
    return 0

# Get counter of trainings
def count_trainings():
    current_season = get_current_season()  # Replace this with the actual way you get the current season
    
    if current_season:
        start_date = current_season.start_date
        end_date = date.today()
        
        num_trainings = Training.objects.filter(
            season=current_season,
            date__range=(start_date, end_date)
        ).count()
        
        return num_trainings
        
    return 0

# Find upcomming next trainig
def get_next_training():
    current_season = get_current_season()  # Replace this with the actual way you get the current season
    if current_season:
        today = date.today()
        now = datetime.now()
        
        next_training = Training.objects.filter(
            season=current_season,
            date__gte=today
        ).exclude(
            date=today,
            training_time__end_time__lt=now.time()
        ).order_by('date', 'training_time__start_time').first()
        
        return next_training
    return None
