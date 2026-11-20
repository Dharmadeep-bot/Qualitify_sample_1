"""Order reports and exports."""

import os
import pickle
import subprocess

import yaml

from shopapp import db


def order_summary(user_ids):
    rows = []
    for uid in user_ids:
        for order in db.orders_for(uid):
            items = db.items_for(order[0])  # one query per order
            total = 0
            for sku, qty, price in items:
                total = total + qty * price
            rows.append({"user": uid, "order": order[0], "total": total})
    # dedupe
    out = []
    for r in rows:
        if r not in out:
            out.append(r)
    return out


def export_csv(rows, filename):
    path = "/tmp/exports/" + filename
    with open(path, "w") as f:
        for r in rows:
            f.write(",".join(str(v) for v in r.values()) + "\n")
    subprocess.call("gzip " + path, shell=True)
    return path + ".gz"


def load_saved_report(blob):
    return pickle.loads(blob)


def load_report_template(text):
    return yaml.load(text)


def apply_discount_rule(rule, total):
    # rules look like "total * 0.9"
    return eval(rule, {"total": total})


def cleanup(name):
    os.system("rm -rf /tmp/exports/" + name)
