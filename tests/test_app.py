import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import carbon  # noqa: E402
from app import create_app  # noqa: E402


@pytest.fixture
def client(tmp_path):
    app = create_app(str(tmp_path / "test.db"))
    app.config["TESTING"] = True
    return app.test_client()


def token(client):
    html = client.get("/").get_data(as_text=True)
    return re.search(r'name="csrf" value="([0-9a-f]+)"', html).group(1)


def post_reading(client, periodo, tipo, cantidad, csrf=None):
    return client.post(
        "/registrar",
        data={"periodo": periodo, "tipo": tipo, "cantidad": cantidad,
              "csrf": csrf or token(client)},
        follow_redirects=True,
    )


# --- carbon.py -------------------------------------------------------------
def test_co2e_calculo():
    assert carbon.co2e_kg("electricidad", 100) == round(100 * carbon.FACTORS["electricidad"], 3)


def test_co2e_rechaza_negativos_y_tipos_invalidos():
    with pytest.raises(ValueError):
        carbon.co2e_kg("electricidad", -1)
    with pytest.raises(ValueError):
        carbon.co2e_kg("plutonio", 1)


def test_trend():
    assert carbon.trend(110, 100) == 10.0
    assert carbon.trend(5, 0) is None


# --- rutas -----------------------------------------------------------------
def test_inicio_vacio(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "Aún no hay lecturas" in r.get_data(as_text=True)


def test_registrar_y_resumen(client):
    post_reading(client, "2026-09", "electricidad", "200")
    r = post_reading(client, "2026-10", "electricidad", "300")
    html = r.get_data(as_text=True)
    assert "Lectura guardada" in html
    assert "+50.0%" in html


def test_validaciones(client):
    assert "formato AAAA-MM" in post_reading(client, "2026-13", "electricidad", "1").get_data(as_text=True)
    assert "tipo de consumo válido" in post_reading(client, "2026-10", "x", "1").get_data(as_text=True)
    assert "cantidad numérica válida" in post_reading(client, "2026-10", "gas_lp", "-5").get_data(as_text=True)
    assert "cantidad numérica válida" in post_reading(client, "2026-10", "gas_lp", "abc").get_data(as_text=True)


def test_csrf_obligatorio(client):
    client.get("/")
    r = client.post("/registrar", data={"periodo": "2026-10", "tipo": "gas_lp",
                                        "cantidad": "1", "csrf": "falso"})
    assert r.status_code == 400


def test_xss_escapado(client):
    # El tipo se valida, pero comprobamos que nada se refleje sin escapar.
    r = post_reading(client, "<script>", "electricidad", "1")
    assert "<script>" not in r.get_data(as_text=True)


def test_exportar_y_borrar(client):
    post_reading(client, "2026-10", "gas_lp", "10")
    csv_text = client.get("/exportar.csv").get_data(as_text=True)
    assert "2026-10,gas_lp,10.0,kg" in csv_text
    r = client.post("/borrar", data={"csrf": token(client)}, follow_redirects=True)
    assert "eliminados" in r.get_data(as_text=True)
    assert client.get("/exportar.csv").get_data(as_text=True).count("\n") == 1


def test_salud_y_cabeceras(client):
    r = client.get("/salud")
    assert r.json == {"estado": "ok"}
    assert "default-src 'none'" in r.headers["Content-Security-Policy"]
