from __future__ import annotations

import json
import urllib.error
import urllib.request
from datetime import datetime

from clinicasegura.dominio.errores import FarmaciaNoDisponible
from clinicasegura.dominio.modelos import Despacho, Receta

TIEMPO_LIMITE = 1.5
INTENTOS = 3


def _como_dict(receta: Receta) -> dict:
    return {
        "cedula": receta.cedula.valor,
        "medicamento": receta.medicamento,
        "dias": receta.dias,
        "dosis_mg": str(receta.dosis_mg),
        "riesgo_alto": receta.riesgo_alto,
    }


def _publicar(url: str, cuerpo: dict, tiempo_limite: float) -> int:
    ultima: Exception | None = None
    for _ in range(INTENTOS):
        peticion = urllib.request.Request(
            url,
            data=json.dumps(cuerpo).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(peticion, timeout=tiempo_limite) as r:
                return r.status
        except urllib.error.URLError as falla:
            ultima = falla
    raise FarmaciaNoDisponible(f"{url} no respondió en {INTENTOS} intentos") \
        from ultima


class PasarelaHTTP:
    cadena = ""

    def __init__(self, url: str, tiempo_limite: float = TIEMPO_LIMITE):
        self.url = url
        self.tiempo_limite = tiempo_limite

    def enviar(self, receta: Receta, folio: str, vence: datetime) -> Despacho:
        estado = _publicar(self.url, self._cuerpo(receta, folio, vence),
                           self.tiempo_limite)
        if estado >= 400:
            raise FarmaciaNoDisponible(
                f"«{self.cadena}» respondió {estado} al folio {folio}."
            )
        return Despacho(folio=folio, cadena=self.cadena, vence=vence)

    def _cuerpo(self, receta: Receta, folio: str, vence: datetime) -> dict:
        raise NotImplementedError


class FarmaUno(PasarelaHTTP):
    cadena = "farmauno"

    def _cuerpo(self, receta: Receta, folio: str, vence: datetime) -> dict:
        return {"rx": _como_dict(receta), "vence": vence.isoformat(),
                "folio": folio}


class SaludTotal(PasarelaHTTP):
    cadena = "saludtotal"

    def _cuerpo(self, receta: Receta, folio: str, vence: datetime) -> dict:
        return {"receta": _como_dict(receta),
                "expira": vence.strftime("%d/%m/%Y")}


class CruzVerde(PasarelaHTTP):
    cadena = "cruzverde"

    def _cuerpo(self, receta: Receta, folio: str, vence: datetime) -> dict:
        return {"Envelope": {"Receta": _como_dict(receta), "Folio": folio}}
