from django.contrib import admin
from seasonal.models import Team, Player, Season, Game_day, Game, Training, Score

# Compact Admin Registration
models = [Team, Player, Season, Game_day, Game, Training, Score]

for model in models:
    admin.site.register(model)
