"""Monitor de Consumo Energético: aplicación Flask ligera y sostenible."""
import csv
import io
import os
import re
import secrets
from datetime import date

from flask import (Flask, Response, abort, flash, g, redirect,
                   render_template, request, session, url_for)

import carbon
import db

PERIOD_RE = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")
MAX_AMOUNT = 1_000_000


def create_app(db_path=None):
    app = Flask(__name__)
    app.config["DB_PATH"] = db_path or os.environ.get("DB_PATH", "energia.db")
    # En producción define SECRET_KEY; en desarrollo se genera una efímera.
    app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(16)
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    def get_db():
        if "db" not in g:
            g.db = db.connect(app.config["DB_PATH"])
        return g.db

    @app.teardown_appcontext
    def close_db(_exc):
        conn = g.pop("db", None)
        if conn is not None:
            conn.close()

    # --- Seguridad básica -------------------------------------------------
    def csrf_token():
        if "csrf" not in session:
            session["csrf"] = secrets.token_hex(16)
        return session["csrf"]

    app.jinja_env.globals["csrf_token"] = csrf_token

    def check_csrf():
        sent = request.form.get("csrf", "")
        if not sent or not secrets.compare_digest(sent, session.get("csrf", "")):
            abort(400, "Token CSRF inválido")

    @app.after_request
    def headers(resp):
        resp.headers["Content-Security-Policy"] = (
            "default-src 'none'; style-src 'self'; form-action 'self'; "
            "base-uri 'none'; frame-ancestors 'none'"
        )
        resp.headers["X-Content-Type-Options"] = "nosniff"
        resp.headers["Referrer-Policy"] = "no-referrer"
        if request.path.startswith("/static/"):
            resp.headers["Cache-Control"] = "public, max-age=604800"
        return resp

    # --- Lógica de resumen --------------------------------------------------
    def build_summary(conn):
        rows = db.monthly_totals(conn)
        months = {}
        for r in rows:
            m = months.setdefault(r["periodo"], {"co2e": 0.0, "kinds": {}})
            m["kinds"][r["tipo"]] = {"cantidad": r["cantidad"], "co2e": r["co2e_kg"]}
            m["co2e"] += r["co2e_kg"]
        ordered = sorted(months.items(), reverse=True)
        change = {}
        by_kind = {}
        if ordered:
            current = ordered[0][1]["kinds"]
            previous = ordered[1][1]["kinds"] if len(ordered) > 1 else {}
            for kind in carbon.FACTORS:
                cur = current.get(kind, {}).get("cantidad", 0)
                prev = previous.get(kind, {}).get("cantidad", 0)
                by_kind[kind] = cur
                change[kind] = carbon.trend(cur, prev)
        total = round(sum(m["co2e"] for _, m in ordered), 1)
        peak = max((m["co2e"] for _, m in ordered), default=0) or 1
        return {
            "months": ordered,
            "total_co2e": total,
            "peak": peak,
            "change": change,
            "tips": carbon.recommendations(by_kind, change),
        }

    # --- Rutas ----------------------------------------------------------------
    @app.get("/")
    def index():
        summary = build_summary(get_db())
        return render_template(
            "index.html",
            s=summary,
            labels=carbon.LABELS,
            units=carbon.UNITS,
            today=date.today().strftime("%Y-%m"),
        )

    @app.post("/registrar")
    def registrar():
        check_csrf()
        periodo = request.form.get("periodo", "").strip()
        tipo = request.form.get("tipo", "")
        try:
            cantidad = float(request.form.get("cantidad", ""))
        except ValueError:
            cantidad = None
        if not PERIOD_RE.match(periodo):
            flash("El periodo debe tener formato AAAA-MM.", "error")
        elif tipo not in carbon.FACTORS:
            flash("Selecciona un tipo de consumo válido.", "error")
        elif cantidad is None or not (0 <= cantidad <= MAX_AMOUNT):
            flash("Ingresa una cantidad numérica válida.", "error")
        else:
            db.add_reading(get_db(), periodo, tipo, cantidad,
                           carbon.co2e_kg(tipo, cantidad))
            flash("Lectura guardada.", "ok")
        return redirect(url_for("index"))

    @app.get("/exportar.csv")
    def exportar():
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(["periodo", "tipo", "cantidad", "unidad", "co2e_kg"])
        for r in db.all_readings(get_db()):
            w.writerow([r["periodo"], r["tipo"], r["cantidad"],
                        carbon.UNITS.get(r["tipo"], ""), r["co2e_kg"]])
        return Response(
            buf.getvalue(), mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=consumo.csv"},
        )

    @app.post("/borrar")
    def borrar():
        check_csrf()
        db.delete_all(get_db())
        flash("Todos tus datos fueron eliminados.", "ok")
        return redirect(url_for("index"))

    @app.get("/acerca")
    def acerca():
        return render_template("acerca.html", factors=carbon.FACTORS,
                               labels=carbon.LABELS, units=carbon.UNITS)

    @app.get("/salud")
    def salud():
        get_db().execute("SELECT 1")
        return {"estado": "ok"}

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000)
