# Qualitify sample 1: a deliberately bad shop API

A small Flask order/payments service written **badly on purpose** to test
Qualitify against. Do not deploy it. All keys and passwords in it are fake.

```
shopapp/app.py        HTTP routes (login, orders, checkout, refund, admin, upload)
shopapp/auth.py       login, tokens, roles
shopapp/db.py         sqlite data layer
shopapp/payments.py   card storage and charging
shopapp/reports.py    reports, exports, discount rules
shopapp/config.py     settings
shopapp/templates/    checkout page
```

Some problems only show when you follow data across files (e.g. a request
parameter in `app.py` that ends up in SQL in `db.py`, or a token that
`auth.py` trusts without a signature).
