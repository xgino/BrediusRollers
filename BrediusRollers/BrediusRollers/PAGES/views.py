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

# TODO IS to fix Globe and template


def home(request):
    template = 'home.html'
    current_season = globe.get_current_season()
    if current_season:
        club_name = "Bredius"
        club_games = globe.get_club_games_in_current_season(club_name)
        past_bredius_games = globe.get_past_bredius_games(club_name, 4)
        future_bredius_games = globe.get_future_bredius_games(club_name)
        next_bredius_gameday = globe.get_next_game_day(club_name)
        next_bredius_game = globe.get_next_bredius_game(club_name)
        return render(request, template, {
            'current_season': current_season,
            'club_games': club_games,
            'header_past2games': globe.get_past_bredius_games(club_name, 2),

            'past_bredius_games': past_bredius_games,
            'future_bredius_games': future_bredius_games,
            'next_bredius_gameday': next_bredius_gameday,
            'next_bredius_game': next_bredius_game,
            
            'bredius_keepers': globe.get_player_position_season(club_name, 'goalkeeper'),
            'bredius_defenders': globe.get_player_position_season(club_name, 'defender'),
            'player_goals': globe.get_goals_by_position_in_season(club_name),
            })
    else:
        return render(request, template, {
            'error_message': "No current season found."
            })



    # Get SLIDER Past -3 Bredius Games
    #past_bredius1, past_bredius2, past_bredius3, past_bredius = globe.pastBredius()

    #top_goals = globe.top_goals(season)
    #top_assists = globe.top_assists(season)

    #keepers = globe.get_keepers(season)
    #defenders = globe.get_defenders(season)

    #upcomming_matchday = globe.upcomming_matchday(season)
    #bredius_players = globe.get_bredius_players(season)

    #BrediusTeam3, BrediusTeam6, BrediusTeam9, BrediusTeam12, BrediusTeam15 = globe.brediusTeam(season)

    #sponsor = Sponsors.objects.order_by("?")[:4]

    context = {
        'current_season': current_season,
        'psge': psge,
        # 'past_bredius': past_bredius, 'past_bredius1': past_bredius1, 'past_bredius2': past_bredius2, 'past_bredius3': past_bredius3,
        # 'bredius_players': bredius_players,
        # 'upcomming_matchday': upcomming_matchday,
        # 'top_goals': top_goals, 'top_assists': top_assists,
        # 'keepers': keepers[1:], 'defenders': defenders,
        # 'fkeepers':keepers.first(),
        # 'BrediusTeam3': BrediusTeam3, 'BrediusTeam6': BrediusTeam6, 'BrediusTeam9': BrediusTeam9, 'BrediusTeam12': BrediusTeam12, 'BrediusTeam15': BrediusTeam15,
        # 'sponsor': sponsor,
    }

    return render(request, template, context)


def wedstrijden(request):
    template = 'wedstrijden.html'
    season = globe.season()

    get_bredius_games = (Q(home_team__in=Match_team.objects.filter(team__in=Team.objects.filter(club__in=Club.objects.filter(name__startswith='Bredius')))) | Q(away_team__in=Match_team.objects.filter(team__in=Team.objects.filter(club__in=Club.objects.filter(name__startswith='Bredius')))))
    get_future_games = globe.get_future_games()
    get_past_games = globe.get_past_games()

    #Future and past matches of bredius
    future_bredius = Game.objects.filter(get_bredius_games).filter(gameday__in=get_future_games).filter(season=season).order_by('start_time')
    past_bredius = Game.objects.filter(get_bredius_games).filter(gameday__in=get_past_games).filter(season=season).order_by('end_time')

    upcomming_matchday = globe.upcomming_matchday(season)
    
    context = {
        'future_bredius': future_bredius, 'past_bredius': past_bredius,
        'upcomming_matchday': upcomming_matchday,
    }

    return render(request, template, context)


def wedstrijd(request, game_id):
    template = 'wedstrijd.html'

    game = get_object_or_404(Game, pk=game_id)
    players = Player.objects.filter( season=game.home_team.team.season).filter(team__in=Team.objects.filter(name=game.home_team.team.name).filter(club=game.home_team.team.club) )
    
    context = {
        'game': game,
        'players': players,

    }

    return render(request, template, context)


def teams(request):
    template = 'teams.html'
    season = globe.season()

    PlayerH1 = Player.objects.filter( season=season ).filter(team__in=Team.objects.filter(name='H1').filter(club__in=Club.objects.filter(name__startswith='Bredius')) ).order_by('profile__user__first_name')
    PlayerH2 = Player.objects.filter( season=season ).filter(team__in=Team.objects.filter(name='H2').filter(club__in=Club.objects.filter(name__startswith='Bredius')) ).order_by('profile__user__first_name')
    PlayerH3 = Player.objects.filter( season=season ).filter(team__in=Team.objects.filter(name='H3').filter(club__in=Club.objects.filter(name__startswith='Bredius')) ).order_by('profile__user__first_name')
    PlayerH4 = Player.objects.filter( season=season).filter(team__in=Team.objects.filter(name='H4').filter(club__in=Club.objects.filter(name__startswith='Bredius')) ).order_by('profile__user__first_name')
    PlayerH5 = Player.objects.filter( season=season).filter(team__in=Team.objects.filter(name='H5').filter(club__in=Club.objects.filter(name__startswith='Bredius')) ).order_by('profile__user__first_name')

    BrediusTeam3, BrediusTeam6, BrediusTeam9, BrediusTeam12, BrediusTeam15 = globe.brediusTeam(season)

    sponsor = Sponsors.objects.order_by("?")[:4]

    context = {
        'PlayerH1': PlayerH1, 'PlayerH2': PlayerH2, 'PlayerH3': PlayerH3, 'PlayerH4': PlayerH4, 'PlayerH5': PlayerH5,
        'BrediusTeam3': BrediusTeam3, 'BrediusTeam6': BrediusTeam6, 'BrediusTeam9': BrediusTeam9, 'BrediusTeam12': BrediusTeam12, 'BrediusTeam15': BrediusTeam15,

        'sponsor': sponsor,
    }

    return render(request, template, context)


def player(request, player_id):
    template = 'player.html'

    player = get_object_or_404(Player, pk=player_id)
    old_player = Player.objects.filter(profile=player.profile.user.id).order_by("-season")

    context = {
        'player': player,
        'old_player': old_player,
    }

    return render(request, template, context)


def overons(request):
    template = 'overons.html'
    now = timezone.now()

    season = globe.season()

    club = Club.objects.filter(name__startswith='Bredius').filter(season=season).first()
    bredius_teams = Team.objects.filter(club__in=Club.objects.filter(name__startswith='Bredius').filter(season=season)).order_by('name')
    bredius_teams_count = Team.objects.filter(season=season).filter(club__in=Club.objects.filter(name__startswith='Bredius')).order_by('name')
    photo = Photo.objects.filter(season=season).order_by('?')

    club_player_count = globe.count_players(season)

    BrediusTeam3, BrediusTeam6, BrediusTeam9, BrediusTeam12, BrediusTeam15 = globe.brediusTeam(season)

    sponsor = Sponsors.objects.order_by("?")[:4]
    training = Training.objects.filter(date__lt=now).order_by('date')
    next_training = Training.objects.filter(date__gte=now).order_by('date').first()

    context = {
        'BrediusTeam3': BrediusTeam3, 'BrediusTeam6': BrediusTeam6, 'BrediusTeam9': BrediusTeam9, 'BrediusTeam12': BrediusTeam12, 'BrediusTeam15': BrediusTeam15,

        'sponsor': sponsor,
        'photo': photo,
        'club': club,
        'next_training': next_training,

        'club_player_count': club_player_count,
        'bredius_teams': bredius_teams_count,
        'train_count': len(training),
    }

    return render(request, template, context)


def contact(request):
    template = 'contact.html'
    now = timezone.now()

    next_training = Training.objects.filter(date__gte=now).order_by('date').first()
    context = { 
        'next_training': next_training,
    }

    return render(request, template, context)

