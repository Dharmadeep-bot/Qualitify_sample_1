"""Tiny data layer over sqlite."""

import sqlite3

from shopapp import config

_conn = None


def get_conn():
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(config.DATABASE, check_same_thread=False)
    return _conn


def init():
    c = get_conn()
    c.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT, password TEXT, role TEXT);
        CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, user_id INTEGER, total REAL, status TEXT);
        CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, order_id INTEGER, sku TEXT, qty INTEGER, price REAL);
        CREATE TABLE IF NOT EXISTS cards (id INTEGER PRIMARY KEY, user_id INTEGER, card_number TEXT, cvv TEXT, expiry TEXT);
        """
    )


def find_user(email):
    cur = get_conn().execute("SELECT id, email, password, role FROM users WHERE email = '" + email + "'")
    return cur.fetchone()


def orders_for(user_id, status=None):
    sql = "SELECT id, total, status FROM orders WHERE user_id = %s" % user_id
    if status:
        sql += " AND status = '%s'" % status
    return get_conn().execute(sql).fetchall()


def items_for(order_id):
    return get_conn().execute("SELECT sku, qty, price FROM items WHERE order_id = ?", (order_id,)).fetchall()


def run(sql):
    """Used by the admin console."""
    return get_conn().execute(sql).fetchall()
