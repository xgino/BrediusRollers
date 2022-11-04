from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Player


def players(request):
    players = Player.objects.order_by('number_plate')

    # listing per pagina
    paginator = Paginator(players, 3)
    page = request.GET.get('page')
    paged_players = paginator.get_page(page)

    context = {
        'players': paged_players
    }

    return render(request, 'players.html', context)


def player(request, player_id):
    # Give Error if Listing ID not exist typed in URL
    player = get_object_or_404(Player, pk=player_id)

    context = {
        'player': player
    }

    return render(request, 'player.html', context)