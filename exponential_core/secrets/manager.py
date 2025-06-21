import boto3
import json

from datetime import datetime, timezone
from typing import Optional, Dict
from botocore.exceptions import ClientError


class SecretManager:
    def __init__(self, region_name: str = "us-east-1", default_ttl_seconds: int = 300):
        self._client = boto3.session.Session().client(
            "secretsmanager", region_name=region_name
        )
        self._cache: Dict[str, Dict] = {}
        self.default_ttl_seconds = default_ttl_seconds

    def get_secret(self, secret_name: str, ttl_seconds: Optional[int] = None) -> dict:
        """
        Obtiene un secreto desde AWS Secrets Manager, usando caché en memoria con TTL.

        Args:
            secret_name (str): Nombre del secreto.
            ttl_seconds (int, optional): Tiempo de vida en caché (por defecto usa el TTL global).

        Returns:
            dict: Secreto como diccionario Python.
        """
        now = datetime.now(timezone.utc)
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl_seconds

        if secret_name in self._cache:
            entry = self._cache[secret_name]
            elapsed = (now - entry["timestamp"]).total_seconds()

            if elapsed < ttl:
                return entry["value"]
            else:
                self._cache.pop(secret_name)

        # Recuperar desde AWS si no está o expiró
        try:
            response = self._client.get_secret_value(SecretId=secret_name)
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            raise RuntimeError(
                f"[SecretsManager] Error al obtener secreto '{secret_name}': {error_code}"
            ) from e

        if "SecretString" in response:
            secret_dict = json.loads(response["SecretString"])
        elif "SecretBinary" in response:
            secret_dict = json.loads(response["SecretBinary"].decode("utf-8"))
        else:
            raise ValueError(
                f"[SecretsManager] Secreto '{secret_name}' no contiene valores válidos."
            )

        self._cache[secret_name] = {"value": secret_dict, "timestamp": now}

        return secret_dict

    def invalidate(self, secret_name: Optional[str] = None):
        """
        Invalida uno o todos los secretos del caché.

        Args:
            secret_name (str, optional): Si se pasa, solo ese secreto será invalidado.
        """
        if secret_name:
            self._cache.pop(secret_name, None)
        else:
            self._cache.clear()
