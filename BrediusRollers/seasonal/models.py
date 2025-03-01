from django.db import models
from club_management.models import Address, Profile, Club, Coach, Role, TrainingTime, TrainingLocation
from django.urls import reverse
from datetime import date

class Season(models.Model):
    start_date = models.DateField(verbose_name="Start Date*")
    end_date = models.DateField(verbose_name="End Date*")

    def __str__(self):
        return f"{self.start_date} - {self.end_date}"

class Team(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, verbose_name="Season*")
    name = models.CharField(max_length=100, verbose_name="Name*")
    club = models.ForeignKey(Club, on_delete=models.CASCADE, verbose_name="Club*")
    league = models.CharField(max_length=50, choices=[
            ('Hoofdklasse', 'Hoofdklasse'),
            ('Overgangsklasse', 'Overgangsklasse'),
            ('Eerste Klasse', 'Eerste Klasse'),
            ('Tweede Klasse', 'Tweede Klasse'),
            ('Derde Klasse', 'Derde Klasse'),
            ('Vierde Klasse', 'Vierde Klasse'),
        ], verbose_name="league*")
    coach = models.ForeignKey(Coach, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.club} {self.name}"
    
    def get_name(self):
        return f"{self.club.name} {self.name}"

    def get_absolute_url(self):
        return reverse('Pages:team_filter', args=[self.id])


class Player(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Profile*")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name="Team*")
    position = models.CharField(max_length=50, choices=[
            ('aanvaller', 'Aanvaller'),
            ('middenvelder', 'Middenvelder'),
            ('verdediger', 'Verdediger'),
            ('goalkeeper', 'Goalkeeper'),
        ], verbose_name="Position*")
    number_plate = models.PositiveIntegerField(verbose_name="Number_plate*")
    captain = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.team} - {self.profile}"
    
    def calculate_total_goals_current_season(self):
        current_date = date.today()
        current_season = Season.objects.get(start_date__lte=current_date, end_date__gte=current_date)
        return self.score_set.filter(season=current_season).aggregate(total_goals=models.Sum('goals'))['total_goals']

    def calculate_total_assist_current_season(self):
        current_date = date.today()
        current_season = Season.objects.get(start_date__lte=current_date, end_date__gte=current_date)
        return self.score_set.filter(season=current_season).aggregate(total_assists=models.Sum('assists'))['total_assists']

class Game_day(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, verbose_name="Season*")
    sport_hall = models.CharField(max_length=100, verbose_name="Sporthal*")
    date = models.DateField(verbose_name="Date*")
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.date} | {self.sport_hall}"
    
    def formated_date(self):
        date = self.date
        return date.strftime("%Y-%m-%d")

class Game(models.Model):
    gameday = models.ForeignKey(Game_day, on_delete=models.CASCADE, verbose_name="Game Day*")
    league = models.CharField(max_length=50, choices=[
            ('Hoofdklasse', 'Hoofdklasse'),
            ('Overgangsklasse', 'Overgangsklasse'),
            ('Eerste Klasse', 'Eerste Klasse'),
            ('Tweede Klasse', 'Tweede Klasse'),
            ('Derde Klasse', 'Derde Klasse'),
            ('Vierde Klasse', 'Vierde Klasse'),
        ], verbose_name="league*")
    league_code = models.CharField(max_length=50, blank=True, null=True)
    field = models.PositiveIntegerField(verbose_name="Field*")
    start_time = models.TimeField(verbose_name="start time*")
    end_time = models.TimeField(verbose_name="end time*")
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='Home_Team', verbose_name="Home Team*")
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='Away_Team', verbose_name="Away Team*")
    home_score = models.IntegerField(blank=True, null=True)
    away_score = models.IntegerField(blank=True, null=True)

    
    def __str__(self):
        return f'{self.home_team} VS {self.away_team}'

    def battle(self):
        return f'{self.home_team.club.name} {self.home_team.name} VS {self.away_team.club.name} {self.away_team.name}'

    def gameday_sport_hall(self):
        return self.gameday.sport_hall
    
    def gameday_date(self):
        return self.gameday.date.strftime("%d-%m-%Y")

    def gameday_season(self):
        return self.gameday.season
    
    def home_team_name(self):
        return self.home_team.get_name()
    
    def away_team_name(self):
        return self.away_team.get_name()

    def formated_starttime(self):
        date = self.start_time
        return date.strftime("%H:%M")

    def long_formated_starttime(self):
        date = self.start_time
        return date.strftime("%H:%M:%S")

    def formated_endtime(self):
        date = self.end_time
        return date.strftime("%H:%M")

    def get_long_datetime(self):
        date = self.gameday.formated_date()
        time = self.long_formated_starttime()
        return f'{date} {time}'


class Training(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, verbose_name="Season*")
    date = models.DateField(verbose_name="Date*")
    training_time = models.ForeignKey(TrainingTime, on_delete=models.CASCADE, verbose_name="Training Time*")
    training_location = models.ForeignKey(TrainingLocation, on_delete=models.CASCADE, verbose_name="Training Location*")

    def __str__(self):
        return f"{self.training_time} | {self.date}"

class Score(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Player*")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name="Game*")
    goals  = models.PositiveIntegerField(verbose_name="Goals*", default=0)

    def __str__(self):
        return str(self.goals)
    
    def gameday_sport_hall(self):
        return self.game.gameday.sport_hall

    def matching(self):
        return f"{self.game.home_team.club.name} {self.game.home_team.name} VS {self.game.away_team.club.name} {self.game.away_team.name}"
    
class Photo(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Season")
    title  = models.CharField(max_length=15, verbose_name="Title -> 1x naam perdag, Verander naam hier != als file naam")
    photo = models.ImageField(upload_to="photo/", verbose_name="Photo")

    def __str__(self):
        return str(self.title)