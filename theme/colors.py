"""Tokens de color: paleta técnica TechEdu.

El acento NO vive aquí: llega como HEX del usuario por CLI y se convierte en
CSS vars por slide. Aquí sólo están los colores fijos y las utilidades de
contraste.
"""

FONDO = "#000000"
FONDO_SUAVE = "#141417"
FONDO_CODIGO = "#0F172A"
SUPERFICIE = "#1F2937"
BORDE = "#26262B"
BORDE_CLARO = "#334155"

TEXTO = "#FFFFFF"
TEXTO_SUAVE = "#E5E7EB"
TEXTO_TENUE = "#9CA3AF"
GRIS = "#8E8E93"

OK = "#10B981"          # comandos exitosos, checks
INFO = "#3B82F6"        # card info
WARN = "#F59E0B"        # warnings educativos
PELIGRO = "#EF4444"     # errores, mitos
RESALTE_DEFECTO = "#FFB800"  # keywords (ámbar, contraste estable sobre negro)

# Variantes de card-info: (borde, icono)
VARIANTES = {
    "info": (INFO, "i"),
    "tip": (OK, "✓"),
    "warn": (WARN, "!"),
    "danger": (PELIGRO, "✕"),
}

PALETA = {
    "rojo": "#E63946",
    "azul": "#2563EB",
    "verde": "#10B981",
    "purpura": "#8B5CF6",
    "naranja": "#F97316",
    "rosa": "#EC4899",
    "dorado": "#FFD700",
    "cian": "#06B6D4",
    "lima": "#84CC16",
}


def normalizar_hex(valor: str) -> str:
    """Devuelve un #RRGGBB mayúsculas o lanza ValueError."""
    v = (valor or "").strip()
    if not v.startswith("#"):
        v = PALETA.get(v.lower(), v)
    v = v.upper()
    if len(v) == 4:  # #RGB → #RRGGBB
        v = "#" + "".join(c * 2 for c in v[1:])
    if not __import__("re").match(r"^#[0-9A-F]{6}$", v):
        nombres = ", ".join(sorted(PALETA))
        raise ValueError(
            f"Color no reconocido: {valor!r}. "
            f"Esperaba un HEX #RRGGBB (ej: #06B6D4) o #RGB (ej: #0BD), "
            f"o un nombre de paleta: {nombres}."
        )
    return v


def resuelve_resalte(resalte: str | None, hex_color: str) -> str:
    """Color de keywords: el que pidió el usuario, si no el MISMO --color.

    `resalte=None` significa "no lo pidió": en ese caso las keywords usan el
    acento del tema para que todo el carrusel viva de un solo color.
    """
    return normalizar_hex(resalte) if resalte else normalizar_hex(hex_color)


def rgb(hex_color: str):
    h = normalizar_hex(hex_color).lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def acento_vars(hex_color: str) -> dict:
    """Vars CSS + tuples RGB para el acento (del HEX del usuario)."""
    r, g, b = rgb(hex_color)
    br = (
        min(255, int(r + (255 - r) * 0.45)),
        min(255, int(g + (255 - g) * 0.45)),
        min(255, int(b + (255 - b) * 0.45)),
    )
    return {
        "accent": normalizar_hex(hex_color),
        "accent_bright": f"#{br[0]:02x}{br[1]:02x}{br[2]:02x}",
        "accent_rgba": f"rgba({r},{g},{b},0.14)",
        "accent_rgba_b": f"rgba({r},{g},{b},0.10)",
        "accent_rgba_30": f"rgba({r},{g},{b},0.30)",
        "accent_rgba_40": f"rgba({r},{g},{b},0.40)",
        "rgb": (r, g, b),
        "bright_rgb": br,
    }


def luminancia(hex_color: str) -> float:
    r, g, b = rgb(hex_color)
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255.0


def contraste(fg: str, bg: str) -> float:
    """Contraste WCAG 2.x (1.0 - 21.0)."""
    def lum(h):
        r, g, b = rgb(h)
        def canal(c):
            c = c / 255.0
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        return 0.2126 * canal(r) + 0.7152 * canal(g) + 0.0722 * canal(b)
    a, b = lum(fg), lum(bg)
    lo, hi = min(a, b), max(a, b)
    return (hi + 0.05) / (lo + 0.05)


def avisar_contraste(resalte: str, fondo: str = FONDO) -> str | None:
    c = contraste(resalte, fondo)
    if c < 4.5:
        return (f"Contraste bajo de --resalte {resalte} sobre {fondo}: "
                f"{c:.1f}:1 (mínimo AA 4.5:1)")
    return None
