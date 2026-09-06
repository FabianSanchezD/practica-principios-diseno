from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class Cedula:
    valor: str

    def __str__(self) -> str:
        return self.valor


@dataclass(frozen=True)
class Receta:
    cedula: Cedula
    medicamento: str
    dias: int
    dosis_mg: Decimal
    riesgo_alto: bool = False


@dataclass(frozen=True)
class Despacho:
    folio: str
    cadena: str
    vence: datetime
    recargo: Decimal = Decimal(0)
