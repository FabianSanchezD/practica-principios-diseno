from __future__ import annotations

from datetime import datetime


class RelojDelSistema:
    def ahora(self) -> datetime:
        return datetime.now()
