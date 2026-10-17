"""Componentes web: bloque de API (request/response) + ventana de navegador."""

import html as _html

MAX_LINEAS = 8


def _bloque(texto):
    lineas = str(texto or "").splitlines()
    if len(lineas) > MAX_LINEAS:
        lineas = lineas[:MAX_LINEAS] + ["…"]
    return _html.escape("\n".join(lineas))


def render(props, ctx, warnings=None):
    """api-block: método + URL + estado + cuerpo de request/response."""
    metodo = (props.get("metodo") or props.get("method") or "GET").upper()
    ruta = props.get("ruta") or props.get("url") or "/"
    codigo = props.get("codigo") or props.get("status")
    nota = props.get("nota") or props.get("nota_estado") or ""
    req = props.get("request") or props.get("req")
    res = props.get("response") or props.get("res") or props.get("cuerpo")
    cls_met = {"POST": "api-block__metodo--post",
               "PUT": "api-block__metodo--put", "PATCH": "api-block__metodo--put",
               "DELETE": "api-block__metodo--del", "DEL": "api-block__metodo--del"}.get(metodo, "")
    estado = ""
    if codigo:
        estado = (f'<span class="api-block__status">{_html.escape(str(codigo))}'
                  f'{(" · " + _html.escape(str(nota))) if nota else ""}</span>')
    cuerpos = ""
    if req:
        cuerpos += (f'<div class="api-block__body"><b>→ request</b>\n{_bloque(req)}</div>')
    if res:
        cuerpos += (f'<div class="api-block__body"><b>← response</b>\n{_bloque(res)}</div>')
    return (
        '<div class="api-block">'
        '<div class="api-block__head">'
        f'<span class="api-block__metodo {cls_met}">{_html.escape(metodo)}</span>'
        f'<span class="api-block__url">{_html.escape(str(ruta))}</span>'
        f'{estado}</div>{cuerpos}</div>'
    )


def render_browser(props, ctx, warnings=None):
    """browser: mock de ventana con URL + contenido visible."""
    url = props.get("url") or props.get("ruta") or "https://ejemplo.local"
    vista = props.get("vista") or props.get("contenido") or props.get("body") or ""
    titulo = props.get("titulo") or props.get("title") or ""
    head = (
        '<div class="browser__bar">'
        '<span class="browser__dot browser__dot--r"></span>'
        '<span class="browser__dot browser__dot--y"></span>'
        '<span class="browser__dot browser__dot--g"></span>'
        f'<span class="browser__url">{_html.escape(str(url))}</span></div>'
    )
    t = (f'<div class="browser__view"><b>{_html.escape(str(titulo))}</b>\n'
         if titulo else '<div class="browser__view">')
    return f'<div class="browser">{head}{t}{_bloque(vista)}</div>'
