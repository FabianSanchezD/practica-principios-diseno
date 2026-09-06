from __future__ import annotations

import sqlite3
from datetime import datetime


class BitacoraSQLite:
    def __init__(self, conexion: sqlite3.Connection):
        self.conexion = conexion
        self.conexion.execute(
            "CREATE TABLE IF NOT EXISTS bitacora "
            "(folio TEXT, evento TEXT, cuando TEXT)"
        )

    def registrar(self, evento: str, folio: str) -> None:
        self.conexion.execute(
            "INSERT INTO bitacora VALUES (?, ?, ?)",
            (folio, evento, datetime.now().isoformat()),
        )
        self.conexion.commit()
