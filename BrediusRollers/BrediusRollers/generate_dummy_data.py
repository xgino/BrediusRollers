import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Core.settings')
import django
django.setup()


from django.contrib.auth import get_user_model
from accounts.model.profile import Profile
from accounts.model.adress import Adress
from club.models import Season, Sponsors, About, Photo, Coach, Club, Role

from faker import Faker
from datetime import datetime
import random



def generate_dummy_data():
    fake = Faker()

    """ ACCOUNTS APP """
    User = get_user_model()
    for _ in range(100):
        user = User.objects.create(
            email=fake.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            password='testpassword',
            active=True,
            staff=False,
            admin=False
        )

        profile, created = Profile.objects.get_or_create(
            user=user,
            defaults={
                'gender': fake.random_element(Profile.GENDER_CHOICES)[0],
                'phone': fake.phone_number(),
                'date_of_birth': fake.date_of_birth(),
                'bio': fake.text(max_nb_chars=200),
                'hobby': fake.sentence(),
                # Add other fields here as needed
            }
        )

        # Link the profile to an existing address or create a new one
        address = Adress.objects.first()  # Use an existing address or modify as needed
        if address:
            profile.adress = address
            profile.save()



    """ CLUBS APP """
    for _ in range(1):
        years = [2022, 2023, 2024, 2025]
        seasons = [
            Season.objects.create(
                name=year,
                members=100,
                start_date=datetime(year, 1, 1),
                end_date=datetime(year, 12, 31),
                first_training=datetime(year, 1, 1),
                last_training=datetime(year, 12, 31)
            ) for year in years
        ]

        all_seasons = Season.objects.all()

        club_instances = [
            Club.objects.create(
                name=fake.company(),
                city=fake.city(),
                season=season
            ) for season in all_seasons
        ]


        # Create an About instance
        about_instances = [
            About.objects.create(
                season=season,
                description="About Description",
                photo="about/default_image.jpg"  # You need to provide the actual path or URL to the photo image
            ) for season in all_seasons
        ]

        # Create Photo instances
        photo_instances = [
            Photo.objects.create(
                title="Photo Title",
                description="Photo Description",
                season=season,
                photo="about/default_image.jpg"  # Provide the actual path or URL to the photo image
            ) for season in all_seasons
        ]

        # Create Sponsors instances
        sponsor_instances = [
            Sponsors.objects.create(
                title="Sponsor Title",
                description="Sponsor Description",
                short_description="Sponsor Short Description",
                logo="sponsor/default.jpg"  # Provide the actual path or URL to the logo image
            ) for season in all_seasons
        ]






if __name__ == "__main__":
    generate_dummy_data()
