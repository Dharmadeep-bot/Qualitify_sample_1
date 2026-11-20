"""App settings."""

import os

DEBUG = True
SECRET_KEY = "shopapp-dev-secret-key-do-not-use-1234567890"
DATABASE = os.environ.get("SHOP_DB", "shop.db")

# Payment gateway (sandbox)
PAYMENT_API_KEY = "demo_payment_api_key_0123456789abcdef"
PAYMENT_URL = "http://payments.example.internal/charge"

ADMIN_PASSWORD = "admin12345"
UPLOAD_DIR = "/tmp/uploads"
