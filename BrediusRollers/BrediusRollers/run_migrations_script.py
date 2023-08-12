import subprocess

# Migration commands
migration_commands = """
    makemigrations accounts
    migrate accounts
    makemigrations club
    migrate club
    makemigrations teams
    migrate teams
    makemigrations players
    migrate players
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