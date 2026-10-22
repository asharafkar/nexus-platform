from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import app, create_app

client = TestClient(app)

def test_root_returns_service_information() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "service": "nexus-platform",
        "message": "Nexus Platform is running",
    }

def test_health_check_returns_ok() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_lifespan_initializes_application_state()-> None:
    with TestClient(app) as test_client:
        assert test_client.app.state.settings.service_name == "Nexus Platform"

def test_create_app_uses_custom_settings()->None:
    custom_settings = Settings(
        _env_file=None,
        service_name="Nexus Test API",
        environment="testing",
    )

    test_app = create_app(custom_settings)

    assert test_app.title == "Nexus Test API"

    with TestClient(test_app) as test_client:
        assert test_client.app.state.settings.service_name == "Nexus Test API"