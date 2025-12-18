"""Schemas para paginação e respostas genéricas."""

from pydantic import BaseModel
from typing import TypeVar, Generic, List, Optional

T = TypeVar("T")


class PaginationParams(BaseModel):
    """Parâmetros de paginação."""

    skip: int = 0
    limit: int = 100

    class Config:
        # Validações
        ge = {"skip": 0, "limit": 1}  # skip >= 0, limit >= 1
        le = {"limit": 1000}  # limit <= 1000


class PaginatedResponse(BaseModel, Generic[T]):
    """Resposta paginada genérica."""

    data: List[T]
    total: int
    skip: int
    limit: int

    @property
    def has_next(self) -> bool:
        """Verifica se há próxima página."""
        return (self.skip + self.limit) < self.total

    @property
    def has_previous(self) -> bool:
        """Verifica se há página anterior."""
        return self.skip > 0


class ErrorResponse(BaseModel):
    """Resposta de erro."""

    error: str
    status_code: int
    error_code: Optional[str] = None
    details: Optional[dict] = None


class SuccessResponse(BaseModel, Generic[T]):
    """Resposta de sucesso genérica."""

    success: bool = True
    data: T
    message: Optional[str] = None
