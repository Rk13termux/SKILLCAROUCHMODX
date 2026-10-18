"""Cielo estrellado: capa de fondo con profundidad.

Las estrellas van en coordenadas **% del lienzo**, así el mismo CSS sirve para
1080×1920, 1080×1440, 1080×1350 y 1080×1080 sin recalcular nada. Determinista:
misma semilla → mismas estrellas en todos los renders de todos los formatos.
"""

import random

SEMILLA = 20261007
FONDO = "0,0,0"   # negro puro


def capas_estrellas(n_tenues: int = 92, n_brillantes: int = 14,
                    semilla: int = SEMILLA) -> list:
    """Capas `background-image`: viñeta + estrellas.

    El orden es de arriba hacia abajo (primera capa = encima): la viñeta
    oscurece los bordes para que el contenido centre respalte y las estrellas
    periféricas se apaguen solas (profundidad).
    """
    rng = random.Random(semilla)
    capas = [
        f"radial-gradient(ellipse 74% 60% at 50% 46%, "
        f"rgba({FONDO},0) 0%, rgba({FONDO},0.30) 66%, "
        f"rgba({FONDO},0.62) 100%)",
    ]
    for _ in range(n_tenues):
        x, y = rng.uniform(1.5, 98.5), rng.uniform(1.0, 99.0)
        r = rng.choice((1.2, 1.5, 1.8, 2.2))
        a = rng.uniform(0.14, 0.46)
        capas.append(
            f"radial-gradient(circle at {x:.2f}% {y:.2f}%, "
            f"rgba(255,255,255,{a:.2f}) 0 {r}px, transparent {r + 1.8}px)")
    for _ in range(n_brillantes):
        x, y = rng.uniform(3.0, 97.0), rng.uniform(2.0, 98.0)
        capas.append(
            f"radial-gradient(circle at {x:.2f}% {y:.2f}%, "
            f"rgba(255,255,255,0.92) 0 2.4px, rgba(255,255,255,0.34) 3.6px, "
            f"transparent 11px)")
    return capas


def css_estrellas(n_tenues: int = 92, n_brillantes: int = 14,
                  semilla: int = SEMILLA) -> str:
    """Lista `background-image` (string): viñeta + estrellas."""
    return ", ".join(capas_estrellas(n_tenues, n_brillantes, semilla))


def posiciones_brillantes(semilla: int = SEMILLA,
                          n_tenues: int = 68, n_brillantes: int = 8):
    """(x%, y%) de las estrellas brillantes — para tests/verificación."""
    rng = random.Random(semilla)
    for _ in range(n_tenues):
        rng.uniform(1.5, 98.5)
        rng.uniform(1.0, 99.0)
        rng.choice((1.2, 1.5, 1.8, 2.2))
        rng.uniform(0.14, 0.46)
    return [(rng.uniform(3.0, 97.0), rng.uniform(2.0, 98.0))
            for _ in range(n_brillantes)]
