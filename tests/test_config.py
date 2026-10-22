
import pytest

from app.core.config import Settings as AppSettings


def test_settings_use_default_values() -> None:
    settings = AppSettings(_env_file=None)

    assert settings.service_name == "Nexus Platform"
    assert settings.app_version == "0.1.0"
    assert settings.environment == "development"
    assert settings.debug is False


def test_settings_read_environment_variables(
    monkeypatch,
) -> None:
    monkeypatch.setenv("NEXUS_SERVICE_NAME", "Nexus Test API")
    monkeypatch.setenv("NEXUS_DEBUG", "true")

    settings = AppSettings(_env_file=None)

    assert settings.service_name == "Nexus Test API"
    assert settings.debug is True

def test_settings_reject_invalid_environment() -> None:
    with pytest.raises(ValueError):
         AppSettings(
            _env_file=None,
            environment="staging",
         )

def test_settings_reject_debug_in_production()-> None:
    with pytest.raises(ValueError):
        AppSettings(
            _env_file=None,
            environment="production",
            debug=True
        )
