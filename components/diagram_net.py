"""Diagrama de nodos enlazados (flujo, topología, attack path defensivo)."""

import html as _html

MAX_NODOS = 5
TIPOS = {"alerta": "alerta", "error": "alerta", "peligro": "alerta",
         "ok": "ok", "bien": "ok", "defensa": "ok", "info": "info",
         "azul": "info", "datos": "info"}


def render(props, ctx, warnings=None):
    nodos = props.get("nodos") or props.get("nodes") or []
    titulo = props.get("titulo") or props.get("title") or ""
    if len(nodos) > MAX_NODOS:
        if warnings is not None:
            warnings.append(f"diagram: {len(nodos)} nodos > {MAX_NODOS}, se recortan")
        nodos = nodos[:MAX_NODOS]

    etiquetas_flecha = props.get("flechas") or []
    etiquetas_planas = props.get("etiquetas") or []
    bloques = []
    for i, n in enumerate(nodos):
        if isinstance(n, str):
            n = {"v": n}
        tipo = TIPOS.get(str(n.get("tipo") or "").lower(), "")
        sub = n.get("sub") or n.get("detalle") or ""
        cls = f" diagram__nodo--{tipo}" if tipo else ""
        sub_html = f'<div class="diagram__sub">{_html.escape(str(sub))}</div>' if sub else ""
        bloques.append(
            f'<div class="diagram__nodo{cls}">'
            f'<div class="diagram__v">{_html.escape(str(n.get("v") or n.get("label") or ""))}</div>'
            f"{sub_html}</div>"
        )
        if i < len(nodos) - 1:
            etiqueta = ""
            if i < len(etiquetas_flecha):
                f = etiquetas_flecha[i]
                etiqueta = str((f or {}).get("v") or (f or {}).get("label") or "")
            if not etiqueta and i < len(etiquetas_planas):
                etiqueta = str(etiquetas_planas[i])
            lbl = f'<span class="lbl">{_html.escape(etiqueta)}</span>' if etiqueta else ""
            bloques.append(f'<div class="diagram__flecha">↓ {lbl}</div>')

    titulo_html = (f'<div class="diagram__titulo">{_html.escape(str(titulo))}</div>'
                   if titulo else "")
    return f'<div class="diagram">{titulo_html}{"".join(bloques)}</div>'
