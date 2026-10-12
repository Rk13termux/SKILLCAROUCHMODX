"""Card comparativa: 2 columnas (A vs B, pros/contras, antes/después)."""

import html as _html

MAX_ITEMS = 4


def _item(it):
    if isinstance(it, str):
        it = {"v": it}
    texto = _html.escape(str(it.get("v") or it.get("texto") or ""))
    if "ok" in it:
        marca, cls = ("✓", "ok") if it["ok"] else ("✕", "no")
    elif it.get("tipo") in ("mid", "warn", "neutral"):
        marca, cls = ("~", "mid")
    else:
        marca, cls = ("·", "mid")
    if it.get("marca"):
        marca = _html.escape(str(it["marca"]))
    return (f'<div class="card-compare__item">'
            f'<span class="card-compare__mark card-compare__mark--{cls}">{marca}</span>'
            f"<span>{texto}</span></div>")


def render(props, ctx, warnings=None):
    cols = props.get("cols") or props.get("columnas") or []
    if len(cols) > 2:
        if warnings is not None:
            warnings.append("card-compare: máx 2 columnas, se recortan")
        cols = cols[:2]
    titulo = props.get("titulo") or props.get("title") or ""
    celdas = []
    for i, col in enumerate(cols[:2]):
        if isinstance(col, str):
            col = {"nombre": col, "items": []}
        items = col.get("items") or []
        if len(items) > MAX_ITEMS:
            items = items[:MAX_ITEMS]
            if warnings is not None:
                warnings.append(f"card-compare: columna {i+1} recortada a {MAX_ITEMS} items")
        lado = "a" if i == 0 else "b"
        badge = col.get("badge") or ("VS" if i == 0 and len(cols) > 1 else "")
        nombre = _html.escape(str(col.get("nombre") or col.get("name") or f"Opción {i+1}"))
        html_badge = f'<div class="card-compare__badge">{_html.escape(str(badge))}</div>' if badge else ""
        celdas.append(
            f'<div class="card-compare__col card-compare__col--{lado}">'
            f"{html_badge}"
            f'<div class="card-compare__nombre">{nombre}</div>'
            f'{"".join(_item(x) for x in items)}</div>'
        )
    titulo_html = (f'<div class="card-compare__titulo">{_html.escape(str(titulo))}</div>'
                   if titulo else "")
    return (
        f'<div class="card-compare" style="--cols:{max(1, len(celdas))}">'
        f"{titulo_html}"
        f'<div class="card-compare__grid">{"".join(celdas)}</div></div>'
    )
