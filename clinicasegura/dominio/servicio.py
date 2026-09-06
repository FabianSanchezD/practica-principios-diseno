from __future__ import annotations

from clinicasegura.dominio.errores import (CadenaNoSoportada,
                                           FarmaciaNoDisponible)
from clinicasegura.dominio.modelos import Despacho, Receta
from clinicasegura.dominio.reglas import (TARIFA_DIARIA, VIGENCIA_DIAS,
                                          calcular_recargo, vencimiento)


class EmisionDeRecetas:
    def __init__(self, pasarelas, reloj, folios, bitacora):
        self.pasarelas = pasarelas
        self.reloj = reloj
        self.folios = folios
        self.bitacora = bitacora

    def emitir(self, receta: Receta, cadena: str) -> Despacho:
        pasarela = self.pasarelas.get(cadena)
        if pasarela is None:
            raise CadenaNoSoportada(
                f"Ninguna pasarela registrada atiende «{cadena}»."
            )

        vence = vencimiento(self.reloj.ahora(), VIGENCIA_DIAS)
        folio = self.folios.siguiente()
        recargo = calcular_recargo(receta.dias, TARIFA_DIARIA,
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
