"""Registry de iconos TechEdu.

API:
    from icons import get_icon, icono_slide, detectar_categoria
    get_icon("shield", accent_vars)            → data URI
    icono_slide(3, 8, accent_vars, categoria)  → data URI por rol
    detectar_categoria("sql-injection")        → "cybersec"

Self-test:
    python3 -m icons.registry --test [categoria ...]
"""

import re
import sys
import xml.etree.ElementTree as ET

from . import ai as _ai
from . import cybersec as _cyber
from . import dev as _dev
from . import genericos as _gen
from . import infra as _infra
from . import lucide_sets as _lucide
from .common import data_uri, glyph_svg

try:  # Overlay local que escribe icon_smith.py (no se pisa al re-sincronizar).
    from . import lucide_extra as _extra
except ImportError:  # pragma: no cover
    _extra = None

try:  # Reglas locales tema→icono que escribe icon_smith.py.
    from . import tema_extra as _tema_extra
    _TEMA_RULES = tuple(_tema_extra.TEMA_GLYPHS)
except ImportError:  # pragma: no cover
    _TEMA_RULES = ()


class _Set:
    """Categoría combinada: glyphs de Lucide + el trazo a mano de la casa."""

    __slots__ = ("GLYPHS", "ORDEN")

    def __init__(self, glyphs, orden):
        self.GLYPHS = glyphs
        self.ORDEN = orden


def _combinar(mod, cat):
    """Lucide + overlay local primero; el trazo a mano gana si comparten nombre."""
    glyphs = dict(_lucide.SETS.get(cat, {}))
    if _extra is not None:
        glyphs.update(_extra.SETS.get(cat, {}))
    glyphs.update(getattr(mod, "GLYPHS", {}))
    orden = list(_extra.ORDEN.get(cat, ())) if _extra is not None else []
    for nombre in _lucide.ORDEN.get(cat, ()):
        if nombre not in orden:
            orden.append(nombre)
    for nombre in getattr(mod, "ORDEN", ()):
        if nombre not in orden:
            orden.append(nombre)
    return _Set(glyphs, orden)


CATEGORIAS = {
    "cybersec": _combinar(_cyber, "cybersec"),
    "dev": _combinar(_dev, "dev"),
    "ai": _combinar(_ai, "ai"),
    "infra": _combinar(_infra, "infra"),
    "data": _combinar(_gen, "genericos"),
    "educativo": _combinar(_gen, "genericos"),
    "common": _combinar(_gen, "genericos"),
    "tech": _combinar(_gen, "genericos"),
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

# Preferencias de glyph por rol del slide (si el glyph existe y no se usó).
_CIERRE = ("rocket", "arrow-right", "check", "target")
_PUENTE = ("list-checks", "target", "flag", "check")


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


# ── Icono semántico: palabra clave del slide → glyph ──────────────
# Gana la clave que aparece MÁS TEMPRANO en el texto del slide (empates:
# orden de esta tabla). Las claves van normalizadas (sin tildes, minúscula).

TEMA_GLYPHS = (
    # ─ Ciberseguridad ─
    (("phishing", "anzuelo", "suplantacion"), "link-2-off"),
    (("ransomware", "secuestro de datos", "rescate"), "lock-keyhole"),
    (("malware", "virus", "troyano", "gusano", "backdoor"), "bug-off"),
    (("inyeccion", "sql injection", "xss", "csrf", "xxe"), "crosshair"),
    (("pentest", "pentesting", "hacking", "explot", "payload", "kali"), "crosshair"),
    (("contrasena", "password", "credencial"), "key-round"),
    (("2fa", "mfa", "doble factor", "autenticacion"), "fingerprint"),
    (("cifrado", "encript", "aes", "cifrar", "criptografia"), "lock"),
    (("hash", "hashing", "sha", "md5"), "hash"),
    (("vulnerab", "cve", "fallo de seguridad"), "shield-alert"),
    (("firewall", "hardening", "blindaje"), "firewall"),
    (("osint", "reconocimiento", "rastreo", "huella"), "radar"),
    (("vpn", "tunel", "anonimato"), "vpn"),
    (("fuga", "brecha", "leak", "exposicion", "filtracion"), "mail-warning"),
    (("certificado", "tls", "ssl", "https"), "certificate"),
    (("ciber", "seguridad", "proteccion", "defensa"), "shield"),
    # ─ Desarrollo ─
    (("docker", "contenedor", "imagen docker"), "container"),
    (("kubernetes", "k8s", "orquest"), "server-cog"),
    (("git", "commit", "rama", "repositorio", "merge"), "git-branch"),
    (("pull request", "code review", "revision de codigo"), "git-pull-request"),
    (("api", "endpoint", "rest", "graphql"), "code-xml"),
    (("base de datos", "database", "postgres", "mysql", "sql"), "database"),
    (("test", "testing", "prueba", "unitari"), "test-tube"),
    (("regex", "expresion regular"), "regex"),
    (("lint", "linter", "formato de codigo"), "list-checks"),
    (("terminal", "consola", "comando", "bash", "shell"), "terminal"),
    (("python", "pip install", "django", "flask"), "flask-conical"),
    (("javascript", "typescript", "node", "npm"), "braces"),
    (("html", "css", "web", "frontend"), "code"),
    (("bug", "error", "depurar", "debug"), "bug"),
    (("refactor", "patron", "arquitectura", "estructura"), "blocks"),
    (("libreria", "paquete", "dependencia", "package"), "package"),
    (("algoritmo", "estructura de datos", "complejidad"), "binary"),
    (("funciones", "funcion ", "def ", "metodo", "clase", "objeto"), "square-function"),
    (("ci ", "cd ", "pipeline", "integracion continua"), "workflow"),
    (("codigo", "programar", "script", "programacion"), "code-xml"),
    # ─ IA ─
    (("llm", "gpt", "modelo de lenguaje", "claude", "gemini"), "brain-circuit"),
    (("prompt", "instruccion", "system prompt"), "message-square-code"),
    (("rag", "embedding", "vector"), "orbit"),
    (("agente", "agentic", "autonom"), "bot"),
    (("entrena", "fine-tun", "dataset"), "brain-cog"),
    (("inferencia", "prediccion", "modelo"), "brain"),
    (("gpu", "tensor", "neural"), "microchip"),
    (("vision", "imagen", "ocr", "reconocimiento de imagen"), "scan-eye"),
    (("chatbot", "chat", "conversacion"), "bot-message-square"),
    (("inteligencia artificial", "machine learning", "deep learning", " ia"), "sparkles"),
    (("automatiz", "automatizar"), "wand-sparkles"),
    # ─ Infra ─
    (("linux", "ubuntu", "debian", "kernel"), "terminal"),
    (("servidor", "server", "vps", "hosting"), "server"),
    (("redes", "red ", "network", "subred", "lan"), "network"),
    (("nube", "cloud", "aws", "azure", "gcp"), "cloud"),
    (("dns", "dominio", "resolucion"), "globe"),
    (("ssh", "acceso remoto", "puerto"), "ethernet-port"),
    (("nginx", "proxy", "balanceo", "carga"), "router"),
    (("deploy", "despliegue", "produccion"), "workflow"),
    (("monitoreo", "observabilidad", "metricas"), "activity"),
    (("backup", "respaldo", "restauracion"), "database"),
    (("disco", "almacenamiento", "ssd", "raid"), "hard-drive"),
    (("cpu", "procesador", "ram", "memoria ram"), "cpu"),
    (("iot", "sensor", "dispositivo"), "microchip"),
    (("wifi", "inalambric", "router wifi"), "wifi"),
    (("energia", "bateria", "consumo"), "battery-charging"),
    # ─ Datos / general ─
    (("dataframe", "dataset", "dato", "datos"), "chart-bar"),
    (("dashboard", "tablero", "reporte"), "grid-3x3"),
    (("metrica", "kpi", "estadistic", "analitica"), "trending-up"),
    (("grafica", "grafico", "plot"), "activity"),
    (("curso", "tutorial", "guia", "aprender"), "graduation-cap"),
    (("roadmap", "plan", "ruta"), "roadmap"),
    (("checklist", "pasos", "resumen"), "list-checks"),
    (("mito", "error comun", "cuidado"), "circle-x"),
    (("consejo", "tip", "truco"), "lightbulb"),
    (("herramienta", "utilidad"), "wrench"),
    (("comparativa", "comparar", "vs"), "scale"),
    (("precio", "costo", "gratis"), "wallet"),
    (("lanzamiento", "novedad"), "rocket"),
    (("comunidad", "seguidores", "personas"), "users"),
    (("logro", "exito", "metas", "objetivo"), "trophy"),
)


def glyph_por_texto(texto, usados=()):
    """Mejor glyph por palabra clave del texto; None si no hay match.

    Gana la clave que aparece MÁS TEMPRANO en el texto (empates: orden de
    TEMA_GLYPHS). Requiere límite de palabra al inicio, para no confundir
    "pipeline" con "pip" ni "funciona" con "funcion".
    """
    t = " " + _normalizar(texto) + " "
    mejor = None  # (posicion, orden, glyph)
    for orden, (claves, glyph) in enumerate(_TEMA_RULES + TEMA_GLYPHS):
        if glyph in usados:
            continue
        for c in claves:
            k = _normalizar(c)
            if not k:
                continue
            m = re.search(r"(?<![a-z0-9])" + re.escape(k), t)
            if m:
                cand = (m.start(), orden, glyph)
                if mejor is None or cand[:2] < mejor[:2]:
                    mejor = cand
                break
    return mejor[2] if mejor else None


def elegir_icono(idx, total, accent_vars, tema="auto", categoria=None,
                 texto=None, usados=()):
    """(nombre, uri). Intenta por el texto del slide; cae al rol."""
    cat = categoria or (tema if tema in CATEGORIAS else detectar_categoria(tema))
    if cat not in CATEGORIAS:
        cat = _DEFAULT
    if texto:
        g = glyph_por_texto(texto, usados)
        if g:
            uri = get_icon(g, accent_vars, cat)
            if uri:
                return g, uri
    lista = nombres(cat)
    if not lista:
        return None, None
    if idx <= 1:
        nombre = lista[0]
    else:
        # Preferencias de rol (si el glyph existe y no se usó).
        pref = ()
        if idx >= total:
            pref = _CIERRE
        elif idx == total - 1:
            pref = _PUENTE
        nombre = None
        for g in pref:
            if g not in usados and get_icon(g, accent_vars, cat):
                nombre = g
                break
        if nombre is None:
            if idx >= total:
                nombre = lista[3] if len(lista) > 3 else lista[-1]
            elif idx == total - 1:
                nombre = lista[1] if len(lista) > 1 else lista[0]
            else:
                # Contenido: rota por el índice sin repetir los ya usados.
                base = 2 if len(lista) > 4 else 0
                for k in range(len(lista)):
                    cand = lista[(base + (idx - 2) + k) % len(lista)]
                    if cand not in usados:
                        nombre = cand
                        break
                if nombre is None:
                    nombre = lista[base + (idx - 2) % max(1, len(lista) - base)]
    return nombre, get_icon(nombre, accent_vars, cat)


def icono_slide(idx, total, accent_vars, tema="auto", categoria=None,
                texto=None, usados=()):
    """Ícono por rol del slide (portada / contenido / puente / cierre)."""
    return elegir_icono(idx, total, accent_vars, tema, categoria,
                        texto, usados)[1]


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
