from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Club
from teams.models import Team
from players.models import Player


def clubs(request):
    club = Club.objects.order_by('name')
    paginator = Paginator(club, 3)
    page = request.GET.get('page')
    paged_clubs = paginator.get_page(page)


    context = {
        'clubs': paged_clubs
    }

    return render(request, 'clubs.html', context)



def club(request, club_id):
    # Give Error if Listing ID not exist typed in URL
    club = get_object_or_404(Club, pk=club_id)
    teams = Team.objects.order_by('name').filter(club=club)

    context = {
        'club': club,
        'teams': teams,
    }

    return render(request, 'club.html', context)