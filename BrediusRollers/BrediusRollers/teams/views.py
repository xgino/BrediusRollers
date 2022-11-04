from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Team
from players.models import Player

def teams(request):

    teams = Team.objects.order_by('club')
    paginator = Paginator(teams, 3)
    page = request.GET.get('page')
    paged_teams = paginator.get_page(page)

    context = {
        'teams': paged_teams
    }

    return render(request, 'teams.html', context)


def team(request, team_id):
    # Give Error if Listing ID not exist typed in URL
    team = get_object_or_404(Team, pk=team_id)
    players = Player.objects.order_by('number_plate').filter(team=team)

    context = {
        'team': team,
        'players': players,
    }

    return render(request, 'team.html', context)