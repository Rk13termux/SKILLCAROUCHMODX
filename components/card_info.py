"""Cards informativas y mitos vs realidad."""

import html as _html

try:
    from ..theme.colors import VARIANTES, acento_vars
except ImportError:  # import como paquete top-level (builder)
    from theme.colors import VARIANTES, acento_vars

MAX_CUERPO = 260  # ~3 líneas en 9:16

# Variante → glyph del registry (icono SVG de la casa, no un carácter).
GLYPH_VARIANTE = {
    "info": "info",
    "tip": "lightbulb",
    "warn": "triangle-alert",
    "danger": "shield-alert",
}


def _icono_svg(nombre, accent):
    """Glyph del registry → <img> data-URI, o '' si no hay icono."""
    if not nombre or not accent:
        return ""
    try:
        from ..icons import get_icon
    except ImportError:
        try:
            from icons import get_icon
        except ImportError:
            return ""
    try:
        uri = get_icon(nombre, acento_vars(accent))
    except Exception:  # noqa: BLE001 - el icono nunca debe romper el slide
        return ""
    if not uri:
        return ""
    return f'<img src="{uri}" alt="">'


def render_info(props, ctx, warnings=None):
    variante = str(props.get("variante") or props.get("variant") or "info").lower()
    borde, ico = VARIANTES.get(variante, VARIANTES["info"])
    titulo = _html.escape(str(props.get("titulo") or props.get("title") or ""))
    cuerpo = _html.escape(str(props.get("cuerpo") or props.get("body") or ""))
    if len(cuerpo) > MAX_CUERPO:
        cuerpo = cuerpo[:MAX_CUERPO].rsplit(" ", 1)[0] + "…"
        if warnings is not None:
            warnings.append("card-info: cuerpo recortado (>260 caracteres)")
    # Icono SVG semántico: prop `icono` > variante > carácter de respaldo.
    glyph = props.get("icono") or props.get("icon") or GLYPH_VARIANTE.get(variante)
    icono_html = _icono_svg(str(glyph), ctx.get("accent")) or _html.escape(ico)
    return (
        f'<div class="card-info" style="--card-borde:{borde}">'
        '<div class="card-info__head">'
        f'<div class="card-info__ico">{icono_html}</div>'
        f'<div class="card-info__titulo">{titulo}</div>'
        "</div>"
        f'<div class="card-info__cuerpo">{cuerpo}</div>'
        "</div>"
    )


def render_mitos(props, ctx, warnings=None):
    mito = _html.escape(str(props.get("mito") or ""))
    realidad = _html.escape(str(props.get("realidad") or ""))
    sub_m = props.get("mito_sub") or props.get("sub_mito") or ""
    sub_r = props.get("realidad_sub") or props.get("sub_realidad") or ""
    bloque_m = f'<div class="mitos__sub">{_html.escape(str(sub_m))}</div>' if sub_m else ""
    bloque_r = f'<div class="mitos__sub">{_html.escape(str(sub_r))}</div>' if sub_r else ""
    return (
        '<div class="mitos">'
        '<div class="mitos__bloque mitos__bloque--mito">'
        '<div class="mitos__label">MITO</div>'
        f'<div class="mitos__texto">{mito}</div>{bloque_m}'
        "</div>"
        '<div class="mitos__bloque mitos__bloque--real">'
        '<div class="mitos__label">REALIDAD</div>'
        f'<div class="mitos__texto">{realidad}</div>{bloque_r}'
        "</div>"
        "</div>"
    )
