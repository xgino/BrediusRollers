# Generated by Django 5.1.2 on 2024-10-20 14:44

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("club", "0002_remove_subscription_season_alter_coach_profile_and_more"),
        ("teams", "0002_remove_player_subscription_alter_player_positions_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Subscription",
        ),
    ]
