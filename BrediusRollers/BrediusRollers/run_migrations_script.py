
class Makemigrations:
    def __init__(self):
        self.migrations()
        print("Finished Migrations!")

    def migrations(self):
        import subprocess


        # Migration commands
        migration_commands = """
            makemigrations accounts
            migrate accounts
            makemigrations club
            migrate club
            makemigrations teams
            migrate teams
            makemigrations games
            migrate games
            makemigrations trainings
            migrate trainings
            makemigrations
            migrate
            """


        # Read and execute migration commands
        for command in migration_commands.strip().splitlines():
            subprocess.run(['python', 'manage.py'] + command.split())


class CreateSuperuser:
    def __init__(self):
        self.create_superuser()
        print("Finished Creating Admin!")

    def create_superuser(self):
        import os
        import sys
        import subprocess
        from django.conf import settings
        from django.apps import apps
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Core.settings")
        from django.contrib.auth import get_user_model

        # Ensure the apps are loaded
        apps.populate(settings.INSTALLED_APPS)

        User = get_user_model()

        email = "admin@admin.nl"
        password = "pass"

        try:
            user = User.objects.create_superuser(email=email, password=password)
            print("Superuser created successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    migrate = Makemigrations()
    admin = CreateSuperuser()