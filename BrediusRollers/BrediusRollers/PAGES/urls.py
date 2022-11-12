from django.urls import path
from . import views

app_name='Pages'

urlpatterns = [
    path('', views.home, name='home'),
    path('wedstrijden', views.wedstrijden, name='wedstrijden'),
    path('wedstrijden/<int:game_id>', views.wedstrijd, name='wedstrijd'),
    path('teams', views.teams, name='teams'),
    path('teams/<int:player_id>', views.player, name='player'),
    path('over-ons', views.overons, name='overons'),
    path('contact', views.contact, name='contact'),
]