"""An audit trail of who did what to money and access. Details never carry secrets."""

from __future__ import annotations

import json
import logging
import re
import time
from typing import Optional

from shopapp.db import Database

_SENSITIVE_KEY = re.compile(r"pass|token|secret|card|key|authorization", re.IGNORECASE)
MAX_DETAIL_CHARS = 500
log = logging.getLogger(__name__)


def redact(details: dict) -> dict:
    """The same details with the value of any sensitive-looking key replaced."""
    return {key: "[hidden]" if _SENSITIVE_KEY.search(str(key)) else value for key, value in details.items()}


def record(db: Database, actor: Optional[int], action: str, **details: object) -> None:
    log.info("audit %s by %s: %s", action, actor, details)
    text = json.dumps(redact(details), default=str, sort_keys=True)[:MAX_DETAIL_CHARS]
    db.add_audit(int(time.time()), actor, action, text)
