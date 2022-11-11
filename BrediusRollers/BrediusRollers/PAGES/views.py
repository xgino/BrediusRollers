from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from django.utils import timezone
from django.db.models import Q  # Django Filter OR

# Import form own models
from games.models import Game_day, Game, Match_team
from club.models import Club, Role, Sponsors
from teams.models import Team
from players.models import Player
from accounts.model import profile


def home(request):
    template = 'home.html'

    
    context = { }

    return render(request, template, context)


def wedstrijden(request):
    template = 'wedstrijden.html'
    now = timezone.now()
    # get bredius games Home_team or Away_team
    get_bredius_games = (Q(home_team__in=Match_team.objects.filter(team__in=Team.objects.filter(club__in=Club.objects.filter(name__startswith='Bredius')))) | Q(away_team__in=Match_team.objects.filter(team__in=Team.objects.filter(club__in=Club.objects.filter(name__startswith='Bredius')))))
    
    #get future and past games
    get_future_games = (Game_day.objects.filter(date__gte=now).order_by('date'))
    get_past_games = (Game_day.objects.filter(date__lt=now).order_by('date'))

    #filter on all teams of bredius
    bredius_teams = Team.objects.filter(club__in=Club.objects.filter(name__startswith='Bredius')).order_by('name')
    
    #Future and past matches of bredius
    future_bredius = Game.objects.filter(get_bredius_games).filter(gameday__in=get_future_games).order_by('start_time')
    past_bredius = Game.objects.filter(get_bredius_games).filter(gameday__in=get_past_games).order_by('end_time')
    
    #Filter on first Upcomming match day date
    upcomming_matchday = Game_day.objects.filter(date__gte=now).earliest('date')

    context = {
        'bredius_teams': bredius_teams,
        'future_bredius': future_bredius,
        'past_bredius': past_bredius,
        'upcomming_matchday': upcomming_matchday,

    }

    return render(request, template, context)


def wedstrijd(request, game_id):
    template = 'wedstrijd.html'

    game = get_object_or_404(Game, pk=game_id)

    context = {
        'game': game,
    }

    return render(request, template, context)


def teams(request):
    template = 'teams.html'
    now = timezone.now()

    #TODO -> FIXED VALUE
    PlayerH1 = Player.objects.filter(team__in=Team.objects.filter(name='H1').filter(club__in=Club.objects.filter(name__startswith='Bredius')))
    PlayerH2 = Player.objects.filter(team__in=Team.objects.filter(name='H2').filter(club__in=Club.objects.filter(name__startswith='Bredius')))
    PlayerH3 = Player.objects.filter(team__in=Team.objects.filter(name='H3').filter(club__in=Club.objects.filter(name__startswith='Bredius')))
    PlayerH4 = Player.objects.filter(team__in=Team.objects.filter(name='H4').filter(club__in=Club.objects.filter(name__startswith='Bredius')))
    PlayerH5 = Player.objects.filter(team__in=Team.objects.filter(name='H5').filter(club__in=Club.objects.filter(name__startswith='Bredius')))

    BrediusTeam3 = Role.objects.order_by('-profile')[:3]
    BrediusTeam6 = Role.objects.order_by('-profile')[3:6]
    BrediusTeam9 = Role.objects.order_by('-profile')[6:9]
    BrediusTeam12 = Role.objects.order_by('-profile')[9:12]
    BrediusTeam15 = Role.objects.order_by('-profile')[12:15]

    sponsor = Sponsors.objects.order_by("?")[:4]


    context = {
        'PlayerH1': PlayerH1,
        'PlayerH2': PlayerH2,
        'PlayerH3': PlayerH3,
        'PlayerH4': PlayerH4,
        'PlayerH5': PlayerH5,

        'BrediusTeam3': BrediusTeam3,
        'BrediusTeam6': BrediusTeam6,
        'BrediusTeam9': BrediusTeam9,
        'BrediusTeam12': BrediusTeam12,
        'BrediusTeam15': BrediusTeam15,

        'sponsor': sponsor,
    }

    return render(request, template, context)



def team(request, team_id):
    # Give Error if Listing ID not exist typed in URL
    team = get_object_or_404(Team, pk=team_id)
    players = Player.objects.order_by('number_plate').filter(team=team)

    context = {
        'team': team,
        'players': players,
    }

    return render(request, 'team.html', context)


def overons(request):
    template = 'overons.html'


    context = { }

    return render(request, template, context)


def contact(request):
    template = 'contact.html'


    context = { }

    return render(request, template, context)

