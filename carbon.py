"""Cálculo de huella de carbono y recomendaciones.

Módulo puro (sin E/S): fácil de probar, reutilizar y mantener.
Los factores son referenciales y se pueden sobrescribir con variables de
entorno para actualizarlos sin tocar el código (p. ej. cuando la autoridad
publique un nuevo factor de emisión del sistema eléctrico).
"""
import os

# kg CO2e por unidad. Valores referenciales: verificar el factor vigente
# publicado por la autoridad competente antes de usarlos en reportes oficiales.
FACTORS = {
    "electricidad": float(os.environ.get("FE_ELECTRICIDAD", "0.438")),  # kg CO2e / kWh
    "gas_lp": float(os.environ.get("FE_GAS_LP", "2.99")),               # kg CO2e / kg
}

UNITS = {"electricidad": "kWh", "gas_lp": "kg"}
LABELS = {"electricidad": "Electricidad", "gas_lp": "Gas LP"}


def co2e_kg(kind: str, amount: float) -> float:
    """Emisiones estimadas (kg CO2e) para una lectura."""
    if kind not in FACTORS:
        raise ValueError(f"Tipo de consumo no soportado: {kind}")
    if amount < 0:
        raise ValueError("El consumo no puede ser negativo")
    return round(amount * FACTORS[kind], 3)


def trend(current: float, previous: float):
    """Variación porcentual entre dos periodos; None si no hay base."""
    if previous <= 0:
        return None
    return round((current - previous) / previous * 100, 1)


def recommendations(by_kind: dict, change_pct: dict) -> list:
    """Sugerencias simples y transparentes basadas en reglas (sin IA opaca,
    sin envío de datos a terceros)."""
    tips = []
    elec = change_pct.get("electricidad")
    if elec is not None and elec > 10:
        tips.append(
            f"Tu consumo eléctrico subió {elec}% frente al mes anterior: "
            "revisa equipos en espera y aire acondicionado."
        )
    if by_kind.get("electricidad", 0) > 0 and (elec is None or elec <= 10):
        tips.append(
            "Cambia a iluminación LED y desconecta cargadores y equipos "
            "que no uses."
        )
    gas = change_pct.get("gas_lp")
    if gas is not None and gas > 10:
        tips.append(
            f"El consumo de gas LP subió {gas}%: revisa fugas y tapa las "
            "ollas al cocinar."
        )
    if not tips:
        tips.append("Registra tus consumos cada mes para detectar cambios a tiempo.")
    return tips
