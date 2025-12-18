"""Definições de exceções customizadas."""

from typing import Any, Dict, Optional


class AppException(Exception):
    """Exceção base da aplicação."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
        super().__init__(self.message)


class ResourceNotFoundException(AppException):
    """Recurso não encontrado."""

    def __init__(self, resource: str, resource_id: Any = None):
        message = f"{resource} não encontrado"
        if resource_id:
            message = f"{resource} com ID {resource_id} não encontrado"
        super().__init__(message, status_code=404)


class ValidationException(AppException):
    """Erro de validação."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=400, details=details)


class ConflictException(AppException):
    """Conflito nos dados (ex: email duplicado)."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=409, details=details)


class UnauthorizedException(AppException):
    """Não autorizado."""

    def __init__(self, message: str = "Não autorizado"):
        super().__init__(message, status_code=401)
