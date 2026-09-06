from __future__ import annotations

import os
import sqlite3
import tempfile
from pathlib import Path

from clinicasegura.dominio.servicio import EmisionDeRecetas
from clinicasegura.infraestructura.bitacora import BitacoraSQLite
from clinicasegura.infraestructura.folios import FoliosUnicos
from clinicasegura.infraestructura.pasarelas import (CruzVerde, FarmaUno,
                                                     SaludTotal)
from clinicasegura.infraestructura.registro import construir_registro
from clinicasegura.infraestructura.reloj import RelojDelSistema

CADENAS = (
    (FarmaUno, "FARMAUNO_URL", "https://api.farmauno.cr/v3/rx"),
    (SaludTotal, "SALUDTOTAL_URL", "https://ws.saludtotal.cr/api/recetas"),
    (CruzVerde, "CRUZVERDE_URL", "https://soap.cruzverde.cr/Recetas.asmx"),
)


def tiempo_limite() -> float:
    return int(os.environ.get("FARMACIA_TIMEOUT_MS", "1500")) / 1000


def ruta_de_bitacora() -> Path:
    por_omision = Path(tempfile.gettempdir()) / "clinicasegura.db"
    return Path(os.environ.get("CLINICA_BITACORA", por_omision))


def construir_servicio() -> EmisionDeRecetas:
    limite = tiempo_limite()
    pasarelas = [tipo(os.environ.get(variable, por_omision), limite)
                 for tipo, variable, por_omision in CADENAS]
    return EmisionDeRecetas(
        pasarelas=construir_registro(pasarelas),
        reloj=RelojDelSistema(),
        folios=FoliosUnicos(),
        bitacora=BitacoraSQLite(sqlite3.connect(ruta_de_bitacora())),
    )
