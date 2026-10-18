#!/usr/bin/env python3
"""icon-smith — elige, busca y crea iconos por tema para los carruseles.

Trabaja sobre la librería `icons/` (Lucide normalizado + trazo de la casa) y
sobre los overlays locales `icons/lucide_extra.py` y `icons/tema_extra.py`,
que NO se pierden al regenerar la librería con `python3 -m icons.sync_lucide`.

Subcomandos:
  sugerir "<tema>" [--slides N] [--categoria CAT]
      Qué glyph recibiría cada slide (portada, contenido, puente, cierre).
  sugerir --tema <slug> [--dir CTSLIDER]
      Igual, pero leyendo los slides reales del carrusel.
  buscar "<texto>" [--limit N]
      Glyphs/reglas que matchean el texto + candidatos del catálogo Lucide.
  listar [CAT] [--grep TEXTO]
      Glyphs disponibles por categoría.
  catalogo [--grep TEXTO] [--limit N] [--refresh]
      Busca en el catálogo de Lucide (2159 iconos) para agregar nuevos.
  agregar <CAT> <icono>... [--kw "a,b"] [--orden] [--dry-run]
      Baja de Lucide, convierte al estilo de la casa y escribe el overlay.

Ejemplos:
  python3 icon_smith.py sugerir "Fugas de correo con Python" --slides 7
  python3 icon_smith.py buscar "kubernetes"
  python3 icon_smith.py catalogo --grep "radar"
  python3 icon_smith.py agregar cybersec radar-crosshair --kw "radar,microondas"
"""

import argparse
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ))

VERSION_LUCIDE = "1.59.0"
CDN = "https://cdn.jsdelivr.net/npm/lucide-static@{v}/icons/{n}.svg"
LISTA_CDN = "https://data.jsdelivr.com/v1/packages/npm/lucide-static@{v}?structure=flat"
CACHE = RAIZ / "icons" / "lucide_catalogo.txt"

DEPENDENCIAS_EXTRA = RAIZ / "icons" / "lucide_extra.py"
REGLAS_EXTRA = RAIZ / "icons" / "tema_extra.py"


# ── utilidades ─────────────────────────────────────────────────────

def _icons():
    from icons import registry

    return registry


def _acc():
    return {"rgb": (250, 204, 21), "bright_rgb": (255, 235, 120)}


def _normalizar(t):
    import unicodedata

    t = (t or "").lower()
    t = unicodedata.normalize("NFKD", t)
    return "".join(c for c in t if not unicodedata.combining(c))


def _catalogo(refresh=False):
    """Nombres de iconos de Lucide (caché local; si no hay red, usa la librería)."""
    nombres = set()
    if CACHE.exists() and not refresh:
        nombres |= {l.strip() for l in CACHE.read_text().splitlines() if l.strip()}
    if not nombres or refresh:
        try:
            with urllib.request.urlopen(LISTA_CDN.format(v=VERSION_LUCIDE),
                                        timeout=60) as r:
                flat = json.load(r)
            nombres = {
                m.group(1)
                for f in flat["files"]
                if (m := re.match(r"/icons/(.+)\.svg$", f["name"]))
            }
            CACHE.write_text("\n".join(sorted(nombres)), encoding="utf-8")
        except Exception as e:  # sin red: degradamos al catálogo instalado
            print(f"  ! catálogo Lucide no disponible ({e}); uso la librería local")
    if not nombres:
        for s in _icons().CATEGORIAS.values():
            nombres |= set(s.GLYPHS)
    return sorted(nombres)


def _textos_del_tema(tema, base=None):
    """(nombre, texto) por slide del carrusel, con el mismo criterio del builder."""
    base = Path(base or os.environ.get("CTSLIDER_DIR", "/sdcard/CTSLIDER")) / tema
    for src in sorted(base.glob("slide-*.html")):
        txt = src.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r'<div class="contenido">(.*?)</div>\s*<div class="pie"',
                      txt, re.S)
        cuerpo = m.group(1) if m else txt
        cuerpo = re.sub(r'data-component="[^"]*"', " ", cuerpo)
        yield src.name, cuerpo


# ── sugerir ────────────────────────────────────────────────────────

def cmd_sugerir(args):
    R = _icons()
    cat = args.categoria
    if cat not in R.CATEGORIAS:
        cat = R.detectar_categoria(args.tema or "")
    if args.tema and args.tema in R.CATEGORIAS:
        cat = args.tema

    if args.dir:
        textos = list(_textos_del_tema(args.tema_dir or args.tema, args.dir))
    else:
        n = args.slides or 5
        texto = args.tema or ""
        textos = [(f"slide-{i + 1:02d}", texto) for i in range(n)]

    total = len(textos)
    print(f"tema      : {args.tema or '(sin texto)'}")
    print(f"categoría : {cat}")
    print(f"slides    : {total}")
    print()
    usados = set()
    for i, (nombre, texto) in enumerate(textos, 1):
        g = R.glyph_por_texto(texto, usados)
        via = "texto"
        if g:
            uri = R.get_icon(g, _acc(), cat)
            if not uri:
                g = None
        if not g:
            g = R.elegir_icono(i, total, _acc(), tema=cat, texto=None,
                               usados=usados)[0]
            via = "rol"
        if g:
            usados.add(g)
        print(f"  {i:2}/{total}  {g or '—':<22} ({via})   {nombre}")
    print()
    print(f"glyphs del set: {len(R.CATEGORIAS[cat].GLYPHS)}")
    print("Forzá otra categoría con --categoria o --iconos en tech_carousel.py.")


# ── buscar / listar / catalogo ─────────────────────────────────────

def cmd_buscar(args):
    R = _icons()
    texto = args.texto
    t = " " + _normalizar(texto) + " "
    print(f"── reglas tema→icono que matchean «{texto}»")
    reglas = tuple(getattr(R, "_TEMA_RULES", ())) + R.TEMA_GLYPHS
    for claves, glyph in reglas:
        for c in claves:
            if _normalizar(c) and re.search(r"(?<![a-z0-9])" + re.escape(_normalizar(c)), t):
                print(f"   · {glyph:<24} ← «{c}»")
                break
    print()
    print(f"── glyphs instalados que coinciden con «{texto}»")
    vistos = set()
    for cat, s in R.CATEGORIAS.items():
        for nombre in sorted(s.GLYPHS):
            if nombre in vistos:
                continue
            if _normalizar(texto) in _normalizar(nombre):
                vistos.add(nombre)
                print(f"   · {nombre:<24} [{cat}]")
    if not vistos:
        print("   (ninguno)")
    print()
    print(f"── candidatos en el catálogo Lucide")
    cat = [n for n in _catalogo(args.refresh) if _normalizar(texto) in _normalizar(n)]
    for n in cat[: args.limit]:
        print(f"   · {n}")
    resto = len(cat) - min(len(cat), args.limit)
    if resto > 0:
        print(f"   … {resto} más")
    if cat:
        print()
        print(f"  agregar: python3 icon_smith.py agregar <CAT> "
              f"{' '.join(cat[:3])}")


def cmd_listar(args):
    R = _icons()
    cats = [args.categoria] if args.categoria else list(R.CATEGORIAS)
    for cat in cats:
        if cat not in R.CATEGORIAS:
            print(f"  ! categoría desconocida: {cat}")
            continue
        gs = R.nombres(cat)
        if args.grep:
            gs = [g for g in gs if args.grep.lower() in g.lower()]
        print(f"── {cat} ({len(gs)})")
        cols = 6
        for k in range(0, len(gs), cols):
            print("   " + "".join(f"{g:<22}" for g in gs[k:k + cols]))
        print()


def cmd_catalogo(args):
    nombres = _catalogo(args.refresh)
    if args.grep:
        nombres = [n for n in nombres if args.grep.lower() in n.lower()]
    print(f"catálogo Lucide {VERSION_LUCIDE}: {len(nombres)} iconos"
          + (f" (filtro «{args.grep}»)" if args.grep else ""))
    for k in range(0, min(len(nombres), args.limit), 5):
        print("   " + "".join(f"{n:<24}" for n in nombres[k:k + 5]))
    if len(nombres) > args.limit:
        print(f"   … {len(nombres) - args.limit} más (subí --limit)")


# ── agregar ────────────────────────────────────────────────────────

def _cuerpo_lucide(nombre):
    from icons.sync_lucide import _cuerpo

    url = CDN.format(v=VERSION_LUCIDE, n=nombre)
    with urllib.request.urlopen(url, timeout=60) as r:
        return _cuerpo(r.read().decode("utf-8"))


def _leer_overlay(path, claves):
    """Lee SETS/ORDEN (o TEMA_GLYPHS) del overlay actual sin importar el paquete."""
    ns = {}
    if path.exists():
        exec(compile(path.read_text(encoding="utf-8"), str(path), "exec"), ns)
    return {k: ns.get(k) for k in claves}


def _escribir_iconos(sets, orden):
    lineas = [
        '"""Overlay local de iconos — lo escribe `icon_smith.py agregar`.',
        "",
        "Se mezcla SOBRE `lucide_sets.py`, así que los iconos que agregue el agente",
        "NO se pierden al regenerar con `python3 -m icons.sync_lucide`.",
        '"""',
        "",
        "SETS = {",
    ]
    for cat in sorted(sets):
        lineas.append(f"    {json.dumps(cat)}: {{")
        for nombre in sorted(sets[cat]):
            lineas.append(f"        {json.dumps(nombre)}:")
            lineas.append(f"            {json.dumps(sets[cat][nombre])},")
        lineas.append("    },")
    lineas += ["}", "", "ORDEN = {"]
    for cat in sorted(orden):
        lineas.append(f"    {json.dumps(cat)}: {orden[cat]!r},")
    lineas += ["}", ""]
    DEPENDENCIAS_EXTRA.write_text("\n".join(lineas), encoding="utf-8")


def _escribir_reglas(reglas):
    lineas = [
        '"""Reglas locales de icono-por-tema — las escribe `icon_smith.py agregar --kw`.',
        "",
        "Se evalúan ANTES que `registry.TEMA_GLYPHS`.",
        '"""',
        "",
        "TEMA_GLYPHS = (",
    ]
    for claves, glyph in reglas:
        lineas.append(f"    ({claves!r}, {glyph!r}),")
    lineas += [")", ""]
    REGLAS_EXTRA.write_text("\n".join(lineas), encoding="utf-8")


def cmd_agregar(args):
    R = _icons()
    if args.categoria not in R.CATEGORIAS:
        print(f"  ! categoría desconocida: {args.categoria} "
              f"(usa: {', '.join(sorted(R.CATEGORIAS))})")
        return 2
    sets = _leer_overlay(DEPENDENCIAS_EXTRA, ("SETS", "ORDEN"))
    sets = {c: dict(v or {}) for c, v in (sets.get("SETS") or {}).items()}
    orden = {c: list(v or []) for c, v in (sets.get("ORDEN") or {}).items()}
    cat = args.categoria
    sets.setdefault(cat, {})
    orden.setdefault(cat, [])
    existentes = set()
    for s in R.CATEGORIAS.values():
        existentes |= set(s.GLYPHS)

    ok = 0
    for nombre in args.iconos:
        if nombre in existentes:
            print(f"  · {nombre}: ya existe en la librería, se omite")
            continue
        try:
            cuerpo = _cuerpo_lucide(nombre)
        except Exception as e:
            print(f"  ✗ {nombre}: no se pudo bajar de Lucide ({e})")
            continue
        sets[cat][nombre] = cuerpo
        if nombre not in orden[cat]:
            orden[cat].append(nombre)
        ok += 1
        print(f"  ✓ {nombre} → {cat}")

    if not ok:
        print("  (nada para agregar)")
        return 1
    if args.dry_run:
        print("  (--dry-run: no se escribió nada)")
        return 0

    _escribir_iconos(sets, orden)
    print(f"  · overlay: {DEPENDENCIAS_EXTRA.relative_to(RAIZ)}")

    if args.kw:
        reglas = list(_leer_overlay(REGLAS_EXTRA, ("TEMA_GLYPHS",)).get("TEMA_GLYPHS") or ())
        nuevas = tuple(k.strip() for k in args.kw.split(",") if k.strip())
        destino = args.iconos[0]
        reglas = [(c, g) for c, g in reglas if g != destino or set(c) != set(nuevas)]
        reglas.insert(0, (nuevas, destino))
        _escribir_reglas(reglas)
        print(f"  · reglas: {destino} ← {', '.join(nuevas)}")
    return 0


# ── CLI ────────────────────────────────────────────────────────────

def main(argv=None):
    ap = argparse.ArgumentParser(prog="icon_smith.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("sugerir", help="glyph por slide (rol/tema)")
    s.add_argument("tema", nargs="?", help="texto del tema o slug del carrusel")
    s.add_argument("--slides", type=int, default=0)
    s.add_argument("--categoria", default="auto")
    s.add_argument("--dir", help="dir base del CTSLIDER si leés slides reales")
    s.add_argument("--tema-dir", dest="tema_dir", help="slug del carrusel a leer")
    s.set_defaults(func=cmd_sugerir)

    b = sub.add_parser("buscar", help="glyphs y candidatos para un texto")
    b.add_argument("texto")
    b.add_argument("--limit", type=int, default=12)
    b.add_argument("--refresh", action="store_true")
    b.set_defaults(func=cmd_buscar)

    l = sub.add_parser("listar", help="glyphs disponibles")
    l.add_argument("categoria", nargs="?", default="")
    l.add_argument("--grep", default="")
    l.set_defaults(func=cmd_listar)

    c = sub.add_parser("catalogo", help="catálogo Lucide")
    c.add_argument("--grep", default="")
    c.add_argument("--limit", type=int, default=40)
    c.add_argument("--refresh", action="store_true")
    c.set_defaults(func=cmd_catalogo)

    a = sub.add_parser("agregar", help="agrega iconos de Lucide al overlay")
    a.add_argument("categoria")
    a.add_argument("iconos", nargs="+")
    a.add_argument("--kw", default="", help="palabras clave separadas por coma")
    a.add_argument("--orden", action="store_true", help="(reservado)")
    a.add_argument("--dry-run", action="store_true")
    a.set_defaults(func=cmd_agregar)

    args = ap.parse_args(argv)
    return args.func(args) or 0


if __name__ == "__main__":
    raise SystemExit(main())
