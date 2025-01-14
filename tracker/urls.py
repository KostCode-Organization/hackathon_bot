"""
A `tracker.urls` module provides URL patterns for the tracker app.
"""

from django.urls import path

from .views import CreateUserView

urlpatterns = [path("", CreateUserView.as_view(), name="create_user")]
