"""Helpers de trazo para los glyphs SVG.

Regla crítica (heredada de la versión anterior): UN SOLO stroke-width por
elemento. XML con atributos duplicados da naturalWidth=0 en Chromium y el
ícono sale invisible.

Sin filtros SVG (feGaussianBlur etc.): se rasterizan en cualquier headless.
El halo lo aporta el drop-shadow CSS del template.
"""

GRADIENT = (
    '<linearGradient id="c" x1="0" y1="0" x2="0.9" y2="1">'
    '<stop offset="0" stop-color="rgb({br})"/>'
    '<stop offset="0.55" stop-color="rgb({rgb})"/>'
    '<stop offset="1" stop-color="rgb({dim})"/>'
    "</linearGradient>"
)


def P(d, w=1.5):
    """Path de línea."""
    return (f'<path d="{d}" fill="none" stroke="url(#c)" stroke-width="{w}" '
            'stroke-linecap="round" stroke-linejoin="round"/>')


def C(cx, cy, r, w=1.5):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="url(#c)" '
            f'stroke-width="{w}"/>')


def L(x1, y1, x2, y2, w=1.5):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="url(#c)" '
            f'stroke-width="{w}" stroke-linecap="round"/>')


def R(x, y, ancho, alto, w=1.5, rx=2):
    return (f'<rect x="{x}" y="{y}" width="{ancho}" height="{alto}" rx="{rx}" '
            f'fill="none" stroke="url(#c)" stroke-width="{w}"/>')


def A(d, w=1.5):
    """Arco/pathe de curva (misma semántica que P)."""
    return P(d, w)


def glyph_svg(cuerpo, accent_rgb, bright_rgb):
    """Envuelve el cuerpo de un glyph en un SVG completo 24x24."""
    r, g, b = accent_rgb
    br = bright_rgb
    dim = (int(r * 0.82), int(g * 0.82), int(b * 0.82))
    grad = GRADIENT.format(rgb=f"{r},{g},{b}", br=f"{br[0]},{br[1]},{br[2]}",
                           dim=f"{dim[0]},{dim[1]},{dim[2]}")
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" '
        f'width="100%" height="100%"><defs>{grad}</defs>{cuerpo}</svg>'
    )


def data_uri(svg: str) -> str:
    import base64
    return "data:image/svg+xml;base64," + base64.b64encode(
        svg.encode("utf-8")).decode("ascii")
