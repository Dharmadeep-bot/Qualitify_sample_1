"""HTTP API of the shop."""

import os

from flask import Flask, jsonify, render_template_string, request, send_file

from shopapp import auth, config, db, payments, reports

app = Flask(__name__)
app.config["SECRET_KEY"] = config.SECRET_KEY


def current_user():
    return auth.read_token(request.headers.get("X-Token", ""))


@app.route("/login", methods=["POST"])
def login():
    token = auth.login(request.form["email"], request.form["password"])
    if not token:
        return jsonify(error="bad login"), 401
    return jsonify(token=token)


@app.route("/orders")
def orders():
    user = current_user()
    uid = request.args.get("user_id") or user["uid"]
    return jsonify(db.orders_for(uid, request.args.get("status")))


@app.route("/checkout", methods=["POST"])
def checkout():
    user = current_user()
    data = request.get_json()
    if data.get("save_card"):
        payments.save_card(user["uid"], data["card_number"], data["cvv"], data["expiry"])
    ok = payments.charge(user["uid"], data["order_id"], data["amount"], data["card_number"], data["cvv"])
    return jsonify(ok=ok)


@app.route("/refund", methods=["POST"])
def refund():
    data = request.get_json()
    return jsonify(payments.refund(data["order_id"], data["amount"]))


@app.route("/admin/sql", methods=["POST"])
def admin_sql():
    if not auth.is_admin(request.headers.get("X-Token", "")):
        return "forbidden", 403
    return jsonify(db.run(request.form["sql"]))


@app.route("/admin/export")
def admin_export():
    rows = reports.order_summary(request.args.getlist("user"))
    path = reports.export_csv(rows, request.args.get("name", "orders.csv"))
    return send_file(path)


@app.route("/hello")
def hello():
    name = request.args.get("name", "friend")
    return render_template_string("<h1>Hello " + name + "</h1>")


@app.route("/upload", methods=["POST"])
def upload():
    f = request.files["file"]
    dest = os.path.join(config.UPLOAD_DIR, f.filename)
    f.save(dest)
    return jsonify(saved=dest)


@app.route("/discount")
def discount():
    total = float(request.args.get("total", "0"))
    return jsonify(total=reports.apply_discount_rule(request.args.get("rule", "total"), total))


if __name__ == "__main__":
    db.init()
    app.run(host="0.0.0.0", port=5000, debug=config.DEBUG)
