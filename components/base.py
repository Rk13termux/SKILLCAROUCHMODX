"""Base de componentes: extracción del slide fuente + dispatch + warnings.

Un componente se declara en el slide fuente así:

    <div class="componente" data-component="terminal" data-props='{...JSON...}'>
    </div>

Si falta `data-props`, el JSON se lee del interior del div. El atributo usa
comillas simples para que el JSON pueda llevar comillas dobles.
"""

import json
import re

# ── Extracción (div balanceado: el interior puede tener divs anidados) ──

def extraer_componente(body: str):
    """Devuelve (body_sin_componente, nombre, props) o (body, None, None)."""
    m = re.search(r'<div\s+class="componente"((?:[^>"\']|"[^"]*"|\'[^\']*\')*)>',
                  body)
    if not m:
        return body, None, None
    inicio = m.start()
    attrs = m.group(1)
    # Escanear el balance de <div> ... </div> desde la apertura
    pos = m.end()
    depth = 1
    for match in re.finditer(r"<div\b|</div>", body[pos:], re.I):
        tag = match.group(0).lower()
        depth += 1 if tag.startswith("<div") else -1
        if depth == 0:
            pos = pos + match.end()
            break
    else:
        return body, None, None  # sin cierre: lo dejamos tal cual

    interior = body[m.end():pos - len("</div>")]
    resto = (body[:inicio] + body[pos:]).strip()

    nombre = _attr(attrs, "data-component") or ""
    props_txt = _attr(attrs, "data-props")
    if props_txt is None:
        props_txt = interior.strip()
    props = {}
    if props_txt.strip():
        try:
            props = json.loads(props_txt)
        except json.JSONDecodeError as e:
            return (f'<div class="comp-error">⚠ JSON inválido en '
                    f'componente "{nombre}": {e}</div>' + resto, nombre, None)
    return resto, nombre.strip(), props


def _attr(attrs: str, nombre: str):
    m = re.search(rf'{nombre}=(["\'])(.*?)\1', attrs, re.S)
    return m.group(2) if m else None


# ── Dispatch ───────────────────────────────────────────────────────

def _terminal(p, ctx):
    from .terminal import render
    return render(p, ctx)


def _card_info(p, ctx):
    from .card_info import render_info
    return render_info(p, ctx)


def _mitos(p, ctx):
    from .card_info import render_mitos
    return render_mitos(p, ctx)


def _card_compare(p, ctx):
    from .card_compare import render
    return render(p, ctx)


def _card_repo(p, ctx):
    from .card_repo import render
    return render(p, ctx)


def _diagram(p, ctx):
    from .diagram_net import render
    return render(p, ctx)


def _pasos(p, ctx):
    from .graphic import render_pasos
    return render_pasos(p, ctx)


def _checklist(p, ctx):
    from .graphic import render_checklist
    return render_checklist(p, ctx)


def _code(p, ctx):
    from .code_block import render
    return render(p, ctx)


def _editor(p, ctx):
    from .code_block import render_editor
    return render_editor(p, ctx)


def _gh_stats(p, ctx):
    from .gh_stats import render
    return render(p, ctx)


def _diff(p, ctx):
    from .code_block import render_diff
    return render_diff(p, ctx)


def _tree(p, ctx):
    from .tree import render
    return render(p, ctx)


def _http(p, ctx):
    from .http_api import render
    return render(p, ctx)


def _browser(p, ctx):
    from .http_api import render_browser
    return render_browser(p, ctx)


def _stats(p, ctx):
    from .panels import render_stats
    return render_stats(p, ctx)


def _tabla(p, ctx):
    from .panels import render_tabla
    return render_tabla(p, ctx)


def _layers(p, ctx):
    from .panels import render_layers
    return render_layers(p, ctx)


def _pipeline(p, ctx):
    from .panels import render_pipeline
    return render_pipeline(p, ctx)


def _faq(p, ctx):
    from .graphic import render_faq
    return render_faq(p, ctx)


def _quote(p, ctx):
    from .graphic import render_quote
    return render_quote(p, ctx)


def _quiz(p, ctx):
    from .graphic import render_quiz
    return render_quiz(p, ctx)


def _qr(p, ctx):
    from .qr import render
    return render(p, ctx)


def _social(p, ctx):
    from .social_card import render
    return render(p, ctx)


def _stack(p, ctx):
    from .extra import render_stack
    return render_stack(p, ctx)


def _error(p, ctx):
    from .extra import render_error
    return render_error(p, ctx)


def _timeline(p, ctx):
    from .extra import render_timeline
    return render_timeline(p, ctx)


def _index(p, ctx):
    from .extra import render_index
    return render_index(p, ctx)


RENDERIZADORES = {
    "terminal": _terminal,
    "card-info": _card_info,
    "card-compare": _card_compare,
    "card-repo": _card_repo,
    "diagram": _diagram,
    "pasos": _pasos,
    "code": _code,
    "editor": _editor,
    "gh-stats": _gh_stats,
    "checklist": _checklist,
    "mitos": _mitos,
    "social": _social,
    "tree": _tree,
    "http": _http,
    "browser": _browser,
    "diff": _diff,
    "stats": _stats,
    "tabla": _tabla,
    "layers": _layers,
    "pipeline": _pipeline,
    "faq": _faq,
    "quote": _quote,
    "quiz": _quiz,
    "qr": _qr,
    "stack-tec": _stack,
    "error": _error,
    "timeline-fases": _timeline,
    "indice": _index,
}

ALIAS = {
    "cli": "terminal",
    "cmd": "terminal",
    "info": "card-info",
    "compare": "card-compare",
    "vs": "card-compare",
    "repo": "card-repo",
    "diagrama": "diagram",
    "flow": "diagram",
    "steps": "pasos",
    "timeline": "pasos",
    "codigo": "code",
    "snippet": "code",
    "editor-codigo": "editor",
    "ide": "editor",
    "vscode": "editor",
    "python": "editor",
    "py-editor": "editor",
    "github": "gh-stats",
    "repo-stats": "gh-stats",
    "estrellas": "gh-stats",
    "codigo-qr": "qr",
    "qrcode": "qr",
    "qr-code": "qr",
    "tecnologias": "stack-tec",
    "tech-stack": "stack-tec",
    "traza": "error",
    "traceback": "error",
    "fallo": "error",
    "roadmap": "timeline-fases",
    "ruta": "timeline-fases",
    "fases": "timeline-fases",
    "tabla-contenidos": "indice",
    "toc": "indice",
    "takeaways": "checklist",
    "myth": "mitos",
    "card": "social",
    "arbol": "tree",
    "filesystem": "tree",
    "git-tree": "tree",
    "ramas": "tree",
    "api": "http",
    "api-block": "http",
    "request": "http",
    "endpoint": "http",
    "web": "browser",
    "ventana": "browser",
    "antes-despues": "diff",
    "before-after": "diff",
    "metricas": "stats",
    "kpi": "stats",
    "numeros": "stats",
    "capas": "layers",
    "stack": "layers",
    "pila": "layers",
    "ci": "pipeline",
    "stages": "pipeline",
    "deploy-flow": "pipeline",
    "table": "tabla",
    "comparativa": "tabla",
    "preguntas": "faq",
    "cita": "quote",
    "frase": "quote",
    "test-rapido": "quiz",
    "pregunta": "quiz",
}


def renderizar(nombre, props, ctx=None, warnings=None):
    """Componente → HTML. Devuelve '' si el nombre es desconocido."""
    ctx = ctx or {}
    warnings = warnings if warnings is not None else []
    clave = (nombre or "").lower().strip()
    clave = ALIAS.get(clave, clave)
    fn = RENDERIZADORES.get(clave)
    if not fn:
        warnings.append(f"componente desconocido: {nombre}")
        return ""
    try:
        return fn(props or {}, ctx)
    except Exception as e:  # noqa: BLE001 - el slide no debe morir por esto
        warnings.append(f"componente '{nombre}' falló: {e}")
        return (f'<div class="comp-error">⚠ No se pudo renderizar '
                f'<b>{nombre}</b>: {e}</div>')


def expandir(body: str, ctx=None, warnings=None):
    """Expande TODOS los componentes de un body. Devuelve (html, usados)."""
    usados = []
    if warnings is None:
        warnings = []
    for _ in range(10):  # techo: 10 componentes por slide
        body, nombre, props = extraer_componente(body)
        if not nombre:
            break
        if props is None:
            warnings.append(f"componente '{nombre}': JSON inválido")
            usados.append(nombre)
            continue
        html = renderizar(nombre, props, ctx, warnings)
        usados.append(nombre)
        body = f"{body}\n<div class=\"comp-wrap\">{html}</div>"
    return body, usados


def html_valido(nombre: str) -> bool:
    clave = ALIAS.get((nombre or "").lower().strip(), (nombre or "").lower().strip())
    return clave in RENDERIZADORES
