import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Core.settings')
import django
django.setup()
from django.core.management.base import BaseCommand


from faker import Faker
fake = Faker()
from datetime import datetime
import random

""" Import Models"""
from django.contrib.auth import get_user_model
User = get_user_model()
from accounts.model.profile import Profile
from accounts.model.adress import Adress
from club.models import Season, Sponsors, About, Photo, Coach, Club, Role, Subscription
from teams.models import League, Team, Player


# Accounts app
class AccountsDataGenerator:
    def __init__(self):
        self.generate_accounts_data()

    def generate_accounts_data(self):
        for _ in range(50):
            email = fake.email()
            first_name = fake.first_name()
            last_name = fake.last_name()
            password = 'testpassword'
            active = True
            staff = False
            admin = False

            user = User.objects.create(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
                active=active,
                staff=staff,
                admin=admin
            )
            
            gender = random.choice(['Dhr', 'Mevr'])
            phone = fake.phone_number()
            dob = fake.date_of_birth(minimum_age=18, maximum_age=90)
            bio = fake.paragraph(nb_sentences=2)
            hobby = fake.word()

            profile = Profile.objects.create(
                user=user,
                gender=gender,
                phone=phone,
                date_of_birth=dob,
                bio=bio,
                hobby=hobby
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

        print("Accounts testing data created successfully.")


# Club app
class ClubDataGenerator:
    def __init__(self):
        self.generate_seasons()
        self.generate_clubs()
        self.generate_sponsors()
        self.generate_coaches()
        self.generate_roles()
        self.generate_subscriptions()
        self.generate_abouts()
        self.generate_photos()
        print("Club testing data created successfully.")

    def generate_sponsors(self):
        for _ in range(4):
            Sponsors.objects.create(
                title=fake.company(),
                description=fake.paragraph(nb_sentences=2),
                short_description=fake.sentence(nb_words=3),
                logo='sponsor/default.jpg'
            )

    def generate_coaches(self):
        profiles = list(Profile.objects.all())
        for _ in range(3):
            coach_profile = profiles.pop()
            Coach.objects.create(profile=coach_profile)

    def generate_roles(self):
        profiles = list(Profile.objects.all())
        for _ in range(8):
            role_profile = profiles.pop()
            title = fake.job()
            short_description = fake.sentence(nb_words=5)
            description = fake.paragraph(nb_sentences=2)
            season = random.choice(Season.objects.all())

            Role.objects.create(
                profile=role_profile,
                title=title,
                short_description=short_description,
                description=description,
                season=season
            )

    def generate_seasons(self):
        for year in range(2022, 2026):
            Season.objects.create(
                name=year,
                members=random.randint(50, 200),
                start_date=fake.date_this_year(),
                end_date=fake.date_this_year(),
                first_training=fake.date_this_year(),
                last_training=fake.date_this_year()
            )

    def generate_clubs(self):
        seasons = Season.objects.all()
        bredius_rollers = None
        for season in seasons:
            bredius_rollers = Club.objects.create(
                    name="Bredius Rollers",
                    city=fake.city(),
                    season=season
                )
            for _ in range(10):
                name = fake.company()
                city = fake.city()

                club = Club.objects.create(
                    name=name,
                    city=city,
                    season=season
                )


    def generate_subscriptions(self):
        seasons = Season.objects.all()
        for season in seasons:
            sub_num = fake.unique.random_number(digits=6)
            fee = round(random.uniform(100, 500), 2)

            Subscription.objects.create(
                sub_num=sub_num,
                fee=fee,
                season=season
            )

    def generate_abouts(self):
        seasons = Season.objects.all()
        for season in seasons:
            description = fake.paragraph(nb_sentences=2)
            photo = 'about/default_image.jpg'

            About.objects.create(
                season=season,
                description=description,
                photo=photo
            )

    def generate_photos(self):
        seasons = Season.objects.all()
        for season in seasons:
            for _ in range(30):
                title = fake.word()
                description = fake.sentence(nb_words=5)
                photo = 'photo/default_image.jpg'

                Photo.objects.create(
                    title=title,
                    description=description,
                    season=season,
                    photo=photo
                )


# Team app
class TeamsDataGenerator:
    def __init__(self):
        self.generate_leagues()
        self.generate_teams()
        self.generate_players()
        print("Team testing data created successfully.")

    def generate_leagues(self):
        for _ in range(5):
            name = fake.word()
            shortname = fake.word()[:10]

            League.objects.create(
                name=name,
                shortname=shortname
            )

    def generate_teams(self):
        coaches = list(Coach.objects.all())
        seasons = Season.objects.all()
        clubs = Club.objects.all()
        leagues = League.objects.all()

        team_names = ['H1', 'H2', 'H3', 'H4', 'H5']  # Names for teams

        for club in clubs:
            for name in team_names:
                points_earned = random.randint(0, 100)
                matches_played = random.randint(0, 30)
                coach = random.choice(coaches)
                season = random.choice(seasons)
                league = random.choice(leagues)

                Team.objects.create(
                    name=f"{club.name} {name}",  # Combine club name with team name
                    points_earned=points_earned,
                    matches_played=matches_played,
                    coach=coach,
                    season=season,
                    club=club,
                    league=league
                )
    
    def generate_players(self):
        profiles = list(Profile.objects.all())
        teams = Team.objects.all()
        seasons = Season.objects.all()

        for team in teams:
            num_players = random.randint(7, 8)
            players_for_team = random.sample(profiles, num_players)
            
            for profile in players_for_team:
                positions = random.sample([choice[0] for choice in Player.POSITION_CHOICES], random.randint(1, 4))
                subscription = random.choice(Subscription.objects.all())
                number_plate = fake.random_int(min=1, max=99)
                season = random.choice(seasons)
                is_captain = random.choice([True, False])
                wish = fake.sentence(nb_words=6)

                Player.objects.create(
                    profile=profile,
                    team=team,
                    positions=positions,
                    subscription=subscription,
                    number_plate=number_plate,
                    season=season,
                    is_captain=is_captain,
                    wish=wish
                )






if __name__ == "__main__":
    AccountData = AccountsDataGenerator()
    ClubData = ClubDataGenerator()
    TeamData = TeamsDataGenerator()
