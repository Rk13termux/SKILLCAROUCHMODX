#!/usr/bin/env python3
"""
generar_copy_tech.py — copywriting determinista para carruseles TechEdu.

Dos modos:

  1) Generar slides (cuando no existen slide-*.html):
       python3 generar_copy_tech.py --tema <slug> --slides 8 \
         --vertical cybersec --color "#RRGGBB" \
         [--display-tema "..."] [--short-tema "..."] [--marca TechEdu]

  2) Generar copy-redes.md para publicar:
       python3 generar_copy_tech.py --carpeta <slug> [--funnel]

QA en ambos: dialecto tuteo-latam-neutro, contenido responsable (sin payloads
dañinos), presupuesto de palabras por plataforma y datos inventados marcados
para revisión.
"""

import argparse
import json
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from copywriting import ai as _ai
from theme import colors as _colors
from copywriting import cybersec as _cyber
from copywriting import infra as _infra
from copywriting import programming as _prog
from copywriting.base import (
    contenido_responsable,
    corregir_dialecto,
    datos_inventados,
    regionalismos_presentes,
    resolver_cta_palabra,
    rituales_presentes,
    voseo_presente,
)
from utils.render import resolver_ctslider
from utils.slug import slugificar
from utils.text import contar_palabras

BANCOS = {
    "cybersec": _cyber,
    "prog": _prog,
    "programming": _prog,
    "ai": _ai,
    "ia": _ai,
    "infra": _infra,
    "devops": _infra,
}

MARCA_DEFECTO = "TechEdu"

_STOP = {
    "de", "la", "el", "los", "las", "y", "a", "con", "para", "como", "en",
    "del", "al", "que", "lo", "un", "una", "tu", "su", "por", "sin", "sobre",
    "se", "te", "es", "son", "más", "ya", "muy", "este", "esta",
}


def _palabras(t):
    return re.findall(r"[A-Za-zÁÉÍÓÚáéíóúÑñ]+", t or "")


def _elegir(tupla, semilla):
    import zlib
    import unicodedata
    norm = "".join(c for c in unicodedata.normalize("NFKD", (semilla or "").lower())
                   if not unicodedata.combining(c))
    return tupla[zlib.crc32(norm.encode()) % len(tupla)]


def _marcar_clave(cuerpo, candidata=None):
    """Envuelve 1 keyword del cuerpo en <span class='clave'>."""
    cuerpo = cuerpo.replace("class='clave'", 'class="clave"')
    if 'class="clave"' in cuerpo:
        return cuerpo
    if candidata and re.search(rf"\b{re.escape(candidata)}\b", cuerpo, re.I):
        return re.sub(rf"\b({re.escape(candidata)})\b",
                      r'<span class="clave">\1</span>', cuerpo, count=1,
                      flags=re.I)
    for p in _palabras(cuerpo):
        if len(p) >= 6 and p.lower() not in _STOP and not p[0].isupper():
            return re.sub(rf"\b({re.escape(p)})\b",
                          r'<span class="clave">\1</span>', cuerpo, count=1)
    return cuerpo


def _plantilla(texto, tema, short):
    return (texto or "").replace("{tema}", tema).replace("{short}", short)


def _plantilla_props(props, tema, short):
    """Sustituye {tema}/{short} en todo valor string de las props (recursivo)."""
    if isinstance(props, str):
        return _plantilla(props, tema, short)
    if isinstance(props, list):
        return [_plantilla_props(v, tema, short) for v in props]
    if isinstance(props, dict):
        return {k: _plantilla_props(v, tema, short) for k, v in props.items()}
    return props


# ── Estructura de slide (contrato del parser) ──────────────────────

def _slide_html(numero, contenido, pie, resalte=None):
    # El builder descarta este <style>; sólo sirve para previsualizar la fuente.
    # Las keywords usan el MISMO color que --color, salvo que se pida otro.
    kw = _colors.resuelve_resalte(resalte, _colors.RESALTE_DEFECTO)
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  .titulo {{ font-weight: 700; }}
  .cuerpo {{ font-weight: 400; }}
  .dato {{ font-weight: 700; color: var(--acento); }}
  .resaltar {{ font-weight: 700; }}
  .cita {{ font-style: italic; }}
  .clave {{ font-weight: 700; color: {kw}; }}
</style>
</head>
<body>
  <div class="numero">{numero}</div>
  <div class="slide">
    <div class="contenido">
{contenido}
    </div>
    <div class="pie">
      <span class="logo"></span>{pie}
    </div>
  </div>
</body>
</html>
"""


def generar_slides(tema_slug, n, vertical, display, short, marca):
    banco = BANCOS.get(vertical, _cyber)
    cobertura = banco.COBERTURA
    textos = []
    slides_html = []

    hook = _elegir(banco.HOOKS, tema_slug)
    subhook = _elegir(banco.SUBHOOKS, tema_slug)
    cover = (
        '      <div class="titulo">'
        f"{hook}</div>\n"
        '      <div class="cuerpo">'
        f"{subhook}</div>"
    )
    slides_html.append((1, cover))
    textos.append(f"{hook} {subhook}")

    ultimo_componente = None
    for i in range(2, n - 1):  # slides 2 .. N-2 (contenido)
        bloque = cobertura[(i - 2) % len(cobertura)]
        # No repetir componente consecutivo al ciclar el banco
        comp = bloque["componente"]
        if comp and comp["tipo"] == ultimo_componente:
            comp = None
        titulo = _plantilla(bloque["titulo"], display, short)
        cuerpo = _plantilla(bloque["cuerpo"], display, short)
        cuerpo_corregido, _ = corregir_dialecto(cuerpo)

        partes = [f'      <div class="titulo">{titulo}</div>']
        cuerpo_html = _marcar_clave(cuerpo_corregido,
                                    candidata=short.split()[0] if short else None)
        partes.append(f'      <div class="cuerpo">{cuerpo_html}</div>')
        if comp:
            props = _plantilla_props(comp["props"], display, short)
            partes.append(
                '      <div class="componente" '
                f'data-component="{comp["tipo"]}" '
                f"data-props='{json.dumps(props, ensure_ascii=False)}'></div>"
            )
            ultimo_componente = comp["tipo"]
        slides_html.append((i, "\n".join(partes)))
        textos.append(f"{titulo} {cuerpo_corregido}")

    # N-1 (puente) y N (CTA): el builder los reemplaza; contenido mínimo.
    if n >= 3:
        slides_html.append((n - 1,
                            '      <div class="titulo">Puente</div>\n'
                            '      <div class="cuerpo">Lo inyecta el builder.</div>'))
        textos.append("Puente")
    if n >= 2:
        slides_html.append((n,
                            '      <div class="titulo">CTA final</div>\n'
                            '      <div class="cuerpo">Lo inyecta el builder.</div>'))
        textos.append("CTA final")

    slides_html.sort(key=lambda x: x[0])
    return slides_html, textos, hook


# ── copy-redes.md ──────────────────────────────────────────────────

PRESUPUESTO = {
    "Instagram": (60, 95),
    "TikTok": (30, 50),
    "Facebook": (60, 110),
}



def _hashtags_con_emojis(short, display, slug):
    base = (short or display or slug).lower()
    mapa = {
        'ls': ['💻', '#ls', '#linux', '#terminal', '#bash', '#cli'],
        'flags': ['💻', '#ls', '#terminal', '#linux', '#comandos'],
        'sql': ['🔒', '#sql', '#database', '#seguridad', '#cybersec'],
        'injection': ['🔒', '#sql', '#seguridad', '#cybersec', '#hack'],
        'python': ['🐍', '#python', '#programming', '#desarrollo', '#codigo'],
        'testing': ['🧪', '#testing', '#pytest', '#qa', '#unittest'],
        'pytest': ['🧪', '#pytest', '#testing', '#python', '#qa'],
        'prompt': ['🤖', '#prompt', '#ia', '#ai', '#llm', '#chatgpt'],
        'ia': ['🤖', '#ia', '#ai', '#llm', '#prompt'],
        'deploy': ['🚀', '#deploy', '#cicd', '#devops', '#github'],
        'cicd': ['🔧', '#cicd', '#devops', '#deploy', '#github'],
    }
    hs, em = [], []
    for k, v in mapa.items():
        if k in base:
            for x in v:
                if not x.startswith('#') and x not in em: em.append(x)
                if x.startswith('#') and x not in hs: hs.append(x)
    if not em: em = ['💡']
    if not hs: hs = ['#tech', '#programming']
    return ' '.join(em[:2]) + '  ' + ' '.join(hs[:6])


def generar_copy_redes(carpeta: Path, display, short, marca=None, funnel=False):
    slug = carpeta.name
    cta = resolver_cta_palabra(slug)
    marca = (marca or MARCA_DEFECTO).strip() or MARCA_DEFECTO
    hashtag_base = "#" + re.sub(r"[^a-z0-9]", "", short.lower() or "tech")

    ig = (
        f"{short} se explica en una frase y se aplica en tres.\n"
        f"En este carrusel: qué es, cómo se detecta el error típico y la "
        f"checklist para revisarlo hoy mismo.\n"
        f"Guardalo: vuelve a servirte la primera vez que te atore con esto.\n"
        f"Compartilo con quien está aprendiendo lo mismo.\n"
        f"¿Cuál de estos puntos ya lo tenías cubierto?\n"
        f"Comenta {cta} y te paso la checklist completa.\n"
        f"— {marca}"
    )
    if funnel:
        ig += "\nGuía completa en el enlace del perfil."

    tt = (
        f"{short}: lo que casi nadie revisa.\n"
        f"El detalle está en la configuración, no en la herramienta.\n"
        f"keywords: {short} · seguridad · buenas prácticas\n"
        f"Comenta {cta} y te paso la checklist por DM.\n"
        f"— {marca}"
    )
    if funnel:
        tt += "\nGuía en el perfil."

    fb = (
        f"En las imágenes: una guía breve sobre {short}. "
        f"El post recorre la definición, el error más común y una checklist "
        f"de cuatro puntos para aplicarla hoy.\n"
        f"Este carrusel está pensado para quien necesita resolver esto sin "
        f"perder una tarde entera en documentación dispersa.\n"
        f"Si te resultó útil, compártelo con tu equipo.\n"
        f"— {marca}"
    )

    story = short.upper()[:60]

    bloques = [
        ("Instagram", ig, PRESUPUESTO["Instagram"]),
        ("TikTok", tt, PRESUPUESTO["TikTok"]),
        ("Facebook", fb, PRESUPUESTO["Facebook"]),
    ]

    filas = []
    problemas = []
    for nombre, texto, (minimo, maximo) in bloques:
        palabras = contar_palabras(texto)
        ok = minimo <= palabras <= maximo
        estado = "OK" if ok else "FUERA DE RANGO"
        if not ok:
            problemas.append(f"{nombre}: {palabras} palabras (esperado "
                             f"{minimo}-{maximo})")
        filas.append(f"| {nombre} | {palabras} | {estado} |")

    # QA de dialecto y responsabilidad sobre TODO el copy
    todo = " ".join(t for _, t, _ in bloques)
    dia_ok = (not voseo_presente(todo)
              and not regionalismos_presentes(todo)
              and not rituales_presentes(todo))
    resp = contenido_responsable(todo)
    pct = datos_inventados(todo)

    md = [
        f"# Copy para redes — {display}",
        "",
        f"- Slug: `{slug}`",
        f"- Palabra CTA (misma que el Slide N): **{cta}**",
        f"- Dialecto: tuteo-latam-neutro",
        "",
        "## QA",
        "",
        "| Plataforma | Palabras | Estado |",
        "|---|---|---|",
        *filas,
        "",
        f"- Voseo: {0 if not voseo_presente(todo) else 'DETECTADO'}",
        f"- Regionalismos: {len(regionalismos_presentes(todo))}",
        f"- Rituales culturales: {len(rituales_presentes(todo))}",
        f"- Contenido responsable: {'OK' if not resp else 'REVISAR: ' + ', '.join(resp)}",
        f"- Cifras a verificar: {', '.join(pct) if pct else 'ninguna'}",
        "",
        "## Instagram",
        "",
        ig,
        "",
        "## TikTok",
        "",
        tt,
        "",
        "## Facebook",
        "",
        fb,
        "",
        "## Story (titular en mayúsculas)",
        "",
        story,
        "",
        "## Primer comentario sugerido",
        "",
        f"Fijá este comentario: «La checklist completa está en el carrusel. "
        f"Comenta {cta} y la mando por DM.»",
        "",
        "## Hashtags recomendados",
        "",
        _hashtags_con_emojis(short, display, slug),
        "",
    ]
    (carpeta / "copy-redes.md").write_text("\n".join(md), encoding="utf-8")
    print(f"  OK copy-redes.md  ·  CTA {cta}")
    if problemas:
        print("  ! Presupuesto de palabras:")
        for p in problemas:
            print(f"    - {p}")
    if not dia_ok:
        print("  ! QA de dialecto: revisar voseo/regionalismos/rituales.")
    if resp:
        print(f"  ! Contenido responsable: {resp}")


# ── main ───────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tema", help="Slug del tema (modo generación de slides)")
    ap.add_argument("--carpeta", help="Slug existente (modo copy-redes.md)")
    ap.add_argument("--slides", type=int, help="Cantidad de slides (obligatorio "
                                               "en modo generación)")
    ap.add_argument("--vertical", default="cybersec",
                    choices=list(BANCOS))
    ap.add_argument("--color", default=None,
                    help="#RRGGBB (sólo para validarlo antes de escribir)")
    ap.add_argument("--display-tema", default=None)
    ap.add_argument("--short-tema", default=None)
    ap.add_argument("--marca", default=MARCA_DEFECTO)
    ap.add_argument("--funnel", action="store_true")
    args = ap.parse_args()

    ct = resolver_ctslider()

    if args.carpeta:
        carpeta = ct / args.carpeta
        if not carpeta.is_dir():
            sys.exit(f"No existe la carpeta: {carpeta}")
        display = args.display_tema or args.carpeta.replace("-", " ").title()
        short = args.short_tema or display
        generar_copy_redes(carpeta, display, short, funnel=args.funnel)
        return

    if not args.tema:
        sys.exit("Falta --tema (slides) o --carpeta (copy-redes).")
    if not args.slides or args.slides < 3:
        sys.exit("--slides mínimo 3 (obligatorio en modo generación).")
    resalte = None
    if args.color:
        from theme import colors
        try:
            resalte = colors.normalizar_hex(args.color)
        except ValueError as e:
            sys.exit(str(e))

    slug = slugificar(args.tema)
    display = args.display_tema or args.tema.replace("-", " ").title()
    short = args.short_tema or " ".join(_palabras(display)[:4])

    carpeta = ct / slug
    carpeta.mkdir(parents=True, exist_ok=True)

    slides, textos, hook = generar_slides(
        slug, args.slides, args.vertical, display, short, args.marca)

    # QA previo
    infracciones, dialecto = [], 0
    for t in textos:
        infracciones += contenido_responsable(t)
        if voseo_presente(t):
            dialecto += 1
        if regionalismos_presentes(t) or rituales_presentes(t):
            dialecto += 1

    for numero, contenido in slides:
        pie = f"{args.marca} · {short}"
        path = carpeta / f"slide-{numero:02d}.html"
        path.write_text(
            _slide_html(f"{numero}/{args.slides}", contenido, pie,
                        resalte=resalte),
            encoding="utf-8")
        print(f"  OK slide-{numero:02d}.html")

    # story-fuente.html (opcional, el builder la renderiza)
    story = _slide_html(
        "1/1",
        f'      <div class="titulo">'
        f'{_marcar_clave(short, candidata=short.split()[0] if short else None)}'
        f"</div>",
        args.marca, resalte=resalte)
    (carpeta / "story-fuente.html").write_text(story, encoding="utf-8")
    print("  OK story-fuente.html")

    cta = resolver_cta_palabra(slug)
    print(f"\n  QA · Dialecto tuteo-latam-neutro | Infracciones dialecto: "
          f"{dialecto} | Responsable: "
          f"{'OK' if not infracciones else 'REVISAR ' + str(infracciones)}")
    print(f"  CTA: {cta}  ·  Hook: {hook}")
    print(f"  Carpeta: {carpeta}")
    print(f"\n  Siguiente paso: tech_carousel.py --tema {slug} "
          f"--color \"{'#RRGGBB' if not args.color else args.color}\" "
          f"--slides {args.slides} --vertical {args.vertical}")


if __name__ == "__main__":
    main()
