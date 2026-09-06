from __future__ import annotations

from decimal import Decimal
from typing import Mapping

from clinicasegura.dominio.errores import (CadenaNoSoportada,
                                           FarmaciaNoDisponible)
from clinicasegura.dominio.modelos import Despacho, Receta
from clinicasegura.dominio.puertos import (Bitacora, GeneradorFolio,
                                           Pasarela, Reloj)
from clinicasegura.dominio.reglas import (TARIFA_DIARIA, VIGENCIA_DIAS,
                                          calcular_recargo, vencimiento)


class EmisionDeRecetas:
    def __init__(self, pasarelas: Mapping[str, Pasarela], reloj: Reloj,
                 folios: GeneradorFolio, bitacora: Bitacora):
        self.pasarelas = pasarelas
        self.reloj = reloj
        self.folios = folios
        self.bitacora = bitacora

    def emitir(self, receta: Receta, cadena: str,
               tarifa_diaria: Decimal = TARIFA_DIARIA,
               vigencia_dias: int = VIGENCIA_DIAS) -> Despacho:
        pasarela = self.pasarelas.get(cadena)
        if pasarela is None:
            raise CadenaNoSoportada(
                f"Ninguna pasarela registrada atiende «{cadena}»."
            )

        vence = vencimiento(self.reloj.ahora(), vigencia_dias)
        folio = self.folios.siguiente()
        recargo = calcular_recargo(receta.dias, tarifa_diaria,
                                   receta.riesgo_alto)

        try:
            despacho = pasarela.enviar(receta, folio, vence)
        except FarmaciaNoDisponible:
            raise
        except Exception as falla:
            raise FarmaciaNoDisponible(
                f"«{cadena}» no aceptó el folio {folio}: {falla}"
            ) from falla

        self.bitacora.registrar("emitida", folio)
        return Despacho(folio=despacho.folio, cadena=despacho.cadena,
                        vence=despacho.vence, recargo=recargo)
