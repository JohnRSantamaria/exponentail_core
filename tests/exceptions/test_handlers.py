from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from exponential_core.exceptions import setup
from exponential_core.exceptions.types import InvoiceParsingError
from exponential_core.exceptions.middleware import GlobalExceptionMiddleware

app = FastAPI()
setup.setup_exception_handlers(app)
app.add_middleware(
    GlobalExceptionMiddleware
)  # 🔧 Importante para capturar Exception genérico


@app.get("/http-error")
def raise_http_error():
    raise HTTPException(status_code=404, detail="No encontrado")


@app.get("/custom-error")
def raise_custom_error():
    raise InvoiceParsingError("No se pudo extraer el NIT")


@app.get("/unhandled")
def raise_unhandled():
    raise ValueError("Algo inesperado")


client = TestClient(app)


def test_http_exception_handler():
    """Verifica que HTTPException sea convertida a error externo."""
    response = client.get("/http-error")
    assert response.status_code == 502
    assert response.json()["error_type"] == "ExternalServiceError"


def test_custom_app_exception_handler():
    """Verifica que las excepciones personalizadas se manejen correctamente."""
    response = client.get("/custom-error")
    assert response.status_code == 422
    assert response.json()["error_type"] == "InvoiceParsingError"
    assert "NIT" in response.json()["detail"]


def test_unhandled_exception_handler():
    """Verifica que errores no controlados sean manejados por el handler general."""
    response = client.get("/unhandled")
    assert response.status_code == 500
    assert response.json()["error_type"] == "UnhandledException"
