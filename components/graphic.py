"""Infografía de pasos + checklist de takeaways."""

import html as _html

MAX_PASOS = 4
MAX_ITEMS = 4


def render_pasos(props, ctx, warnings=None):
    pasos = props.get("pasos") or props.get("steps") or []
    titulo = props.get("titulo") or props.get("title") or ""
    if len(pasos) > MAX_PASOS:
        if warnings is not None:
            warnings.append(f"pasos: {len(pasos)} > {MAX_PASOS}, se recortan")
        pasos = pasos[:MAX_PASOS]
    filas = []
    for i, p in enumerate(pasos, 1):
        if isinstance(p, str):
            p = {"t": p}
        t = _html.escape(str(p.get("t") or p.get("titulo") or ""))
        d = _html.escape(str(p.get("d") or p.get("desc") or ""))
        n = p.get("n", i)
        desc = f'<div class="paso__d">{d}</div>' if d else ""
        filas.append(
            f'<div class="paso"><div class="paso__n">{_html.escape(str(n))}</div>'
            f'<div><div class="paso__t">{t}</div>{desc}</div></div>'
        )
    titulo_html = (f'<div class="pasos__titulo">{_html.escape(str(titulo))}</div>'
                   if titulo else "")
    return f'<div class="pasos">{titulo_html}{"".join(filas)}</div>'


def render_checklist(props, ctx, warnings=None):
    items = props.get("items") or props.get("lista") or []
    titulo = props.get("titulo") or props.get("title") or "Takeaways"
    if len(items) > MAX_ITEMS:
        if warnings is not None:
            warnings.append(f"checklist: {len(items)} > {MAX_ITEMS}, se recortan")
        items = items[:MAX_ITEMS]
    filas = []
    for it in items:
        if isinstance(it, str):
            it = {"v": it}
        texto = _html.escape(str(it.get("v") or it.get("texto") or ""))
        filas.append(f'<div class="checklist__item">'
                     f'<span class="checklist__ico">✓</span><span>{texto}</span></div>')
    return (f'<div class="checklist">'
            f'<div class="checklist__titulo">{_html.escape(str(titulo))}</div>'
            f'{"".join(filas)}</div>')


def render_faq(props, ctx, warnings=None):
    items = props.get("items") or []
    pregunta = props.get("pregunta") or props.get("q")
    respuesta = props.get("respuesta") or props.get("a")
    if pregunta and respuesta and not items:
        items = [{"q": pregunta, "a": respuesta}]
    titulo = props.get("titulo") or props.get("title") or ""
    bloques = []
    for it in items[:3]:
        if isinstance(it, str):
            it = {"q": it}
        q = _html.escape(str(it.get("q") or it.get("pregunta") or ""))
        a = _html.escape(str(it.get("a") or it.get("respuesta") or ""))
        bloques.append(f'<div class="faq__item"><div class="faq__q">'
                       f'<span class="faq__badge">?</span>{q}</div>'
                       f'<div class="faq__a">{a}</div></div>')
    t = (f'<div class="faq__titulo">{_html.escape(str(titulo))}</div>' if titulo else "")
    return f'<div class="faq">{t}{"".join(bloques)}</div>'


def render_quote(props, ctx, warnings=None):
    texto = props.get("texto") or props.get("cita") or ""
    autor = props.get("autor") or props.get("author") or "CHMODX"
    rol = props.get("rol") or props.get("rol_autor") or ""
    rol_html = f'<div class="quote__rol">{_html.escape(str(rol))}</div>' if rol else ""
    return (
        '<div class="quote">'
        f'<div class="quote__text">“{_html.escape(str(texto))}”</div>'
        f'<div class="quote__autor">— {_html.escape(str(autor))}</div>{rol_html}</div>'
    )


def render_quiz(props, ctx, warnings=None):
    pregunta = props.get("pregunta") or props.get("q") or ""
    opciones = props.get("opciones") or props.get("options") or []
    pie = props.get("pie") or "La respuesta está en el siguiente slide →"
    filas = []
    for i, op in enumerate(opciones[:4]):
        if isinstance(op, str):
            op = {"v": op}
        v = _html.escape(str(op.get("v") or ""))
        ok = bool(op.get("ok") or op.get("correcta"))
        cls = "quiz__op--ok" if ok else ""
        marca = "✓" if ok else chr(65 + i)
        filas.append(f'<div class="quiz__op {cls}"><span class="quiz__mk">{marca}</span>'
                     f'<span>{v}</span></div>')
    return (
        '<div class="quiz">'
        f'<div class="quiz__q"><span class="quiz__badge">?</span>{_html.escape(str(pregunta))}</div>'
        f'{"".join(filas)}'
        f'<div class="quiz__pie">{_html.escape(str(pie))}</div></div>'
    )
