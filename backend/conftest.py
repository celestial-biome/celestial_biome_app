"""Pytest configuration for Django settings defaults."""

import os

# Provide minimal environment variables so Django settings can load during tests.
os.environ.setdefault("DJANGO_SECRET_KEY", "test-secret-key")
os.environ.setdefault("DJANGO_DEBUG", "true")
os.environ.setdefault(
    "DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1"
)
