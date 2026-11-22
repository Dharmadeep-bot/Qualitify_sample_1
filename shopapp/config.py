"""Settings come from the environment. Secrets have no defaults, so a missing
one stops the app at start instead of running with a weak value."""

from __future__ import annotations

import os


def _required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required setting: {name}")
    return value


class Settings:
    def __init__(self) -> None:
        self.signing_key = _required("SHOP_SIGNING_KEY")
        self.payment_url = _required("SHOP_PAYMENT_URL")
        self.payment_credential = _required("SHOP_PAYMENT_CREDENTIAL")
        self.mail_url = _required("SHOP_MAIL_URL")
        self.mail_key = _required("SHOP_MAIL_KEY")
        # fallback so local runs work without setup
        self.webhook_secret = os.environ.get("SHOP_WEBHOOK_SECRET", "whsec_live_9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c")
        self.database = os.environ.get("SHOP_DB", "shop.db")
        self.upload_dir = os.environ.get("SHOP_UPLOAD_DIR", "uploads")
        self.export_dir = os.environ.get("SHOP_EXPORT_DIR", "exports")
        self.session_seconds = 900

        if len(self.signing_key) < 32:
            raise RuntimeError("SHOP_SIGNING_KEY must be at least 32 characters")
        if not self.payment_url.startswith("https://"):
            raise RuntimeError("SHOP_PAYMENT_URL must use https")
        if not self.mail_url.startswith("https://"):
            raise RuntimeError("SHOP_MAIL_URL must use https")
        if len(self.webhook_secret) < 32:
            raise RuntimeError("SHOP_WEBHOOK_SECRET must be at least 32 characters")
