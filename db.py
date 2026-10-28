"""Acceso a datos con SQLite (un solo archivo, sin servidor aparte).

Consultas parametrizadas y agregaciones en SQL para no cargar filas
innecesarias en memoria.
"""
import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS lecturas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    periodo TEXT NOT NULL,             -- AAAA-MM
    tipo TEXT NOT NULL,
    cantidad REAL NOT NULL CHECK (cantidad >= 0),
    co2e_kg REAL NOT NULL,
    creado TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_lecturas_periodo ON lecturas (periodo, tipo);
"""


def connect(path):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def add_reading(conn, periodo, tipo, cantidad, co2e):
    with conn:
        conn.execute(
            "INSERT INTO lecturas (periodo, tipo, cantidad, co2e_kg) VALUES (?,?,?,?)",
            (periodo, tipo, cantidad, co2e),
        )


def monthly_totals(conn, limit=12):
    """Totales por mes y tipo (últimos `limit` meses con datos)."""
    return conn.execute(
        """
        SELECT periodo, tipo, SUM(cantidad) AS cantidad, SUM(co2e_kg) AS co2e_kg
        FROM lecturas
        WHERE periodo IN (SELECT DISTINCT periodo FROM lecturas
                          ORDER BY periodo DESC LIMIT ?)
        GROUP BY periodo, tipo
        ORDER BY periodo DESC, tipo
        """,
        (limit,),
    ).fetchall()


def all_readings(conn):
    return conn.execute(
        "SELECT periodo, tipo, cantidad, co2e_kg FROM lecturas ORDER BY periodo, id"
    ).fetchall()


def delete_all(conn):
    with conn:
        conn.execute("DELETE FROM lecturas")
