from typing import List
from exponential_core.exceptions.base import CustomAppException

class InvoiceParsingError(CustomAppException):
    def __init__(self, detail: str):
        super().__init__(f"Error al parsear factura: {detail}", status_code=422)


class OdooException(CustomAppException):
    def __init__(self, detail: str, data: dict = None):
        super().__init__(message=detail, status_code=502, data=data or {})

class TaxIdNotFoundError(CustomAppException):
    def __init__(self, invoice_number: str, candidates: list[float]):
        super().__init__(
            message=(
                f"No se encontró un tax_id válido para la factura '{invoice_number}'. "
                f"Porcentajes candidatos: {candidates}"
            ),
            status_code=422,
            data={
                "invoice_number": invoice_number,
                "candidates": candidates,
            },
        )


class ValidTaxIdNotFoundError(CustomAppException):
    def __init__(self, raw_ids: List[str]):
        super().__init__(
            message="No se encontraron identificadores fiscales válidos.",
            status_code=422,
            data={"candidates": raw_ids},
        )
