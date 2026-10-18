"""Fondos deterministas para los slides.

Todo se define en % del lienzo (o en un viewBox 1080×1920) con semilla fija:
el mismo CSS sirve para 1080×1920, 1620, 1440, 1350 y 1080, y el render es
reproducible slide a slide.

Composición
-----------
`.slide::before` (todas las capas cubren el área completa, sin background-size):
    1. viñeta     — apaga los bordes y centra la atención
    2. mesh       — radiales del color de acento (intensidad por rol)
    3. base       — degradado vertical del negro

`.slide::after` (texturas, con `background-size` y máscara propias):
    · circuitos (por defecto) / grid / puntos / nodos / topología / beams
    · grano anti-banding (feTurbulence, ~5 % de opacidad)
    La máscara las desvanece hacia los bordes.

El fondo de la casa son los **circuitos** (`VARIANTE_DEFECTO`): `auto` —y por
lo tanto el default de `--fondo`— los usa en todos los verticales y roles.

`--fondo-fijo` (fuera de este módulo) fuerza el rol «contenido» para todos los
slides; acá `rol` decide la intensidad del mesh y la forma del código fantasma.
"""

from __future__ import annotations

import base64
import html as _html
import random

NEGRO = "0,0,0"
SEMILLA = 20261018

# Variantes aceptadas por --fondo (auto = el fondo de la casa: circuitos).
VARIANTES = ("auto", "base", "mesh", "grid", "puntos", "circuitos", "nodos",
             "topologia", "beams", "codigo")

TEXTURAS = ("grid", "puntos", "circuitos", "nodos", "topologia", "beams")

# El fondo de la casa: lo que usa `auto` en todos los verticales y roles.
VARIANTE_DEFECTO = "circuitos"

ROLES = ("cover", "contenido", "puente", "cierre")

# (x%, y%, tamaño%, alpha) de cada glow del acento.
_MESH = {
    "cover": ((86, 6, 46, 0.30), (10, 94, 50, 0.22), (50, 46, 58, 0.10)),
    "contenido": ((88, 8, 40, 0.15), (8, 92, 42, 0.11)),
    "puente": ((50, 104, 74, 0.20),),
    "cierre": ((50, 106, 84, 0.34), (88, 8, 40, 0.13)),
}
# Multiplicador del variante "mesh" (glows más marcados).
_MESH_ESCALA = {"cover": 1.35, "contenido": 1.7, "puente": 1.6, "cierre": 1.2}

_BASE = "linear-gradient(180deg, #111116 0%, #09090C 52%, #0B0B0D 100%)"


# ── capas de ::before ──────────────────────────────────────────────

def _vineta() -> str:
    """Viñeta: oscurece los bordes y centra la atención en el contenido."""
    return (f"radial-gradient(ellipse 74% 60% at 50% 46%, "
            f"rgba({NEGRO},0) 0%, rgba({NEGRO},0.30) 66%, "
            f"rgba({NEGRO},0.62) 100%)")


def _mesh(rgb, rol: str, escala: float = 1.0):
    r, g, b = rgb
    glows = _MESH.get(rol, _MESH["contenido"])
    capas = []
    for x, y, tam, a in glows:
        a = min(0.55, a * escala)
        capas.append(f"radial-gradient(circle at {x}% {y}%, "
                     f"rgba({r},{g},{b},{a:.3f}) 0%, transparent {tam}%)")
    return capas


# ── texturas (van en ::after) ──────────────────────────────────────

def _grano(op: float = 0.05) -> str:
    """Ruido monocromo como imagen SVG en base64 (tile de 140×140).

    `op` es la opacidad del rect de ruido: ~0.05 deja un grano apenas
    perceptible que rompe el banding de los degradados en OLED sin ensuciar
    el texto. Más de 0.15 se convierte en una bruma gris.
    """
    svg = ("<svg xmlns='http://www.w3.org/2000/svg' width='140' height='140'>"
           "<filter id='n'>"
           "<feTurbulence type='fractalNoise' baseFrequency='0.9' "
           "numOctaves='2' stitchTiles='stitch'/>"
           "<feColorMatrix type='saturate' values='0'/>"
           "</filter>"
           f"<rect width='140' height='140' filter='url(#n)' opacity='{op}'/>"
           "</svg>")
    return "url(\"data:image/svg+xml;base64," + \
        base64.b64encode(svg.encode("utf-8")).decode() + "\")"


def _svg(cuerpo: str, w: int = 1080, h: int = 1920) -> str:
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}' "
           f"viewBox='0 0 {w} {h}' fill='none'>{cuerpo}</svg>")
    return "url(\"data:image/svg+xml;base64," + \
        base64.b64encode(svg.encode("utf-8")).decode() + "\")"


def _grid(alpha: float = 0.09, px: int = 92):
    linea = f"rgba(255,255,255,{alpha}) 0 1px, transparent 1px {px}px"
    return ([f"repeating-linear-gradient(0deg, {linea})",
             f"repeating-linear-gradient(90deg, {linea})"],
            [f"{px}px {px}px", f"{px}px {px}px"])


def _puntos(alpha: float = 0.16, px: int = 38):
    img = (f"radial-gradient(circle, rgba(255,255,255,{alpha}) 1.5px, "
           f"transparent 1.8px)")
    return [img], [f"{px}px {px}px"]


def _circuitos(rgb, semilla: int = SEMILLA, n: int = 24):
    """Trazas ortogonales con nodos (estilo PCB)."""
    r, g, b = rgb
    rng = random.Random(semilla)
    paso = 54
    trazos, nodos = [], []
    for _ in range(n):
        x = round(rng.randrange(1, 19) * paso)
        y = round(rng.randrange(1, 34) * paso)
        pts, cx, cy = [], x, y
        for _ in range(rng.randint(2, 4)):
            if rng.random() < 0.5:
                cx = min(1035, max(45, cx + paso * rng.choice((-2, -1, 1, 2))))
            else:
                cy = min(1875, max(45, cy + paso * rng.choice((-2, -1, 1, 2))))
            pts.append(f"L{cx} {cy}")
        trazos.append(f"<path d='M{x} {y} {' '.join(pts)}' "
                      f"stroke='rgba({r},{g},{b},0.45)' stroke-width='2' "
                      "stroke-linecap='round'/>")
        for (px_, py_) in ((x, y), (cx, cy)):
            nodos.append(f"<circle cx='{px_}' cy='{py_}' r='5' "
                         f"fill='rgba({r},{g},{b},0.7)'/>")
    return _svg("".join(trazos) + "".join(nodos))


def _nodos(rgb, semilla: int = SEMILLA, n: int = 32):
    """Red de puntos conectados (estilo grafo / red neuronal)."""
    r, g, b = rgb
    rng = random.Random(semilla)
    pts = [(rng.uniform(60, 1020), rng.uniform(80, 1840)) for _ in range(n)]
    lineas = []
    for x1, y1 in pts:
        vecinos = sorted(pts, key=lambda p: (p[0] - x1) ** 2 + (p[1] - y1) ** 2)[1:3]
        for x2, y2 in vecinos:
            lineas.append(f"<line x1='{x1:.0f}' y1='{y1:.0f}' x2='{x2:.0f}' "
                          f"y2='{y2:.0f}' stroke='rgba({r},{g},{b},0.22)' "
                          "stroke-width='1.6'/>")
    circ = "".join(f"<circle cx='{x:.0f}' cy='{y:.0f}' "
                   f"r='{rng.uniform(2.5, 6):.1f}' "
                   f"fill='rgba({r},{g},{b},0.55)'/>" for x, y in pts)
    return _svg("".join(lineas) + circ)


def _topologia(rgb, semilla: int = SEMILLA):
    """Tres filas de nodos conectadas (esquema de red / infra)."""
    r, g, b = rgb
    rng = random.Random(semilla)
    filas = ((300, 4), (900, 5), (1500, 4))
    cajas, lineas, centros = [], [], []
    for y, cuantas in filas:
        xs = [180 + i * (720 / max(1, cuantas - 1)) for i in range(cuantas)]
        centros.append([(x, y) for x in xs])
        for x in xs:
            cajas.append(f"<rect x='{x - 40:.0f}' y='{y - 40:.0f}' width='80' "
                         "height='80' rx='16' stroke="
                         f"'rgba({r},{g},{b},0.4)' stroke-width='2'/>")
    for a, b_ in zip(centros, centros[1:]):
        for x1, y1 in a:
            for x2, y2 in b_:
                if abs(x1 - x2) < 320 and rng.random() < 0.55:
                    lineas.append(f"<line x1='{x1:.0f}' y1='{y1:.0f}' "
                                  f"x2='{x2:.0f}' y2='{y2:.0f}' "
                                  f"stroke='rgba({r},{g},{b},0.2)' "
                                  "stroke-width='1.6'/>")
    return _svg("".join(lineas) + "".join(cajas))


def _beams(rgb, semilla: int = SEMILLA, n: int = 7):
    """Haces de luz: un conic-gradient desde arriba del lienzo."""
    r, g, b = rgb
    rng = random.Random(semilla)
    paradas = ["transparent 0deg"]
    ang = 0.0
    for _ in range(n):
        w = rng.uniform(3.0, 7.5)
        hueco = rng.uniform(7, 17)
        a = rng.uniform(0.05, 0.12)
        paradas.append(f"rgba({r},{g},{b},{a:.3f}) {ang + w * 0.2:.1f}deg")
        paradas.append(f"rgba({r},{g},{b},{a:.3f}) {ang + w:.1f}deg")
        paradas.append(f"transparent {ang + w + hueco:.1f}deg")
        ang += w + hueco
    paradas.append(f"transparent {max(ang, 360):.1f}deg")
    return "conic-gradient(from 180deg at 50% -14%, " + ", ".join(paradas) + ")"


def _textura(nombre: str, rgb, semilla: int = SEMILLA):
    """(imagenes, tamaños, mascara) de la textura pedida."""
    # La máscara deja la textura más marcada en los BORDES y más tenue en el
    # centro, que es donde vive el texto: identidad visual sin pelear legibilidad.
    mascara_radial = ("radial-gradient(ellipse 92% 78% at 50% 46%, "
                      "rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.72) 55%, #000 100%)")
    mascara_arriba = "linear-gradient(180deg, #000 0%, transparent 74%)"
    if nombre == "grid":
        img, tam = _grid()
        return img, tam, mascara_radial
    if nombre == "puntos":
        img, tam = _puntos()
        return img, tam, mascara_radial
    if nombre == "circuitos":
        return [_circuitos(rgb, semilla)], ["100% 100%"], mascara_radial
    if nombre == "nodos":
        return [_nodos(rgb, semilla)], ["100% 100%"], mascara_radial
    if nombre == "topologia":
        return [_topologia(rgb, semilla)], ["100% 100%"], mascara_radial
    if nombre == "beams":
        return [_beams(rgb, semilla)], ["100% 100%"], mascara_arriba
    return [], [], mascara_radial


# ── código fantasma ────────────────────────────────────────────────

def codigo_html(comandos=None, semilla: int = SEMILLA, lineas: int = 30,
                con_numeros: bool = True) -> str:
    """Código/comandos reales del carrusel como capa de fondo (muy tenue)."""
    base = [c.strip() for c in (comandos or []) if c and c.strip()]
    if not base:
        base = ["python3 -m pip install --user requests",
                "python3 script.py --verbose",
                "git add -A && git commit -m 'feat: fondo'",
                "curl -s localhost:8000/health",
                "cat datos.csv | head -5"]
    rng = random.Random(semilla)
    filas = []
    for i in range(lineas):
        c = base[i % len(base)]
        prefijo = (f"<span class='ln'>{i + 1:02d}</span>"
                   if con_numeros else "")
        filas.append(f"<div>{prefijo}{_html.escape(c)}</div>")
    rng.shuffle(filas)  # determinista: misma semilla → mismo orden
    return ("<div class='fondo-codigo' aria-hidden='true'>"
            + "".join(filas) + "</div>")


# ── composición ────────────────────────────────────────────────────

def capas_before(rgb, rol: str = "cover") -> list:
    """Capas de `.slide::before`: viñeta + mesh + degradado base."""
    return [_vineta()] + _mesh(rgb, rol) + [_BASE]


def fondo_simple(rgb=(250, 204, 21), rol: str = "cover") -> str:
    """Fondo en una sola declaración (story): sin textura ni grano."""
    return ", ".join(capas_before(rgb, rol))


def fondo(rol: str = "contenido", vertical: str = "tech", rgb=(250, 204, 21),
          variante: str = "auto", comandos=None, semilla: int = SEMILLA,
          con_codigo: bool = True) -> dict:
    """Capas de fondo de un slide.

    Devuelve un dict listo para sustituir en el template:
        fondo, textura, textura_size, textura_mask, textura_op, codigo
    """
    variante = variante if variante in VARIANTES else "auto"
    if rol not in ROLES:
        rol = "contenido"

    solo_base = variante == "base"
    escala = _MESH_ESCALA.get(rol, 1.0) if variante == "mesh" else 1.0
    r, g, b = rgb

    # ::before ─ "base" es el look liso (sin textura ni grano); el resto
    # suma el mesh propio del rol.
    if solo_base:
        # Ojo: background-image sólo acepta imágenes, no colores sueltos; el
        # negro final va como gradiente plano o Chromium descarta la regla.
        capas = [
            f"radial-gradient(circle at 85% 8%, rgba({r},{g},{b},0.14),"
            " transparent 45%)",
            f"radial-gradient(circle at 8% 92%, rgba({r},{g},{b},0.10),"
            " transparent 45%)",
        ] + [_vineta()] + [f"linear-gradient(#0B0B0D, #0B0B0D)"]
    else:
        capas = [_vineta()]
        capas.extend(_mesh(rgb, rol, escala))
        capas.append(_BASE)

    # ::after ─ textura (el fondo de la casa o la pedida) + grano anti-banding
    if variante == "auto":
        nombre = VARIANTE_DEFECTO
    elif variante in TEXTURAS:
        nombre = variante
    else:
        nombre = ""
    img, tam, mascara = _textura(nombre, rgb, semilla)
    if not solo_base:
        img = img + [_grano()]
        tam = tam + ["140px 140px"]

    # código fantasma: en el fondo de la casa solo cuando hay comandos reales
    con_codigo = con_codigo and not solo_base and variante in (
        "auto", VARIANTE_DEFECTO, "codigo")
    codigo = codigo_html(comandos, semilla) if con_codigo else ""

    return {
        "fondo": ", ".join(capas),
        "textura": ", ".join(img) if img else "none",
        "textura_size": ", ".join(tam) if tam else "auto",
        "textura_mask": mascara if img else "none",
        "textura_op": "1",
        "codigo": codigo,
    }
