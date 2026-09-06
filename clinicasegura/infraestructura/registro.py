from __future__ import annotations

from typing import Iterable, Mapping

from clinicasegura.dominio.puertos import Pasarela


def construir_registro(pasarelas: Iterable[Pasarela]) -> Mapping[str, Pasarela]:
    return {pasarela.cadena: pasarela for pasarela in pasarelas}
