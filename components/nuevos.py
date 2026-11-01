"""Componentes Wave 4: piezas de alto impacto para retención.

- `dato-hero`  : una cifra gigante + contexto. El freno de scroll más directo.
- `split`      : comparación visual en dos paneles con VS central.
- `progreso`   : barra de avance con hitos (madurez, plan, checklist de nivel).
- `fix`        : el error a la izquierda, la solución a la derecha.
"""

import html as _html

MAX_SUB = 190
MAX_HITOS = 5
MAX_FIX_LINEAS = 6


def _txt(valor):
    return _html.escape(str(valor if valor is not None else ""))


# ── dato-hero ─────────────────────────────────────────────────────

def render_dato_hero(props, ctx, warnings=None):
    valor = props.get("valor") or props.get("v") or props.get("cifra") or "—"
    etiqueta = props.get("etiqueta") or props.get("label") or ""
    sub = str(props.get("sub") or props.get("cuerpo") or "")
    fuente = props.get("fuente") or props.get("source") or ""
    eyebrow = props.get("eyebrow") or props.get("kicker") or ""
    if len(sub) > MAX_SUB:
        sub = sub[:MAX_SUB].rsplit(" ", 1)[0] + "…"
        if warnings is not None:
            warnings.append("dato-hero: `sub` recortado (>190 caracteres)")

    partes = ['<div class="hero-dato">']
    if eyebrow:
        partes.append(f'<div class="hero-dato__eyebrow">{_txt(eyebrow)}</div>')
    partes.append(f'<div class="hero-dato__val">{_txt(valor)}</div>')
    if etiqueta:
        partes.append(f'<div class="hero-dato__lbl">{_txt(etiqueta)}</div>')
    if sub:
        partes.append(f'<div class="hero-dato__sub">{_txt(sub)}</div>')
    if fuente:
        partes.append(f'<div class="hero-dato__src">{_txt(fuente)}</div>')
    partes.append("</div>")
    return "".join(partes)


# ── split ─────────────────────────────────────────────────────────

def _lado(datos, lado):
    if isinstance(datos, str):
        datos = {"titulo": datos}
    tag = datos.get("etiqueta") or datos.get("tag") or ""
    tit = datos.get("titulo") or datos.get("title") or ""
    cuerpo = datos.get("cuerpo") or datos.get("body") or ""
    items = datos.get("items") or []
    html = [f'<div class="split__lado split__lado--{lado}">']
    if tag:
        html.append(f'<div class="split__tag">{_txt(tag)}</div>')
    if tit:
        html.append(f'<div class="split__t">{_txt(tit)}</div>')
    if cuerpo:
        html.append(f'<div class="split__c">{_txt(cuerpo)}</div>')
    if items:
        filas = "".join(
            f'<div class="split__item"><span class="split__dot"></span>'
            f'<span>{_txt(i.get("v") if isinstance(i, dict) else i)}</span></div>'
            for i in items[:4])
        html.append(f'<div class="split__items">{filas}</div>')
    html.append("</div>")
    return "".join(html)


def render_split(props, ctx, warnings=None):
    titulo = props.get("titulo") or props.get("title") or ""
    izq = props.get("izq") or props.get("left") or {}
    der = props.get("der") or props.get("right") or {"v": ""}
    vs = props.get("vs") or "VS"
    t = (f'<div class="split__titulo">{_txt(titulo)}</div>' if titulo else "")
    return (
        '<div class="split">'
        f"{t}"
        '<div class="split__grid">'
        f"{_lado(izq, 'a')}"
        f'<div class="split__vs">{_txt(vs)}</div>'
        f"{_lado(der, 'b')}"
        "</div></div>"
    )


# ── progreso ──────────────────────────────────────────────────────

_ESTADOS = {"ok": "ok", "hecho": "ok", "done": "ok",
            "run": "run", "curso": "run", "activo": "run",
            "error": "error", "falta": "error", "pendiente": "idle"}


def render_progreso(props, ctx, warnings=None):
    titulo = props.get("titulo") or props.get("title") or ""
    etiqueta = props.get("etiqueta") or props.get("label") or ""
    try:
        valor = int(round(float(props.get("valor") or props.get("value") or 0)))
    except (TypeError, ValueError):
        valor = 0
    valor = max(0, min(100, valor))

    hitos = props.get("hitos") or props.get("milestones") or []
    if isinstance(hitos, str):
        hitos = [hitos]
    if len(hitos) > MAX_HITOS:
        hitos = hitos[:MAX_HITOS]
        if warnings is not None:
            warnings.append("progreso: máx 5 hitos, se recortaron")
    filas = []
    for h in hitos:
        if isinstance(h, str):
            h = {"v": h}
        estado = _ESTADOS.get(str(h.get("estado") or "").lower(), "idle")
        filas.append(
            f'<div class="prog__hito prog__hito--{estado}">'
            f'<span class="prog__dot"></span>'
            f'<span>{_txt(h.get("v") or h.get("titulo") or "")}</span></div>')

    t = (f'<div class="prog__titulo">{_txt(titulo)}</div>' if titulo else "")
    e = (f'<div class="prog__etiqueta">{_txt(etiqueta)}</div>' if etiqueta else "")
    hitos_html = (f'<div class="prog__hitos">{"".join(filas)}</div>'
                  if filas else "")
    return (
        '<div class="prog">'
        f"{t}"
        '<div class="prog__head">'
        f'<div class="prog__track"><div class="prog__fill" '
        f'style="width:{valor}%"></div></div>'
        f'<div class="prog__pct">{valor}%</div>'
        "</div>"
        f"{e}{hitos_html}"
        "</div>"
    )


# ── fix (error → solución) ────────────────────────────────────────

def _panel(texto, lenguaje, clase):
    from .code_block import resaltar
    lineas = str(texto or "").splitlines()
    if len(lineas) > MAX_FIX_LINEAS:
        lineas = lineas[:MAX_FIX_LINEAS] + ["…"]
    filas = "".join(
        f'<div class="fix__line">{resaltar(ln, lenguaje)}</div>' for ln in lineas)
    return f'<div class="fix__panel fix__panel--{clase}">{filas}</div>'


def render_fix(props, ctx, warnings=None):
    titulo = props.get("titulo") or props.get("title") or ""
    lenguaje = str(props.get("lenguaje") or props.get("lang") or "python").lower()
    malo = props.get("error") or props.get("antes") or props.get("roto") or ""
    bueno = props.get("solucion") or props.get("despues") or props.get("fix") or ""
    nota = props.get("nota") or props.get("pie") or ""
    t = (f'<div class="fix__titulo">{_txt(titulo)}</div>' if titulo else "")
    n = (f'<div class="fix__nota">{_txt(nota)}</div>' if nota else "")
    return (
        '<div class="fix">'
        f"{t}"
        '<div class="fix__row">'
        '<div class="fix__col">'
        '<div class="fix__lbl fix__lbl--malo">✕ ROTO</div>'
        f"{_panel(malo, lenguaje, 'malo')}</div>"
        '<div class="fix__arrow">→</div>'
        '<div class="fix__col">'
        '<div class="fix__lbl fix__lbl--bueno">✓ FIX</div>'
        f"{_panel(bueno, lenguaje, 'bueno')}</div>"
        "</div>"
        f"{n}</div>"
    )
