from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal

VIGENCIA_DIAS = 30
VIGENCIA_MAXIMA_DIAS = 90
TARIFA_DIARIA = Decimal("250")
FACTOR_RIESGO_ALTO = 2


def calcular_recargo(dias_restantes: int, tarifa_diaria: Decimal,
                     recargo_por_riesgo: bool) -> Decimal:
    factor = FACTOR_RIESGO_ALTO if recargo_por_riesgo else 1
    return tarifa_diaria * dias_restantes * factor


def vencimiento(emitida_en: datetime, vigencia_dias: int) -> datetime:
    return emitida_en + timedelta(days=vigencia_dias)
