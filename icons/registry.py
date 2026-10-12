"""Registry de iconos TechEdu.

API:
    from icons import get_icon, icono_slide, detectar_categoria
    get_icon("shield", accent_vars)            → data URI
    icono_slide(3, 8, accent_vars, categoria)  → data URI por rol
    detectar_categoria("sql-injection")        → "cybersec"

Self-test:
    python3 -m icons.registry --test [categoria ...]
"""

import sys
import xml.etree.ElementTree as ET

from . import ai as _ai
from . import cybersec as _cyber
from . import dev as _dev
from . import genericos as _gen
from . import infra as _infra
from .common import data_uri, glyph_svg

CATEGORIAS = {
    "cybersec": _cyber,
    "dev": _dev,
    "ai": _ai,
    "infra": _infra,
    "data": _gen,
    "educativo": _gen,
    "common": _gen,
    "tech": _gen,
}

# Compat con el nombre viejo (los builders importan TEMAS_SETS).
TEMAS_SETS = tuple(CATEGORIAS)

# Orden = precedencia anti-colisión (primer match gano).
_DETECCION = (
    ("cybersec", (
        "ciber", "seguridad", "vulner", "inyecc", "sql", "xss", "phishing",
        "ransom", "malware", "exploit", "pentest", "zero-trust", "zerotrust",
        "auth", "firewall", "red-team", "blueteam", "blue-team", "cifrado",
        "hash", "2fa", "mfa", "xxe", "csrf", "log4shell", "ddos", "burp",
        "owasp", "phish", "backdoor", "rootkit", "botnet", "cve", "ataque",
        "atac", "defensa", "hardening", "bounty", "kali", "wireshark",
        "nmap", "metasploit", "injection", "deserializ", "credential",
    )),
    ("ai", (
        "inteligencia", "artificial", " ia", "ia-", "llm", "gpt", "prompt",
        "rag", "embedding", "agente", "modelo", "token", "fine-tun", "entrena",
        "inferencia", "transformer", "mcp", "guardrail", "alucina", "vision",
        "machine-learning", "deep-learning", "neural", "claude", "copilot",
        "chatbot", "vectorial", "vectoriz",
    )),
    ("infra", (
        "red", "redes", "linux", "ubuntu", "debian", "servidor", "kubernetes",
        "k8s", "contenedor", "docker", "ci-cd", "pipeline", "nube", "aws",
        "azure", "gcp", "deploy", "sre", "monitoreo", "observabilidad",
        "dns", "tcp", "udp", "ip", "subred", "vpn", "ssh", "nginx", "carga",
        "balanceo", "cluster", "terraform", "ansible", "backup",
    )),
    ("dev", (
        "python", "javascript", "typescript", "java", "rust", "golang",
        " git", "git-", "commit", "api", "rest", "test", "testing", "refactor",
        "patron", "patrón", "arquitectura", "diseno", "diseño", "algoritmo",
        "base-de-datos", "sql-code", "linter", "ide", "codigo", "código",
        "funcion", "función", "clase", "objeto", "framework", "libreria",
        "librería", "version", "repositorio", "github", "debug", "bug-code",
    )),
    ("data", (
        "dato", "datos", "dataframe", "analitica", "analítica", "metrica",
        "métrica", "grafica", "gráfica", "dashboard", "etl", "sql-analytics",
        "estadistic", "correlacion",
    )),
    ("educativo", (
        "tutorial", "guia", "guía", "curso", "paso", "aprende", "manual",
        "checklist", "roadmap", "concepto",
    )),
)

_DEFAULT = "tech"


def _normalizar(texto):
    import unicodedata
    return "".join(
        c for c in unicodedata.normalize("NFKD", (texto or "").lower())
        if not unicodedata.combining(c)
    )


def detectar_categoria(*textos):
    """Elige la categoría de íconos según el slug/tema/vertical."""
    t = " " + " ".join(_normalizar(x) for x in textos if x) + " "
    for cat, claves in _DETECCION:
        for c in claves:
            if _normalizar(c).strip() and _normalizar(c) in t:
                return cat
    return _DEFAULT


def nombres(categoria):
    """Glyphs de una categoría en orden de rol (portada → puente → cierre)."""
    mod = CATEGORIAS.get(categoria, CATEGORIAS[_DEFAULT])
    orden = [n for n in getattr(mod, "ORDEN", ()) if n in mod.GLYPHS]
    resto = sorted(n for n in mod.GLYPHS if n not in orden)
    return orden + resto


def get_icon(nombre, accent_vars, categoria=None):
    """Glyph por nombre → data URI. None si no existe."""
    mods = []
    if categoria:
        mods.append(CATEGORIAS.get(categoria))
    mods.extend(CATEGORIAS.values())
    for mod in mods:
        if mod is None:
            continue
        cuerpo = mod.GLYPHS.get(nombre)
        if cuerpo:
            rgb = accent_vars.get("rgb", (255, 184, 0))
            bright = accent_vars.get("bright_rgb", rgb)
            return data_uri(glyph_svg(cuerpo, rgb, bright))
    return None


def icono_slide(idx, total, accent_vars, tema="auto", categoria=None):
    """Ícono por rol del slide (portada / contenido / puente / cierre)."""
    cat = categoria or (tema if tema in CATEGORIAS else detectar_categoria(tema))
    if cat not in CATEGORIAS:
        cat = _DEFAULT
    lista = nombres(cat)
    if not lista:
        return None
    if idx <= 1:
        nombre = lista[0]
    elif idx >= total:
        nombre = lista[3] if len(lista) > 3 else lista[-1]
    elif idx == total - 1:
        nombre = lista[1] if len(lista) > 1 else lista[0]
    else:
        # Contenido: rota por el índice de forma determinista, sin repetir
        # los 2 glyphs ya usados en portada y puente cuando hay variedad.
        base = 2 if len(lista) > 4 else 0
        nombre = lista[base + (idx - 2) % max(1, len(lista) - base)]
    return get_icon(nombre, accent_vars, cat)


# ── Self-test ──────────────────────────────────────────────────────

def _test_glyph(nombre, cuerpo):
    """Valida un glyph. Devuelve lista de errores."""
    errores = []
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">{cuerpo}</svg>'
    try:
        root = ET.fromstring(svg)
    except ET.ParseError as e:
        return [f"XML inválido: {e}"]
    for el in root.iter():
        attrs = list(el.attrib)
        sw = [a for a in attrs if a.endswith("stroke-width")]
        if len(sw) > 1:
            errores.append(f"{el.tag}: {len(sw)} stroke-width (máx 1)")
        # El defecto clásico: atributos repetidos no son posibles en XML
        # bien formado, pero sí una key duplicada escapa como texto crudo.
    if "feGaussianBlur" in cuerpo or "<filter" in cuerpo:
        errores.append("filtro SVG (no portable en headless)")
    return errores


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    categorias = [a for a in argv if a != "--test"] or list(CATEGORIAS)
    total, malos = 0, 0
    for cat in categorias:
        mod = CATEGORIAS.get(cat)
        if not mod:
            print(f"  ✗ categoría desconocida: {cat}")
            return 1
        for nombre, cuerpo in sorted(mod.GLYPHS.items()):
            total += 1
            errs = _test_glyph(nombre, cuerpo)
            if errs:
                malos += 1
                print(f"  ✗ {cat}/{nombre}: {'; '.join(errs)}")
    estado = "OK" if malos == 0 else f"{malos} con error"
    print(f"  Iconos {total} · {estado}")
    return 1 if malos else 0


if __name__ == "__main__":
    raise SystemExit(main())
