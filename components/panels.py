"""Paneles estructurados: stats, tabla, layers, pipeline.

Reutilizan el CSS ya centralizado en theme/tokens.py (.stats, .ctable,
.layers, .pipeline). Todos recortan con warning en vez de romper el slide.
"""

import html as _html

MAX_STATS = 4
MAX_FILAS = 4
MAX_CAPAS = 5
MAX_ETAPAS = 5

_ESTADO_STAGE = {"ok": "stage--ok", "warn": "stage--warn", "warning": "stage--warn",
                 "err": "stage--err", "error": "stage--err", "fail": "stage--err",
                 "idle": "stage--idle", "wait": "stage--idle", "run": "stage--warn"}
_TIPO_LAYER = {"front": "layer--front", "back": "layer--back", "db": "layer--db",
               "api": "layer--api"}


def render_stats(props, ctx, warnings=None):
    items = props.get("items") or props.get("stats") or []
    titulo = props.get("titulo") or props.get("title") or ""
    if len(items) > MAX_STATS:
        if warnings is not None:
            warnings.append(f"stats: {len(items)} > {MAX_STATS}, se recortan")
        items = items[:MAX_STATS]
    tarjetas = []
    for it in items:
        if isinstance(it, str):
            it = {"valor": it}
        v = _html.escape(str(it.get("valor") or it.get("v") or "—"))
        e = _html.escape(str(it.get("etiqueta") or it.get("label") or ""))
        lbl = f'<div class="stat__lbl">{e}</div>' if e else ""
        tarjetas.append(f'<div class="stat"><div class="stat__val">{v}</div>{lbl}</div>')
    t = (f'<div class="stats__titulo">{_html.escape(str(titulo))}</div>' if titulo else "")
    return f'<div class="stats">{t}<div class="stats__grid">{"".join(tarjetas)}</div></div>'


def render_tabla(props, ctx, warnings=None):
    headers = props.get("headers") or props.get("columnas") or []
    filas = props.get("filas") or props.get("rows") or []
    titulo = props.get("titulo") or props.get("title") or ""
    if len(filas) > MAX_FILAS:
        if warnings is not None:
            warnings.append(f"tabla: {len(filas)} filas > {MAX_FILAS}, se recortan")
        filas = filas[:MAX_FILAS]
    thead = ""
    if headers:
        thead = ("<tr>" + "".join(f"<th>{_html.escape(str(h))}</th>" for h in headers)
                 + "</tr>")
    trs = []
    for f in filas:
        if isinstance(f, str):
            f = [f]
        trs.append("<tr>" + "".join(f"<td>{_html.escape(str(c))}</td>" for c in f) + "</tr>")
    t = (f'<div class="ctable__titulo">{_html.escape(str(titulo))}</div>' if titulo else "")
    return (f'<div class="ctable">{t}<table class="ctable__tbl">{thead}'
            f'{"".join(trs)}</table></div>')


def render_layers(props, ctx, warnings=None):
    capas = props.get("capas") or props.get("layers") or []
    titulo = props.get("titulo") or props.get("title") or ""
    if len(capas) > MAX_CAPAS:
        if warnings is not None:
            warnings.append(f"layers: {len(capas)} > {MAX_CAPAS}, se recortan")
        capas = capas[:MAX_CAPAS]
    bloques = []
    for i, c in enumerate(capas):
        if isinstance(c, str):
            c = {"v": c}
        v = _html.escape(str(c.get("v") or c.get("nombre") or ""))
        s = _html.escape(str(c.get("sub") or c.get("s") or ""))
        tipo = _TIPO_LAYER.get((c.get("tipo") or "").lower(), "")
        sub = f'<div class="layer__s">{s}</div>' if s else ""
        bloques.append(f'<div class="layer {tipo}"><div class="layer__n">{v}</div>{sub}</div>')
        if i < len(capas) - 1:
            bloques.append('<div class="layers__arr">▲</div>')
    t = (f'<div class="layers__titulo">{_html.escape(str(titulo))}</div>' if titulo else "")
    return f'<div class="layers">{t}{"".join(bloques)}</div>'


def render_pipeline(props, ctx, warnings=None):
    etapas = props.get("etapas") or props.get("stages") or []
    titulo = props.get("titulo") or props.get("title") or ""
    if len(etapas) > MAX_ETAPAS:
        if warnings is not None:
            warnings.append(f"pipeline: {len(etapas)} > {MAX_ETAPAS}, se recortan")
        etapas = etapas[:MAX_ETAPAS]
    tarjetas = []
    for e in etapas:
        if isinstance(e, str):
            e = {"v": e}
        v = _html.escape(str(e.get("v") or e.get("nombre") or ""))
        st = _html.escape(str(e.get("estado") or e.get("st") or "ok"))
        cls = _ESTADO_STAGE.get(st.lower(), "stage--ok")
        tarjetas.append(f'<div class="stage {cls}"><div class="stage__n">{v}</div>'
                        f'<div class="stage__st">{st}</div></div>')
    t = (f'<div class="pipeline__titulo">{_html.escape(str(titulo))}</div>' if titulo else "")
    return f'<div class="pipeline">{t}<div class="pipeline__row">{"".join(tarjetas)}</div></div>'
