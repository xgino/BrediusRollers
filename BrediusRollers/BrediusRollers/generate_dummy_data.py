import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Core.settings')
from django.db import IntegrityError
from django.db.models import Q
import django
django.setup()
from django.core.management.base import BaseCommand

from tqdm import tqdm
from faker import Faker
fake = Faker()
from datetime import datetime, timedelta, time
import random

""" Import Models"""
from django.contrib.auth import get_user_model
User = get_user_model()
from accounts.model.profile import Profile
from accounts.model.adress import Adress
from club.models import Season, Sponsors, Photo, Coach, Club, Role
from teams.models import League, Team, Player
from games.models import Game, Game_day, Score
from trainings.models import Training, Trainings_location, Trainings_time


# Accounts app
class AccountsDataGenerator:
    def __init__(self):
        self.generate_accounts_data()

    def generate_accounts_data(self):
        total_users = 250  # Total number of users to generate
        with tqdm(total=total_users, desc="Generating accounts") as pbar: # Create a tqdm progress bar
            for _ in range(total_users):
                email = fake.email()
                password = 'testpassword'
                active = True
                staff = False
                admin = False

                user = User.objects.create(
                    email=email,
                    password=password,
                    active=active,
                    staff=staff,
                    admin=admin
                )
                
                firstname = fake.first_name()
                lastname = fake.last_name()
                gender = random.choice(['Dhr', 'Mevr'])

                profile = Profile.objects.create(
                    user=user,
                    firstname=firstname,
                    lastname=lastname,
                    gender=gender,
                )

                street = fake.street_name()
                house_number = fake.building_number()
                zipcode = fake.random_int(min=1000, max=9999)
                zipcode_number = fake.random_element(elements=['AB', 'CD', 'EF'])
                place = fake.city()

                address = Adress.objects.create(
                    street=street,
                    house_number=house_number,
                    zipcode=str(zipcode),
                    zipcode_number=zipcode_number,
                    place=place
                )

                profile.adress = address
                profile.save()
                pbar.update(1)  # Update the progress bar

        print("Accounts testing data created successfully.")


# Club app
class ClubDataGenerator:
    def __init__(self):

        self.total_methods = 7  # Total number of methods in the class
        with tqdm(total=self.total_methods, desc="Club Data Generation") as pbar:
            self.generate_seasons()
            pbar.update(1)
            
            self.generate_clubs()
            pbar.update(1)
            
            self.generate_sponsors()
            pbar.update(1)
            
            self.generate_coaches()
            pbar.update(1)
            
            self.generate_roles()
            pbar.update(1)
            
            self.generate_photos()
            pbar.update(1)

        print("Club testing data created successfully.")


    def generate_seasons(self):
        season_data = [
        (datetime(2021, 12, 1), datetime(2022, 11, 30)),
        (datetime(2022, 12, 1), datetime(2023, 11, 30)),
        (datetime(2023, 12, 1), datetime(2024, 11, 30)),
    ]
    
        # Loop through the season data and create seasons if they don't exist
        for start_date, end_date in season_data:
            existing_season = Season.objects.filter(start_date=start_date, end_date=end_date).first()
            
            if not existing_season:
                Season.objects.create(start_date=start_date, end_date=end_date)

    def generate_clubs(self):
        seasons = Season.objects.all()
        club_data = [
            ("Bredius Rollers", "Bredius_rollers"),
            ("Rappid Rollers", "Rappid_rollers"),
            ("Kampong", "Kampong"),
            ("Kenerme keine", "Kenerme"),
            ("Haag 88", "Haag"),
            ("Doing", "Doing"),
        ]
        
        for season in seasons:
            for club_name, variable_name in club_data:
                existing_club = Club.objects.filter(Q(name=club_name) & Q(season=season)).first()
                if not existing_club:
                    club = Club.objects.create(
                        name=club_name,
                        city=fake.city(),
                        season=season,
                        members=random.randint(50, 200),
                    )
                    locals()[variable_name] = club  # Assign created club to the corresponding variable name
                else:
                    locals()[variable_name] = existing_club  # Use existing club if found
            
    def generate_sponsors(self):
        clubs = Club.objects.all()
        seasons = Season.objects.filter(start_date__year__in=[2021, 2022, 2023])
        for club in clubs:
            for season in seasons:
                for _ in range(4):
                    Sponsors.objects.create(
                        title=fake.company(),
                    )

    def generate_coaches(self):
        all_seasons = Season.objects.all()
        all_profiles = list(Profile.objects.all())  # Convert queryset to a list

        for season in all_seasons:
            profiles_for_season = all_profiles.copy()
            random.shuffle(profiles_for_season)

            for _ in range(3):
                if not profiles_for_season:
                    break  # No more profiles left for this season
                profile = profiles_for_season.pop()
                
                try:
                    Coach.objects.create(season=season, profile=profile)
                except IntegrityError:
                    pass

    def generate_roles(self):
        all_seasons = Season.objects.all()

        for season in all_seasons:
            profiles = list(Profile.objects.order_by('?')[:9])  # Get 9 random profiles
            clubs = Club.objects.all()

            for club in clubs:
                for profile in profiles:
                    try:
                        Role.objects.create(
                            season=season,
                            profile=profile,
                            title=fake.job(),
                        )
                    except IntegrityError:
                        pass

    def generate_photos(self):
        all_seasons = Season.objects.all()
        for season in all_seasons:
            for _ in range(30):
                while True:
                    title = fake.unique.word()

                    try:
                        Photo.objects.create(season=season, title=title, photo='path/to/photo.jpg')
                        break
                    except IntegrityError:
                        pass


# Team app
class TeamsDataGenerator:
    def __init__(self):
        self.total_methods = 3  # Total number of methods in the class
        with tqdm(total=self.total_methods, desc="Team Data Generation") as pbar:
            self.generate_leagues()
            pbar.update(1)
            
            self.generate_teams()
            pbar.update(1)
            
            self.generate_players()
            pbar.update(1)

        print("Team testing data created successfully.")

    def generate_leagues(self):
        LEAGUE_CHOICES = [
            ('Hoofdklasse', 'Hoofdklasse'),
            ('Overgangsklasse', 'Overgangsklasse'),
            ('Eerste Klasse', 'Eerste Klasse'),
            ('Tweede Klasse', 'Tweede Klasse'),
            ('Derde Klasse', 'Derde Klasse'),
            ('Vierde Klasse', 'Vierde Klasse'),
        ]
        existing_league_names = set(League.objects.values_list('name', flat=True))
        for choice in LEAGUE_CHOICES:
            name = choice[0]
            if name not in existing_league_names:
                League.objects.create(name=name)
                existing_league_names.add(name)


    def generate_teams(self):
        all_seasons = Season.objects.all()
        team_names = ["H1", "H2", "H3", "H4", "H5"]

        for season in all_seasons:
            clubs_in_season = Club.objects.filter(season=season)
            
            for club in clubs_in_season:
                for name in team_names:
                    try:
                        league_code = random.choice(League.LEAGUE_CHOICES)[0]  # Choose a random league code
                        league = League.objects.get(name=league_code)  # Get the corresponding League instance
                        points_earned = random.randint(0, 30)
                        matches_played = random.randint(0, 12)
                        
                        # Get a random coach from the current season
                        coaches_in_season = Coach.objects.filter(season=season)
                        coach = random.choice(coaches_in_season)
                        
                        Team.objects.create(
                            club=club,
                            league=league,
                            name=name,
                            points_earned=points_earned,
                            matches_played=matches_played,
                            coach=coach
                        )
                    except IntegrityError:
                        pass
    
    def generate_players(self):
        all_profiles = Profile.objects.all()
        all_teams = Team.objects.all()

        position_choices = [
            ('forward', 'Forward'),
            ('midfielder', 'Midfielder'),
            ('defender', 'Defender'),
            ('goalkeeper', 'Goalkeeper'),
        ]

        for profile in all_profiles:
            if not Player.objects.filter(profile=profile).exists():  # Check if a player already exists with this profile
                team = random.choice(all_teams)  # Choose a random team
                
                positions = random.sample(position_choices, random.randint(1, 3))  # Choose 1 to 3 positions
                number_plate = random.randint(1, 99)  # Random number plate
                
                is_captain = random.choice([True, False])  # Randomly assign if the player is captain
                if is_captain:
                    # If the player is captain, make sure there's no other captain in the same team
                    if Player.objects.filter(team=team, is_captain=True).exists():
                        is_captain = False
                
                try:
                    Player.objects.create(
                        profile=profile,
                        team=team,
                        positions=positions,
                        number_plate=number_plate,
                        is_captain=is_captain,
                    )
                except IntegrityError:
                    pass


# Game App
class GameDataGenerator:
    def __init__(self):

        self.total_methods = 3  # Total number of methods in the class
        with tqdm(total=self.total_methods, desc="Game Data Generation") as pbar:
            self.generate_game_days()
            pbar.update(1)
            
            self.generate_games()
            pbar.update(1)
            
            self.generate_scores()
            pbar.update(1)

        print("Game testing data created successfully.")
    
    def generate_game_days(self):
        all_addresses = Adress.objects.all()
        all_seasons = Season.objects.all()
        
        for season in all_seasons:
            start_date = season.start_date
            end_date = season.end_date
            days_diff = (end_date - start_date).days
            
            for _ in range(20):
                sport_hall = fake.company()
                random_address = random.choice(all_addresses)
                
                days_to_add = random.randint(0, days_diff)
                game_day_date = start_date + timedelta(days=days_to_add)
                
                Game_day.objects.create(
                    sport_hall=sport_hall,
                    date=game_day_date,
                    adress=random_address,
                    season=season
                )


    def generate_games(self):
        all_seasons = Season.objects.all()
        all_game_days = Game_day.objects.all()

        for season in all_seasons:
            all_teams_in_season = Team.objects.filter(club__season=season)
            all_teams_list = list(all_teams_in_season)  # Convert to list for shuffling

            for game_day in all_game_days:
                for home_team in all_teams_list:
                    valid_away_teams = [team for team in all_teams_list if team != home_team]
                    if valid_away_teams:
                        away_team = random.choice(valid_away_teams)
                        league = random.choice(League.objects.all())
                        leauge_code = fake.random_element(elements=('A', 'B', 'C', 'D', 'E', 'F')) + str(random.randint(1, 10))
                        field = random.randint(1, 5)
                        start_time = datetime.combine(game_day.date, datetime.min.time()) + timedelta(minutes=random.randint(0, 23*60+59))
                        end_time = start_time + timedelta(minutes=random.randint(60, 180))
                        home_score = random.randint(0, 5)
                        away_score = random.randint(0, 5)

                        games_to_create = []
                        games_to_create.append(Game(
                            gameday=game_day,
                            league=league,
                            leauge_code=leauge_code,
                            field=field,
                            start_time=start_time.time(),
                            end_time=end_time.time(),
                            home_team=home_team,
                            away_team=away_team,
                            home_score=home_score,
                            away_score=away_score
                        ))

                        try:
                            Game.objects.bulk_create(games_to_create)  # Bulk insert
                        except IntegrityError:
                            pass


    def generate_scores(self):
        all_players = Player.objects.all()

        for player in all_players:
            seasons = Season.objects.all()

            for season in seasons:
                games_played = Game.objects.filter(
                    Q(home_team=player.team) | Q(away_team=player.team),
                    gameday__season=season
                ).prefetch_related('gameday__season')

                scores_to_create = []

                for game in games_played:
                    goals = random.choice([0, 1, 2, 3])

                    scores_to_create.append(Score(
                        season=season,
                        player=player,
                        game=game,
                        goals=goals,
                    ))

                try:
                    Score.objects.bulk_create(scores_to_create)
                except IntegrityError:
                    pass


# Training app
class TrainingDataGenerator:
    def __init__(self):
        self.total_methods = 3  # Total number of methods in the class
        with tqdm(total=self.total_methods, desc="Training Data Generation") as pbar:
            self.generate_training_time()
            pbar.update(1)
            
            self.generate_training_adres()
            pbar.update(1)
            
            self.generate_trainingen()
            pbar.update(1)

        print("Training testing data created successfully.")

    def generate_training_time(self):
        start_time = time(hour=10, minute=30)
        end_time = time(hour=12, minute=30)

        default_training_time, created = Trainings_time.objects.get_or_create(
            start_time=start_time, end_time=end_time
        )

    def generate_training_adres(self):
        addresses = Adress.objects.all()
        if addresses.exists():
            random_address = random.choice(addresses)
            training_location, created = Trainings_location.objects.get_or_create(
                adress=random_address
            )


    def generate_trainingen(self):
        seasons = Season.objects.all()
        latest_location = Trainings_location.objects.last()
        latest_time = Trainings_time.objects.last()

        for season in seasons:
            current_date = season.start_date
            while current_date <= season.end_date:
                if current_date.weekday() == 5:  # Saturday
                    Training.objects.get_or_create(
                        season=season,
                        training_time=latest_time,
                        training_location=latest_location,
                        date=current_date
                    )
                current_date += timedelta(days=1)


if __name__ == "__main__":
    AccountData = AccountsDataGenerator()
    ClubData = ClubDataGenerator()
    TeamData = TeamsDataGenerator()
    GameData = GameDataGenerator()
    TrainingData = TrainingDataGenerator()
