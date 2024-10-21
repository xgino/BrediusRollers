from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.exceptions import ObjectDoesNotExist

from django.utils import timezone
from django.db.models import Sum, Q, Count  # Django Filter OR

# Import form own models
from games.models import Game_day, Game, Score
from club.models import Club, Role, Sponsors, Season, Photo
from teams.models import Team, Player
from trainings.models import Training

from .cleanup import globe


def home(request):
    template = 'home.html'
    current_season = globe.get_current_season()
    if current_season:
        club_name = "Bredius"
        return render(request, template, {
            'current_season': current_season,
            'club_games': globe.get_club_games_in_current_season(club_name),
            'header_past2games': globe.get_past_bredius_games(club_name, 2),

            'past_bredius_games': globe.get_past_bredius_games(club_name, 4),
            'future_bredius_games': globe.get_future_bredius_games(club_name),
            'next_bredius_gameday': globe.get_next_game_day(club_name),
            'next_bredius_game': globe.get_next_bredius_game(club_name),
            
            'bredius_keepers': globe.get_player_position_season(club_name, 'goalkeeper'),
            'bredius_defenders': globe.get_player_position_season(club_name, 'verdediger'),
            'player_goals_by_team': globe.get_player_goals_by_team(club_name, 7),

            'sponsor': globe.get_random_sponsors(),
            'roles': globe.get_club_roles(),
            'coaches': globe.get_club_coaches(),
            })
    else:
        return render(request, template, {
            'error_message': "No current season found."
            })


def wedstrijden(request):
    template = 'wedstrijden.html'
    current_season = globe.get_current_season()
    if current_season:
        club_name = "Bredius"
        return render(request, template, {
            'next_bredius_gameday': globe.get_next_game_day(club_name),
            'future_bredius_games': globe.get_future_bredius_games(club_name),
            'past_bredius_games': globe.get_past_bredius_games(club_name, 7),
            })
    else:
        return render(request, template, {
            'error_message': "No current season found."
            })


def wedstrijd(request, game_id):
    template = 'wedstrijd.html'
    current_season = globe.get_current_season()
    if current_season:
        club_name = "Bredius"
        return render(request, template, {
            'game': get_object_or_404(Game, pk=game_id),
            'players': globe.get_players_in_game(club_name, game_id)
            })
    else:
        return render(request, template, {
            'error_message': "No current season found."
            })


def teams(request):
    template = 'teams.html'
    current_season = globe.get_current_season()
    if current_season:
        club_name = "Bredius"
        return render(request, template, {
                'team_players': globe.get_teams_players(club_name),
                'sponsor': globe.get_random_sponsors(),
                'roles': globe.get_club_roles(),
                'coaches': globe.get_club_coaches(),
            })
    else:
        return render(request, template, {
            'error_message': "No current season found."
            })


def player(request, player_id):
    template = 'player.html'
    current_season = globe.get_current_season()
    if current_season:
        return render(request, template, {
                'player': get_object_or_404(Player, pk=player_id),
                'old_player_seasons': Player.objects.filter(profile=player_id).order_by("-team__club__season"),
            })
    else:
        return render(request, template, {
            'error_message': "No current season found."
            })


def overons(request):
    template = 'overons.html'
    current_season = globe.get_current_season()
    if current_season:
        club_name = "Bredius"
        return render(request, template, {
                'club': Club.objects.get(name__icontains=club_name, season=current_season),
                'teamnames': globe.get_team_names_for_club(club_name),
                'training_count': globe.count_trainings(),
                'member_count': globe.count_members_in_club(club_name),
                'sponsor': globe.get_random_sponsors(),
                'roles': globe.get_club_roles(),
                'coaches': globe.get_club_coaches(),
                'next_training': globe.get_next_training(),
                'photos': Photo.objects.filter(season=current_season),      
            })
    else:
        return render(request, template, {
            'error_message': "No current season found."
            })


def contact(request):
    template = 'contact.html'
    current_season = globe.get_current_season()
    if current_season:
        club_name = "Bredius"
        return render(request, template, {
                'club': Club.objects.get(name__icontains=club_name, season=current_season),      
                'next_training': globe.get_next_training(),      
            })
    else:
        return render(request, template, {
            'error_message': "No current season found."
            })
    