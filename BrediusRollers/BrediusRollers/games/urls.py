from django.urls import path
from . import views

app_name='Games'

urlpatterns = [
    path('', views.games, name='games'),
    path('<int:game_id>', views.game, name='game'),
]