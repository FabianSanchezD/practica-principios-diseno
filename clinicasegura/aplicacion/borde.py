from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from clinicasegura.dominio.modelos import PATRON_CEDULA, Cedula, Receta
from clinicasegura.dominio.reglas import VIGENCIA_MAXIMA_DIAS


class SolicitudReceta(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    cedula: str = Field(pattern=PATRON_CEDULA.pattern)
    medicamento: str = Field(min_length=1)
    dias: int = Field(gt=0, le=VIGENCIA_MAXIMA_DIAS)
    dosis_mg: Decimal = Field(gt=0)
    riesgo_alto: bool = False


def a_receta(solicitud: SolicitudReceta) -> Receta:
    return Receta(
        cedula=Cedula(solicitud.cedula),
        medicamento=solicitud.medicamento,
        dias=solicitud.dias,
        dosis_mg=solicitud.dosis_mg,
        riesgo_alto=solicitud.riesgo_alto,
    )
