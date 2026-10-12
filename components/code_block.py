"""Bloque de código con numeración y resaltado ligero por tokens.

Sin parsers pesados: una pasada de regex por línea. Suficiente para que el
snippet se lea en un carrusel, no para un IDE.
"""

import html as _html
import re

MAX_LINEAS = 8

KEYWORDS = {
    "python": "def class import from return if elif else for while with as in not and or None True False try except raise lambda yield async await",
    "js": "const let var function return if else for while class new import from export default async await try catch throw null undefined true false",
    "bash": "if then else fi for do done echo cd sudo apt docker kubectl git python npm curl wget export",
    "sql": "select from where insert into update set delete create table join on group by order limit and or null",
    "go": "func package import return if else for range var const type struct interface go defer chan select nil true false",
    "rust": "fn let mut pub use struct impl match if else for while return Some None Ok Err",
    "generic": "if else for while return function class import",
}
KEYWORDS["sh"] = KEYWORDS["bash"]
KEYWORDS["shell"] = KEYWORDS["bash"]
KEYWORDS["typescript"] = KEYWORDS["js"]
KEYWORDS["ts"] = KEYWORDS["js"]
KEYWORDS["java"] = KEYWORDS["js"]

_COMENT = {"python": r"#", "bash": r"#", "sh": r"#", "shell": r"#", "go": r"//",
           "js": r"//", "ts": r"//", "typescript": r"//", "java": r"//",
           "rust": r"//", "sql": r"--"}

_TOKEN = re.compile(
    r"""(?P<com>#[^\n]*|//[^\n]*|--[^\n]*)"""
    r"""|(?P<str>["'][^"'\n]*["'])"""
    r"""|(?P<num>\b\d+(?:\.\d+)?\b)"""
    r"""|(?P<fn>\b[A-Za-z_]\w*(?=\())"""
    r"""|(?P<kw>\b[A-Za-z_]\w*\b)"""
)


def resaltar(linea: str, lenguaje: str) -> str:
    kw = set(KEYWORDS.get(lenguaje, KEYWORDS["generic"]).split())
    com_pref = _COMENT.get(lenguaje, "#")
    salida = []
    pos = 0
    for m in _TOKEN.finditer(linea):
        salida.append(_html.escape(linea[pos:m.start()]))
        pos = m.end()
        texto = m.group(0)
        if m.lastgroup == "com":
            if texto.startswith(com_pref):
                salida.append(f'<span class="tok-com">{_html.escape(texto)}</span>')
            else:
                salida.append(_html.escape(texto))
            continue
        if m.lastgroup == "str":
            salida.append(f'<span class="tok-str">{_html.escape(texto)}</span>')
        elif m.lastgroup == "num":
            salida.append(f'<span class="tok-num">{_html.escape(texto)}</span>')
        elif m.lastgroup == "fn":
            salida.append(f'<span class="tok-fn">{_html.escape(texto)}</span>')
        elif texto in kw:
            salida.append(f'<span class="tok-kw">{_html.escape(texto)}</span>')
        else:
            salida.append(_html.escape(texto))
    salida.append(_html.escape(linea[pos:]))
    return "".join(salida)


def render(props, ctx, warnings=None):
    lenguaje = str(props.get("lenguaje") or props.get("lang") or "generic").lower()
    codigo = str(props.get("codigo") or props.get("code") or "")
    notas = str(props.get("notas") or props.get("note") or "").strip()
    lineas = codigo.split("\n")
    if len(lineas) > MAX_LINEAS:
        if warnings is not None:
            warnings.append(
                f"code: {len(lineas)} líneas > {MAX_LINEAS} — el snippet se "
                f"recorta; divídelo en 2 slides si necesitas el resto")
        lineas = lineas[:MAX_LINEAS]
    filas = "".join(
        f'<div class="code__line"><span class="code__ln">{i}</span>'
        f'<span class="code__src">{resaltar(ln, lenguaje)}</span></div>'
        for i, ln in enumerate(lineas, 1)
    )
    notas_html = f'<div class="code__note">{_html.escape(notas)}</div>' if notas else ""
    etiqueta = props.get("titulo") or lenguaje.upper()
    return (
        '<div class="code">'
        f'<div class="code__head"><span>{_html.escape(str(etiqueta))}</span>'
        f'<span>{len(lineas)} líneas</span></div>'
        f'<div class="code__body">{filas}</div>{notas_html}</div>'
    )
