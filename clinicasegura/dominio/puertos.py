from __future__ import annotations

from datetime import datetime
from typing import Protocol

from clinicasegura.dominio.modelos import Despacho, Receta


class Pasarela(Protocol):
    cadena: str

    def enviar(self, receta: Receta, folio: str,
               vence: datetime) -> Despacho: ...


class Reloj(Protocol):
    def ahora(self) -> datetime: ...


class GeneradorFolio(Protocol):
    def siguiente(self) -> str: ...


class Bitacora(Protocol):
    def registrar(self, evento: str, folio: str) -> None: ...
