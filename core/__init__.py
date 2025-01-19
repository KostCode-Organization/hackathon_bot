"""
core/__init__.py
================

This module serves as the entry point for the `core` package of the project.
The `core` package is typicallydesigned to contain fundamental components,
utilities, or functionality that is used throughout the project.

Module Overview:
----------------
The `core` package acts as a central hub for core utilities, shared components,
or foundational services required by other parts of the application.
Specific functionality or implementations for the project may be further
broken into submodules or packages within `core`.
"""

from .celery import app as celery_app

__all__ = ("celery_app",)
