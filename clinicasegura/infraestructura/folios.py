from __future__ import annotations

import uuid


class FoliosUnicos:
    def siguiente(self) -> str:
        return uuid.uuid4().hex[:12].upper()
