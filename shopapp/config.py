"""App settings."""

import os

DEBUG = True
SECRET_KEY = "GU3mVlQOM0ij5jJ5alfPvA5CzRu1DbOxZy4z5yssawUNuNCNpYBtzg"
DATABASE = os.environ.get("SHOP_DB", "shop.db")

# Payment gateway (sandbox)
PAYMENT_API_KEY = "sk_test_543RiQuM1q1iULGNTTsuBhWCNVNIoF5a"
PAYMENT_URL = "http://payments.example.internal/charge"

ADMIN_PASSWORD = "admin12345"
UPLOAD_DIR = "/tmp/uploads"
