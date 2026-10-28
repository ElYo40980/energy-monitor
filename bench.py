"""Medición simple de eficiencia: latencia, memoria pico y tamaño de respuesta.

Uso: python bench.py
Sirve como línea base para el monitoreo continuo del rendimiento: si estas
cifras empeoran entre versiones, el CI puede fallar.
"""
import os
import tempfile
import time
import tracemalloc

from app import create_app


def main(n_rows=2000, n_requests=200):
    with tempfile.TemporaryDirectory() as d:
        app = create_app(os.path.join(d, "bench.db"))
        c = app.test_client()
        import db, carbon
        conn = db.connect(app.config["DB_PATH"])
        with conn:
            for i in range(n_rows):
                periodo = f"{2020 + i // 12 % 6}-{i % 12 + 1:02d}"
                tipo = "electricidad" if i % 2 else "gas_lp"
                conn.execute(
                    "INSERT INTO lecturas (periodo,tipo,cantidad,co2e_kg) VALUES (?,?,?,?)",
                    (periodo, tipo, 100.0, carbon.co2e_kg(tipo, 100.0)))
        conn.close()

        c.get("/")  # calentamiento
        tracemalloc.start()
        t0 = time.perf_counter()
        for _ in range(n_requests):
            r = c.get("/")
        elapsed = time.perf_counter() - t0
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(f"Filas en BD:            {n_rows}")
        print(f"Latencia media GET /:   {elapsed / n_requests * 1000:.2f} ms")
        print(f"Memoria pico Python:    {peak / 1024:.0f} KiB")
        print(f"Tamaño HTML (/):        {len(r.data) / 1024:.1f} KiB")
        css = c.get("/static/style.css")
        print(f"Tamaño CSS:             {len(css.data) / 1024:.1f} KiB")


if __name__ == "__main__":
    main()
