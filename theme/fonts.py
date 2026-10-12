"""Tipografías del sistema TechEdu.

Display: Inter (títulos, cuerpo). Mono: Hasklig primero (lo pedido: "tipo
Hask"), con JetBrains Mono como webfont real (Hasklig no está en Google
Fonts) y stack del sistema al final: así el render funciona también offline.
"""

# Google Fonts: Inter + JetBrains Mono. Si no hay red, el fallback del
# font-family cubre y el slide sale igual de legible.
GOOGLE_FONTS = (
    "https://fonts.googleapis.com/css2?"
    "family=Inter:wght@400;500;600;700;800&display=swap"
)

GOOGLE_FONTS_MONO = (
    "https://fonts.googleapis.com/css2?"
    "family=JetBrains+Mono:wght@400;500;700&display=swap"
)

DISPLAY = "'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif"

# Hask → Hasklig (instalada localmente si el usuario la tiene) → JetBrains
# Mono → stack de sistema. Orden: lo más parecido a Hask primero, lo
# siempre-disponible al final.
MONO = (
    "'Hasklig', 'JetBrains Mono', 'SF Mono', 'SFMono-Regular', "
    "'Menlo', 'Consolas', 'DejaVu Sans Mono', monospace"
)


def links() -> str:
    """Etiquetas <link> de preconnect + fuentes (con fallback de red).

    En modo offline (o si no hay red) devuelve cadena vacía: los fallbacks
    de `DISPLAY`/`MONO` ya cubren, así el render no espera a Google Fonts.
    """
    if _OFFLINE:
        return ""
    return (
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        f'<link href="{GOOGLE_FONTS}" rel="stylesheet">\n'
        f'<link href="{GOOGLE_FONTS_MONO}" rel="stylesheet">'
    )


def body_css() -> str:
    """Reglas base de tipografía aplicadas a body y bloques técnicos."""
    return f"""
  body {{ font-family: {DISPLAY}; }}
  .terminal, .code, .repo-card__tree, .repo-card__install, .chip {{
    font-family: {MONO};
  }}
"""


# ── Modo offline ───────────────────────────────────────────────────
# Con red, el builder enlaza Google Fonts y el render usa Inter/JetBrains.
# Sin red (o con --offline) no se emite ningún <link> externo: el slide se
# compone directo con los fallbacks del sistema, así no hay espera de red
# ni saltos de layout entre intentos.

_OFFLINE = False


def set_offline(valor: bool) -> None:
    global _OFFLINE
    _OFFLINE = bool(valor)


def offline() -> bool:
    return _OFFLINE
