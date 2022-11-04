from django.urls import path
from . import views

app_name='Players'

urlpatterns = [
    path('', views.players, name='players'),
    path('<int:player_id>', views.player, name='player'),
]