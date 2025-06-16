from exponential_core.exceptions.base import CustomAppException

class InvoiceParsingError(CustomAppException):
    def __init__(self, detail: str):
        super().__init__(f"Error al parsear factura: {detail}", status_code=422)


class OdooException(CustomAppException):
    def __init__(self, detail: str, data: dict = None):
        super().__init__(message=detail, status_code=502, data=data or {})
