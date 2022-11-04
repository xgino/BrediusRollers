from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Game, Game_day



def games(request):

    gameday = Game_day.objects.order_by('date')
    games = Game.objects.all().filter(gameday__in=gameday).order_by('start_time')       

    

    context = {
        'games': games,
    }

    return render(request, 'games.html', context)


def game(request, game_id):
    # Give Error if Listing ID not exist typed in URL
    game = get_object_or_404(Game, pk=game_id)

    context = {
        'game': game
    }

    return render(request, 'game.html', context)

