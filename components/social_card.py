"""Social / value card (portadas y cierres de valor)."""

import html as _html


def render(props, ctx, warnings=None):
    kicker = str(props.get("kicker") or props.get("badge") or "")
    titulo = _html.escape(str(props.get("titulo") or props.get("title") or ""))
    texto = _html.escape(str(props.get("texto") or props.get("body") or ""))
    cta = _html.escape(str(props.get("cta") or ""))
    kicker_html = f'<div class="social__kicker">{_html.escape(kicker)}</div>' if kicker else ""
    cta_html = f'<div class="social__cta">{cta}</div>' if cta else ""
    texto_html = f'<div class="social__texto">{texto}</div>' if texto else ""
    return (
        '<div class="social">'
        f"{kicker_html}"
        f'<div class="social__titulo">{titulo}</div>'
        f"{texto_html}{cta_html}"
        "</div>"
    )
