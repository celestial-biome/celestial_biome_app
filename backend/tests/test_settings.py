from django.conf import settings


def test_secret_key_is_configured():
    """Ensure the Django settings are populated for tests."""
    assert settings.SECRET_KEY == "test-secret-key"


def test_debug_default_true_in_tests():
    assert settings.DEBUG is True
