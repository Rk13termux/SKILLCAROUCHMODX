"""Componente tree: árbol de archivos o ramas git.

Iconos SVG inline profesionales por tipo (sin emojis: Chromium headless no
trae fuente emoji y salen tofu). Modo fs (default): nodos
[{v, depth, tipo}] o texto preformateado en `tree`. Modo git: ramas=[...]
con sufijo * en la actual.
"""

import html as _html

MAX_LINEAS = 10
GUIAS = ("├── ", "└── ", "│    ", "     ")

_SVG_OPEN = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
             'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">')

# (color, paths SVG estilo feather)
ICONOS = {
    "dir": ("#EAB308",
            '<path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>'),
    "code": ("#10B981",
             '<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>'),
    "config": ("#60A5FA",
               '<line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/>'
               '<line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/>'
               '<line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/>'
               '<line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/>'
               '<line x1="17" y1="16" x2="23" y2="16"/>'),
    "doc": ("#9CA3AF",
            '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>'
            '<polyline points="14 2 14 8 20 8"/>'
            '<line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>'),
    "db": ("#34D399",
           '<ellipse cx="12" cy="5" rx="9" ry="3"/>'
           '<path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>'
           '<path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>'),
    "file": ("#9CA3AF",
             '<path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/>'
             '<polyline points="13 2 13 9 20 9"/>'),
    "git": ("#F07178",
            '<line x1="6" y1="3" x2="6" y2="15"/><circle cx="18" cy="6" r="3"/>'
            '<circle cx="6" cy="18" r="3"/><path d="M18 9a9 9 0 0 1-9 9"/>'),
}

_EXT_TIPO = {}
for _ext in (".py", ".js", ".ts", ".tsx", ".jsx", ".mjs", ".sh", ".bash",
             ".go", ".rs", ".java", ".rb", ".php", ".c", ".h", ".cpp",
             ".sql", ".html", ".css", ".vue", ".dart", ".kt", ".swift"):
    _EXT_TIPO[_ext] = "code"
for _ext in (".yaml", ".yml", ".json", ".toml", ".ini", ".cfg", ".conf",
             ".env", ".xml"):
    _EXT_TIPO[_ext] = "config"
for _ext in (".md", ".markdown", ".txt", ".rst", ".log"):
    _EXT_TIPO[_ext] = "doc"
for _ext in (".db", ".sqlite", ".sqlite3"):
    _EXT_TIPO[_ext] = "db"

_NOMBRES_TIPO = {"dockerfile": "code", "makefile": "code", "license": "doc",
                 "readme.md": "doc", ".gitignore": "config", ".env": "config"}


def _tipo_archivo(nombre):
    base = str(nombre).strip().rstrip("/").lower()
    if base in _NOMBRES_TIPO:
        return _NOMBRES_TIPO[base]
    if "." in base:
        return _EXT_TIPO.get("." + base.rsplit(".", 1)[1], "file")
    return "file"


def _icono(tipo):
    color, paths = ICONOS.get(tipo, ICONOS["file"])
    return (f'<span class="tree-dir__ico" style="color:{color}">'
            f'{_SVG_OPEN}{paths}</svg></span>')


def _es_guiada(v):
    return v.startswith(GUIAS)


def _nodos_desde_texto(texto):
    nodos = []
    for ln in str(texto).splitlines():
        s = ln.strip()
        if not s or s in (".",):
            continue
        depth = 0
        resto = ln.replace("\t", "    ")
        while resto.startswith("│   ") or resto.startswith("    "):
            depth += 1
            resto = resto[4:]
        for g in ("├── ", "└── "):
            if resto.startswith(g):
                resto = resto[len(g):]
                break
        nodos.append({"v": resto.strip(), "depth": depth})
    return nodos


def _li(v, depth, tipo):
    vv = _html.escape(str(v))
    if tipo == "dir" and not vv.endswith("/"):
        vv += "/"
    sangria = (f'<span style="display:inline-block;width:{depth * 18}px"></span>'
               if depth else "")
    return (f'<li class="tree-dir__li">{sangria}{_icono(tipo)}'
            f'<span>{vv}</span></li>')


def render(props, ctx, warnings=None):
    titulo = props.get("titulo") or props.get("title") or ""
    modo = (props.get("modo") or props.get("mode") or "fs").lower()
    if modo == "git":
        ramas = props.get("ramas") or props.get("branches") or []
        if isinstance(ramas, str):
            ramas = [r.strip() for r in ramas.splitlines() if r.strip()]
        if len(ramas) > MAX_LINEAS:
            if warnings is not None:
                warnings.append(f"tree: {len(ramas)} ramas > {MAX_LINEAS}, se recortan")
            ramas = ramas[:MAX_LINEAS]
        filas = []
        for r in ramas:
            r = str(r)
            actual = r.endswith("*")
            nombre = _html.escape(r[:-1].strip() if actual else r)
            color = "#EAB308" if actual else "#9CA3AF"
            marca = "* " if actual else "&nbsp;&nbsp;"
            filas.append(
                f'<li class="tree-dir__li">'
                f'<span class="tree-dir__ico" style="color:{color}">'
                f'{_SVG_OPEN}{ICONOS["git"][1]}</svg></span>'
                f'<span class="prompt">{marca}</span><span>{nombre}</span></li>')
        cuerpo = f'<ul class="tree-dir__ul">{"".join(filas)}</ul>'
    else:
        nodos = props.get("nodos") or props.get("items") or []
        if not nodos and props.get("tree"):
            nodos = _nodos_desde_texto(props["tree"])
        if len(nodos) > MAX_LINEAS:
            if warnings is not None:
                warnings.append(f"tree: {len(nodos)} líneas > {MAX_LINEAS}, se recortan")
            nodos = nodos[:MAX_LINEAS]
        filas = []
        for nd in nodos:
            if isinstance(nd, str):
                if _es_guiada(nd):
                    tmp = _nodos_desde_texto(nd)
                    nd = tmp[0] if tmp else {"v": nd}
                else:
                    nd = {"v": nd}
            v = nd.get("v") or nd.get("texto") or ""
            depth = int(nd.get("depth") or nd.get("nivel") or 0)
            tipo = (nd.get("tipo") or "").lower()
            if not tipo or tipo not in ICONOS:
                tipo = "dir" if str(v).strip().endswith("/") else _tipo_archivo(v)
            filas.append(_li(v, depth, tipo))
        cuerpo = f'<ul class="tree-dir__ul">{"".join(filas)}</ul>'
    titulo_html = (f'<div class="tree-dir__titulo">{_html.escape(str(titulo))}</div>'
                   if titulo else "")
    return f'<div class="tree-dir">{titulo_html}{cuerpo}</div>'
