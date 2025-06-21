# tests/exceptions/test_custom_exceptions.py

from exponential_core.exceptions.types import (
    InvoiceParsingError,
    OdooException,
    TaxIdNotFoundError,
)


def test_invoice_parsing_error():
    """Verifica que la excepción InvoiceParsingError tenga el mensaje y status correctos."""
    exc = InvoiceParsingError("Faltan datos")
    assert exc.message.startswith("Error al parsear factura")
    assert exc.status_code == 422


def test_odoo_exception():
    """Verifica que la excepción OdooException incluya datos y código 502."""
    exc = OdooException("Error Odoo", {"foo": "bar"})
    assert exc.status_code == 502
    assert "foo" in exc.data


def test_tax_id_not_found_error():
    """Verifica que TaxIdNotFoundError incluya invoice_number y candidatos."""
    exc = TaxIdNotFoundError("FAC123", [0.19, 0.05])
    assert exc.data["invoice_number"] == "FAC123"
