"""Genera `lucide_sets.py`: iconos Lucide normalizados al estilo de la casa.

Fuente: lucide-static (licencia ISC) — https://lucide.dev
Los SVG de Lucide traen stroke/stroke-width en el <svg> raíz y los hijos
heredan; acá se envuelve el contenido en un <g> con el trazo de la casa
(stroke=url(#c), stroke-width=1.5) para que funcione como glyph del registry.

Uso:
    python3 -m icons.sync_lucide          # baja y regenera lucide_sets.py
    python3 -m icons.sync_lucide --ver 1.59.0

El resultado NO se importa solo: el registry lo mezcla (Lucide primero, el
trazo a mano de la casa gana en caso de colisión de nombre).
"""

import io
import re
import sys
import tarfile
import urllib.request
from pathlib import Path

VERSION_DEF = "1.59.0"

# Iconos curados por categoría, en orden de rol (portada → contenido → cierre).
CATS = {
    "cybersec": [
        "shield-alert", "lock-keyhole", "fingerprint", "scan-face", "crosshair",
        "siren", "triangle-alert", "user-x", "badge-check", "shield-off",
        "key-round", "bug-off", "door-closed", "mail-warning", "link-2-off",
        "biohazard", "skull", "scan-line", "shield-plus", "file-lock",
        "user-check", "alert-octagon", "shield-ban", "venetian-mask",
        "footprints", "key-square", "shield-question", "file-warning",
    ],
    "dev": [
        "terminal", "git-branch", "code-xml", "braces", "package", "workflow",
        "test-tube", "binary", "regex", "component", "database", "cpu",
        "refresh-cw", "square-function", "file-code", "boxes", "flask-conical",
        "wrench", "cog", "variable", "git-merge", "git-pull-request",
        "git-fork", "repeat", "play", "power", "blocks", "puzzle", "keyboard",
        "monitor-cog", "table", "grid-3x3", "layers", "file-terminal",
        "list-checks", "mouse-pointer-click",
    ],
    "ai": [
        "brain-circuit", "sparkles", "bot", "network", "wand-sparkles",
        "brain-cog", "atom", "orbit", "cpu", "microchip", "scan-eye",
        "message-square-code", "audio-waveform", "image", "scan-text",
        "telescope", "satellite", "antenna", "radio", "waves", "waypoints",
        "spline", "activity", "gauge", "sigma", "infinity", "combine",
        "merge", "focus", "bot-message-square", "scan-search", "search",
    ],
    "infra": [
        "server", "network", "cloud", "globe", "router", "radio-tower",
        "signal", "wifi", "ethernet-port", "cable", "plug-zap", "cpu",
        "memory-stick", "microchip", "monitor", "gauge", "activity",
        "trending-up", "container", "boxes", "package", "warehouse",
        "factory", "building-2", "map", "route", "navigation", "compass",
        "satellite-dish", "battery-charging", "zap", "thermometer", "power",
        "workflow", "waypoints", "hard-drive", "database", "cloud-cog",
        "server-cog", "server-crash",
    ],
    "genericos": [
        "rocket", "target", "trophy", "medal", "award", "star", "flame",
        "zap", "lightbulb", "book-open", "graduation-cap", "map", "compass",
        "route", "flag", "badge-check", "circle-check", "circle-x",
        "triangle-alert", "info", "circle-help", "arrow-up-right",
        "external-link", "download", "upload", "share-2", "bookmark", "heart",
        "thumbs-up", "clock", "calendar", "hash", "gift", "party-popper",
        "megaphone", "sparkles", "crown", "gem", "hourglass", "timer",
        "palette", "pencil", "pen-tool", "scissors", "wrench", "cog",
        "search", "filter", "sliders-horizontal", "users", "user-plus",
        "message-square", "mail", "phone", "bell", "tag", "ticket", "wallet",
        "credit-card", "briefcase", "building", "home", "puzzle", "blocks",
        "smile", "handshake", "scale", "landmark", "languages", "quote",
        "plus", "check", "x", "arrow-right", "move-right",
    ],
}

URL = "https://registry.npmjs.org/lucide-static/-/lucide-static-{v}.tgz"


def _cuerpo(svg: str) -> str:
    """Extrae el interior del SVG y lo envuelve con el trazo de la casa."""
    m = re.search(r"<svg[^>]*>(.*)</svg>", svg, re.S)
    if not m:
        raise ValueError("SVG sin cuerpo")
    inner = m.group(1)
    inner = re.sub(r"<!--.*?-->", "", inner, flags=re.S)
    inner = re.sub(r"<defs>.*?</defs>", "", inner, flags=re.S)
    inner = inner.replace('stroke="currentColor"', 'stroke="url(#c)"')
    inner = inner.replace('fill="currentColor"', 'fill="url(#c)"')
    inner = re.sub(r"\s+", " ", inner).strip()
    return ('<g fill="none" stroke="url(#c)" stroke-width="1.5" '
            'stroke-linecap="round" stroke-linejoin="round">'
            f"{inner}</g>")


def generar(version=VERSION_DEF):
    todos = [n for lista in CATS.values() for n in lista]
    print(f"· descargando lucide-static {version} ({len(todos)} iconos)…")
    data = urllib.request.urlopen(URL.format(v=version), timeout=180).read()
    tf = tarfile.open(fileobj=io.BytesIO(data), mode="r:gz")
    encontrados = {}
    for miembro in tf.getmembers():
        m = re.match(r".*/icons/([^/]+)\.svg$", miembro.name)
        if not m:
            continue
        nombre = m.group(1)
        if nombre not in todos:
            continue
        svg = tf.extractfile(miembro).read().decode("utf-8")
        encontrados[nombre] = _cuerpo(svg)
    faltan = [n for n in todos if n not in encontrados]
    if faltan:
        print("  ✗ faltan en el paquete:", ", ".join(faltan))
    return encontrados


def escribir(encontrados, version, destino: Path):
    lineas = [
        '"""Iconos Lucide normalizados al estilo de la casa (generado).',
        "",
        f"Fuente: lucide-static {version} · licencia ISC · https://lucide.dev",
        "NO editar a mano: regenerar con `python3 -m icons.sync_lucide`.",
        '"""',
        "",
        f'VERSION = "{version}"',
        "",
        "SETS = {",
    ]
    for cat, lista in CATS.items():
        lineas.append(f'    "{cat}": {{')
        for n in lista:
            if n not in encontrados:
                continue
            cuerpo = encontrados[n].replace('"', '\\"')
            lineas.append(f'        "{n}":')
            lineas.append(f'            "{cuerpo}",')
        lineas.append("    },")
    lineas.append("}")
    lineas.append("")
    lineas.append("# Orden de rol sugerido (portada → puente → cierre) por categoría.")
    lineas.append("ORDEN = {")
    for cat, lista in CATS.items():
        presentes = [n for n in lista if n in encontrados]
        lineas.append(f'    "{cat}": {presentes!r},')
    lineas.append("}")
    lineas.append("")
    destino.write_text("\n".join(lineas), encoding="utf-8")
    return sum(1 for c in CATS for n in CATS[c] if n in encontrados)


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    version = VERSION_DEF
    if "--ver" in argv:
        version = argv[argv.index("--ver") + 1]
    enc = generar(version)
    destino = Path(__file__).with_name("lucide_sets.py")
    total = escribir(enc, version, destino)
    print(f"  ✓ {total} iconos → {destino.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
