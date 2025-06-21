import pytest
from unittest.mock import patch, MagicMock
from exponential_core.secrets.manager import SecretManager
import datetime


@pytest.fixture
def fake_aws_secret():
    """Retorna un secreto falso simulado, usado en pruebas unitarias."""
    return {"SecretString": '{"API_KEY": "12345", "TOKEN": "abcd"}'}


def test_get_secret_caches_result(fake_aws_secret):
    """Verifica que el secreto se almacene en caché y no se llame dos veces a AWS."""
    with patch("boto3.session.Session.client") as mock_client:
        mock_instance = MagicMock()
        mock_instance.get_secret_value.return_value = fake_aws_secret
        mock_client.return_value = mock_instance

        manager = SecretManager(default_ttl_seconds=300)

        result_1 = manager.get_secret("my-secret")
        result_2 = manager.get_secret("my-secret")  # Esto debe salir del caché

        assert result_1 == {"API_KEY": "12345", "TOKEN": "abcd"}
        assert result_2 is result_1  # Mismo objeto (caché)
        assert mock_instance.get_secret_value.call_count == 1


def test_get_secret_respects_ttl(fake_aws_secret):
    """Verifica que el TTL se respete y que se vuelva a solicitar el secreto si ha expirado."""
    with patch("boto3.session.Session.client") as mock_client:
        mock_instance = MagicMock()
        mock_instance.get_secret_value.return_value = fake_aws_secret
        mock_client.return_value = mock_instance

        manager = SecretManager(default_ttl_seconds=1)
        manager.get_secret("my-secret")  # Primera vez → AWS

        # Forzar timestamp viejo para simular expiración
        manager._cache["my-secret"]["timestamp"] -= datetime.timedelta(seconds=2)

        manager.get_secret("my-secret")  # Segunda vez → nuevamente AWS
        assert mock_instance.get_secret_value.call_count == 2


def test_invalidate_removes_secret(fake_aws_secret):
    """Verifica que `invalidate()` remueve correctamente un secreto del caché."""
    with patch("boto3.session.Session.client") as mock_client:
        mock_instance = MagicMock()
        mock_instance.get_secret_value.return_value = fake_aws_secret
        mock_client.return_value = mock_instance

        manager = SecretManager()
        manager.get_secret("my-secret")

        assert "my-secret" in manager._cache
        manager.invalidate("my-secret")
        assert "my-secret" not in manager._cache


def test_invalidate_all(fake_aws_secret):
    """Verifica que `invalidate()` sin argumentos vacíe todo el caché."""
    with patch("boto3.session.Session.client") as mock_client:
        mock_instance = MagicMock()
        mock_instance.get_secret_value.return_value = fake_aws_secret
        mock_client.return_value = mock_instance

        manager = SecretManager()
        manager.get_secret("s1")
        manager.get_secret("s2")

        assert len(manager._cache) == 2
        manager.invalidate()
        assert len(manager._cache) == 0
