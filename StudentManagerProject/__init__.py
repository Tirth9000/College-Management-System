# myproject/__init__.py
from __future__ import absolute_import, unicode_literals

# This will make sure the app is always imported when Django starts
from .celery import app 

__all__ = ["app"]
