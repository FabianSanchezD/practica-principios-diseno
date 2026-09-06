from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Mapping

from clinicasegura.dominio.errores import RecetaInvalida
from clinicasegura.dominio.modelos import Cedula, Receta

CAMPOS_REQUERIDOS = ("cedula", "medicamento", "dias", "dosis_mg")


def a_receta(datos: Mapping) -> Receta:
    faltantes = [c for c in CAMPOS_REQUERIDOS if c not in datos]
    if faltantes:
        raise RecetaInvalida(f"Faltan los campos {sorted(faltantes)}.")

    try:
        dias = int(datos["dias"])
        dosis_mg = Decimal(str(datos["dosis_mg"]))
    except (TypeError, ValueError, InvalidOperation) as falla:
        raise RecetaInvalida(f"Días o dosis no son numéricos: {falla}") from falla

    if dias <= 0:
        raise RecetaInvalida("Los días de tratamiento deben ser positivos.")
    if dosis_mg <= 0:
        raise RecetaInvalida("La dosis debe ser mayor que cero.")

    return Receta(
        cedula=Cedula(str(datos["cedula"])),
        medicamento=str(datos["medicamento"]),
        dias=dias,
        dosis_mg=dosis_mg,
        riesgo_alto=bool(datos.get("riesgo_alto", False)),
    )
