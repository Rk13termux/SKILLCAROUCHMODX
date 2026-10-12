"""Cards informativas y mitos vs realidad."""

import html as _html

try:
    from ..theme.colors import VARIANTES
except ImportError:  # import como paquete top-level (builder)
    from theme.colors import VARIANTES

MAX_CUERPO = 260  # ~3 líneas en 9:16


def render_info(props, ctx, warnings=None):
    variante = str(props.get("variante") or props.get("variant") or "info").lower()
    borde, ico = VARIANTES.get(variante, VARIANTES["info"])
    titulo = _html.escape(str(props.get("titulo") or props.get("title") or ""))
    cuerpo = _html.escape(str(props.get("cuerpo") or props.get("body") or ""))
    if len(cuerpo) > MAX_CUERPO:
        cuerpo = cuerpo[:MAX_CUERPO].rsplit(" ", 1)[0] + "…"
        if warnings is not None:
            warnings.append("card-info: cuerpo recortado (>260 caracteres)")
    return (
        f'<div class="card-info" style="--card-borde:{borde}">'
        '<div class="card-info__head">'
        f'<div class="card-info__ico">{ico}</div>'
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
