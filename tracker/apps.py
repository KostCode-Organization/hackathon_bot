"""
A `tracker.apps` module that creates an app isntance
"""

from django.apps import AppConfig


class TrackerConfig(AppConfig):
    """
    A class that creates an app isntance
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "tracker"
