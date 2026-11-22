# Qualitify sample 1: a shop API with a few bad parts

A small Flask shop (catalogue, cart, checkout with coupons, payments, refunds, webhooks, receipts, exports,
uploads, a checkout page) that is mostly written the way it should be, with a handful of problems mixed in,
the way they show up in real code. Qualitify should flag the problems and leave the good code alone.
Do not deploy it. All keys in it are fake.

```
shopapp/config.py          settings from the environment
shopapp/db.py             data layer
shopapp/auth.py           passwords and signed sessions
shopapp/authz.py          sign-in, admin, ownership checks
shopapp/catalog.py        product listing and search
shopapp/cart.py           cart parsing and pricing
shopapp/coupons.py        coupon codes
shopapp/payments.py       charging and refunds
shopapp/webhooks.py       payment-provider webhooks
shopapp/notifications.py  receipt emails
shopapp/audit.py          audit trail
shopapp/reports.py        reports and exports
shopapp/uploads.py        file uploads
shopapp/app.py            routes
shopapp/templates/        checkout and greeting pages
tests/                    the behaviour that is tested
```

## Run

```
pip install -r requirements.txt
set SHOP_SIGNING_KEY=<at least 32 random characters>
set SHOP_PAYMENT_URL=https://payments.example.com/charge
set SHOP_PAYMENT_CREDENTIAL=<from your provider>
set SHOP_MAIL_URL=https://mail.example.com/send
set SHOP_MAIL_KEY=<from your provider>
python -m shopapp.app
python -m pytest
```
