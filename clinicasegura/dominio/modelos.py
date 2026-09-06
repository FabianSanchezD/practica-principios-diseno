from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from clinicasegura.dominio.errores import RecetaInvalida

PATRON_CEDULA = re.compile(r"^\d-\d{4}-\d{4}$")


@dataclass(frozen=True)
class Cedula:
    valor: str

    def __post_init__(self) -> None:
        if not PATRON_CEDULA.fullmatch(self.valor):
            raise RecetaInvalida(
                f"«{self.valor}» no tiene el formato 0-0000-0000."
            )

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
