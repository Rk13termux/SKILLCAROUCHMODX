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

MARCA_DEFECTO = "CHMODX"


def _landing_dominio(url):
    """'https://chmodxcode.pro/' → 'chmodxcode.pro' (mismo criterio que builder)."""
    d = (url or "").strip()
    for pre in ("https://", "http://", "www."):
        if d.lower().startswith(pre):
            d = d[len(pre):]
    return d.rstrip("/") or (url or "").strip()


def _con_utm(url, red, campana=""):
    """Enlace con UTM para medir de qué red viene el tráfico a la landing."""
    if not url:
        return ""
    base = url.strip()
    sep = "&" if "?" in base else "?"
    q = f"utm_source={red}&utm_medium=carrusel"
    if campana:
        q += f"&utm_campaign={campana}"
    return f"{base}{sep}{q}"

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


def _norm_comp(tipo):
    """Nombre canonico de componente (resuelve alias)."""
    clave = (tipo or "").lower().strip()
    try:
        from components.base import ALIAS
        return ALIAS.get(clave, clave)
    except Exception:
        return clave


def generar_slides(tema_slug, n, vertical, display, short, marca,
                   permitidos=None):
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
    # Portada con gancho visual: 1 componente del banco (HOOK_COMPS) que
    # el builder conserva tras título/subtítulo. Determinista por slug.
    hook_comps = getattr(banco, "HOOK_COMPS", ())
    if hook_comps:
        hc = _elegir(tuple(hook_comps), tema_slug)
        hc_props = _plantilla_props(hc.get("props", {}), display, short)
        cover += (
            '\n      <div class="componente" '
            f'data-component="{hc.get("tipo", "terminal")}" '
            f"data-props='{json.dumps(hc_props, ensure_ascii=False)}'></div>"
        )
    slides_html.append((1, cover))
    textos.append(f"{hook} {subhook}")

    if permitidos is not None:
        permitidos = {_norm_comp(c) for c in permitidos}
        # Preset primero: bloques con componente de la whitelist abren
        # el carrusel (orden estable, determinista).
        cobertura = tuple(sorted(
            cobertura,
            key=lambda b: 0 if (b.get("componente") and _norm_comp(
                b["componente"].get("tipo")) in permitidos) else 1))
    ultimo_componente = None
    for i in range(2, n - 1):  # slides 2 .. N-2 (contenido)
        bloque = cobertura[(i - 2) % len(cobertura)]
        # No repetir componente consecutivo al ciclar el banco
        comp = bloque["componente"]
        if comp and comp["tipo"] == ultimo_componente:
            comp = None
        if comp and permitidos is not None:
            if _norm_comp(comp.get("tipo")) not in permitidos:
                comp = None  # preset: fuera de la whitelist
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
        'hermes': ['🤖', '#hermes', '#hermesagent', '#nousresearch', '#ai'],
        'agent': ['🤖', '#aiagent', '#agents', '#automatizacion'],
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


"""Helpers nuevos de copy-redes: SEO, tags, comandos y primer comentario."""


_EMOJI_VERTICAL = {
    "cybersec": "🔒", "prog": "💻", "programming": "💻", "dev": "💻",
    "ai": "🤖", "ia": "🤖", "infra": "🚀", "devops": "🚀", "tech": "💡",
}

_TAGS_VERTICAL = {
    "cybersec": ["#cybersec", "#seguridad", "#infosec"],
    "prog": ["#programacion", "#codigo", "#dev"],
    "programming": ["#programacion", "#codigo", "#dev"],
    "dev": ["#programacion", "#codigo", "#dev"],
    "ai": ["#ia", "#ai", "#llm"],
    "ia": ["#ia", "#ai", "#llm"],
    "infra": ["#devops", "#infraestructura", "#linux"],
    "devops": ["#devops", "#infraestructura", "#linux"],
    "tech": ["#tech", "#tutorial"],
}

_STOP_SEO = {
    "de", "la", "el", "los", "las", "una", "unos", "unas", "este", "esta",
    "estos", "estas", "para", "como", "con", "por", "sin", "sobre", "entre",
    "que", "los", "del", "al", "una", "más", "muy", "todo", "toda", "este",
    "guia", "guía", "instalacion", "instalación", "introduccion", "curso",
}


def _seo_keywords(display, short, slug, tope=5):
    """Palabras clave significativas para títulos, descripciones y tags."""
    import unicodedata
    vistas = []
    for fuente in (display or "", short or "", (slug or "").replace("-", " ")):
        for w in re.findall(r"[A-Za-zÁÉÍÓÚáéíóúÑñ]{4,}", fuente):
            norm = "".join(c for c in unicodedata.normalize("NFKD", w.lower())
                           if not unicodedata.combining(c))
            if norm not in _STOP_SEO and norm not in vistas:
                vistas.append(norm)
    # Primero las del short (más específicas), luego display/slug
    cortas = [w for w in re.findall(r"[A-Za-zÁÉÍÓÚáéíóúÑñ]{4,}", short or "")]
    cortas = ["".join(c for c in unicodedata.normalize("NFKD", w.lower())
                      if not unicodedata.combining(c)) for w in cortas]
    orden = [w for w in cortas if w in vistas]
    orden += [w for w in vistas if w not in orden]
    return orden[:tope]


def _tagify(palabra):
    limpio = re.sub(r"[^a-z0-9]", "", (palabra or "").lower())
    return f"#{limpio}" if limpio else ""


def _tags(cantidad, kws, vertical, slug):
    """Hashtags exactos y deterministas: keywords + vertical + marca."""
    tags = []
    for kw in (kws or []):
        t = _tagify(kw)
        if t and t not in tags:
            tags.append(t)
    for t in _TAGS_VERTICAL.get((vertical or "tech").lower(), ["#tech"]):
        if t not in tags:
            tags.append(t)
    for t in ("#chmodx", "#tutorial", "#aprende", "#guia", "#tips",
              "#tech"):
        if len(tags) >= cantidad:
            break
        if t not in tags:
            tags.append(t)
    return " ".join(tags[:cantidad])


def extraer_comandos(carpeta, tope=12):
    """Comandos `cmd` de los terminales fuente, únicos y en orden."""
    cmds = []
    for p in sorted(Path(carpeta).glob("slide-*.html")):
        try:
            texto = p.read_text(encoding="utf-8")
        except OSError:
            continue
        for m in re.finditer(r'\{"t":\s*"cmd",\s*"v":\s*"((?:[^"\\]|\\.)*)"\}',
                             texto):
            cmd = m.group(1).replace('\\"', '"').replace("\\n", " ").strip()
            if cmd and cmd not in cmds:
                cmds.append(cmd)
            if len(cmds) >= tope:
                return cmds
    return cmds


def _primer_comentario(short, cta, comandos, repo, marca,
                       cierre=None, landing=None, landing2=None,
                       landing2_texto=None, campana=""):
    lineas = []
    if landing:
        lineas.append(f"🚀 Primero: {_con_utm(landing, 'instagram', campana)}")
        linea2 = ""
        if landing2:
            txt2 = (landing2_texto or "Telegram").strip()
            linea2 = f" · {txt2}: {_con_utm(landing2, 'instagram', campana)}"
        lineas += [
            "Curso de Python completo + canal de Telegram para resolver "
            "dudas en comunidad." + linea2,
            "",
        ]
    lineas += [
        f"📌 Comandos de «{short}» — cópialos y úsalos:",
        "",
    ]
    if comandos:
        lineas.append("```")
        lineas.extend(comandos)
        lineas.append("```")
        lineas.append("")
    else:
        lineas.append("Todos los comandos están en las imágenes del carrusel.")
        lineas.append("")
    if repo:
        lineas.append(f"🔗 Repo oficial: {repo}")
        lineas.append("")
    lineas += [cierre or f"Comenta {cta} y te paso la checklist completa."]
    return "\n".join(lineas)


def generar_copy_redes(carpeta: Path, display, short, marca=None, funnel=False,
                       cta_palabra=None, repo=None, vertical="tech", cta_modo="seguir",
                       landing=None, landing2=None, landing2_texto=None):
    slug = carpeta.name
    cta = resolver_cta_palabra(slug, forzado=cta_palabra)
    marca = (marca or MARCA_DEFECTO).strip() or MARCA_DEFECTO
    dom = _landing_dominio(landing) if landing else ""
    dom2 = _landing_dominio(landing2) if landing2 else ""
    txt2 = (landing2_texto or "Telegram").strip()
    emo = _EMOJI_VERTICAL.get((vertical or "tech").lower(), "💡")
    kws = _seo_keywords(display, short, slug)
    kw1 = (kws[0] if len(kws) > 0 else short).capitalize()
    kw2 = (kws[1] if len(kws) > 1 else "guía práctica").capitalize()
    kw3 = kws[2] if len(kws) > 2 else "paso a paso"
    comandos = extraer_comandos(carpeta)
    seguir = (cta_modo or "comentar") == "seguir"
    if seguir:
        linea_cta_ig = ("Síguenos para no perderte la próxima guía: cada "
                        "semana un tema así, sin humo.")
        linea_cta_tt = "Síguenos: cada semana una guía así."
        cierre_comentario = (f"💬 Síguenos y dime qué tema quieres ver "
                             f"después. — {marca}")
    else:
        linea_cta_ig = f"Comenta {cta} y te paso la checklist completa."
        linea_cta_tt = f"Comenta {cta} y te mando la checklist."
        cierre_comentario = (f"💬 ¿Qué te pareció el post? Cuéntame qué tema "
                             f"quieres ver después.\n"
                             f"Comenta {cta} y te paso la checklist completa. "
                             f"— {marca}")
    if dom:
        # Landing primero: gana jerarquía sobre el CTA genérico.
        linea_landing_ig = (f"Empieza en {dom}: curso de Python completo y "
                            "canal de Telegram para resolver dudas.")
        linea_landing_tt = f"Empieza en {dom} — curso y Telegram."
        linea_landing_fb = (f"Empieza en {dom}: curso de Python completo y "
                            "canal de Telegram.")
        if dom2:
            linea_landing_ig = (f"Empieza en {dom}: curso de Python completo. "
                                f"{txt2}: {dom2}.")
            linea_landing_tt = f"Empieza en {dom} — curso y {txt2}."
            linea_landing_fb = (f"Empieza en {dom}: curso de Python completo. "
                                f"{txt2}: {dom2}.")
        linea_cta_ig = f"{linea_landing_ig} {linea_cta_ig}"
        linea_cta_tt = f"{linea_landing_tt} {linea_cta_tt}"
        # El primer comentario ya abre con la landing: el cierre no la repite.

    ig_titulo = f"{emo} {short} sin humo: guía completa"
    ig_desc = (
        f"{emo} {display}: guía completa en un carrusel.\n"
        f"Comandos reales, errores típicos y checklist aplicable hoy. ✨\n"
        f"Ideal para devs, estudiantes y curiosos de {kw2}.\n"
        f"Si trabajas con {kw1}, guarda este post: vuelve a servirte cuando "
        f"lo necesites. 📌\n"
        f"Compártelo con tu equipo. 💬 ¿Qué punto aplicas primero?\n"
        f"{linea_cta_ig}\n"
        f"— {marca}"
    )
    if funnel:
        ig_desc += "\nGuía completa en el enlace del perfil."

    tt_titulo = f"{emo} {short} en 30 segundos"
    tt_desc = (
        f"{emo} {kw1} explicado rápido: {kw2} y {kw3} sin rodeos.\n"
        f"Mira el carrusel completo en IG. 💬\n"
        f"Guarda y comparte con quien programa.\n"
        f"{linea_cta_tt}\n"
        f"— {marca}"
    )
    if funnel:
        tt_desc += "\nGuía en el perfil."

    fb_titulo = f"{emo} Guía completa: {short}"
    fb_desc = (
        f"{emo} En las imágenes: {display}, explicado {kw3}.\n"
        f"El post recorre {kw1}, el error más común con {kw2} y una checklist "
        f"de cuatro puntos para aplicarla hoy mismo. ✨\n"
        f"Pensado para quien necesita resolver esto sin perder una tarde en "
        f"documentación dispersa. Si te sirve, compártelo con tu equipo. 📌\n"
        + (f"{linea_landing_fb}\n" if dom else "") +
        f"💬 Cuéntame en comentarios qué te pareció y qué tema sigue.\n"
        f"— {marca}"
    )

    story = f"{emo} {short.upper()[:54]}"

    bloques = [
        ("Instagram", ig_desc, PRESUPUESTO["Instagram"]),
        ("TikTok", tt_desc, PRESUPUESTO["TikTok"]),
        ("Facebook", fb_desc, PRESUPUESTO["Facebook"]),
    ]

    filas = []
    problemas = []
    for nombre, texto, (minimo, maximo) in bloques:
        palabras = contar_palabras(texto)
        ok = minimo <= palabras <= maximo
        estado = "OK" if ok else "FUERA DE RANGO"
        if not ok:
            problemas.append(f"{nombre}: {palabras} palabras (esperado "
                             f"{minimo}-{maximo}")
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
        f"- Keywords SEO: {', '.join(kws) if kws else short}",
        f"- Dialecto: tuteo-latam-neutro",
        *([f"- Landing: {landing}"] if dom else []),
        *([f"- Landing 2: {landing2}"] if dom2 else []),
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
        "## Instagram 📸 — título + descripción + 9 hashtags",
        "",
        f"**Título:** {ig_titulo}",
        "",
        "**Descripción:**",
        "",
        ig_desc,
        "",
        f"**Hashtags:** {_tags(9, kws, vertical, slug)}",
        "",
        "## TikTok 🎵 — título + descripción + 5 hashtags",
        "",
        f"**Título:** {tt_titulo}",
        "",
        "**Descripción:**",
        "",
        tt_desc,
        "",
        f"**Hashtags:** {_tags(5, kws, vertical, slug)}",
        "",
        "## Facebook 📘 — título + descripción + 5 hashtags",
        "",
        f"**Título:** {fb_titulo}",
        "",
        "**Descripción:**",
        "",
        fb_desc,
        "",
        f"**Hashtags:** {_tags(5, kws, vertical, slug)}",
        "",
        "## Story (titular en mayúsculas)",
        "",
        story,
        "",
        "## 📌 Primer comentario (fíjalo)",
        "",
        _primer_comentario(short, cta, comandos, repo, marca,
                           cierre=cierre_comentario, landing=landing,
                           landing2=landing2, landing2_texto=landing2_texto,
                           campana=slug),
        "",
        *(["## 🔗 Enlaces con UTM (bio / story / comentario)", "",
           "Copia el que corresponda a cada red para medir de dónde viene "
           "el tráfico:",
           "",
           f"- Instagram: {_con_utm(landing, 'instagram', slug)}",
           *([f"- Telegram (IG): {_con_utm(landing2, 'instagram', slug)}"]
             if dom2 else []),
           f"- TikTok: {_con_utm(landing, 'tiktok', slug)}",
           f"- Facebook: {_con_utm(landing, 'facebook', slug)}",
           ""] if dom else []),
        "## 📅 Plan de publicación sugerido",
        "",
        "- **Día 1 (lanzamiento) · 19:00–21:00:** publica en Instagram (feed) y "
        "comparte la story con sticker de enlace. Fija el primer comentario con "
        "los comandos.",
        "- **Día 1 · 21:30:** sube el mismo carrusel a TikTok con el copy corto "
        "(la landing va en la bio).",
        "- **Día 2 · 12:00–13:00:** Facebook (mejor alcance a mediodía). "
        "Enlaza con UTM de Facebook.",
        "- **Día 4:** republica la story con la diapositiva del CTA final y "
        "responde dudas en comentarios (sube el alcance).",
        "- **Día 7:** repostea la portada como reel corto si el post superó "
        "el promedio de guardados.",
        "",
        "> Ajustá las horas a la analítica de tu cuenta (revisá ``Insights → "
        "Público → Horas más activas``).",
        "",
        "## Hashtags recomendados (todas las redes)",
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
    ap.add_argument("--repo", default=None)
    ap.add_argument("--landing", default=None,
                    help="URL propia (ej: https://chmodxcode.pro): se coloca "
                         "primero en descripciones y primer comentario")
    ap.add_argument("--landing2", default=None,
                    help="Segunda URL del cierre (ej: canal de Telegram)")
    ap.add_argument("--landing2-texto", default=None,
                    help="Texto que acompaña a la segunda URL")
    ap.add_argument("--cta-palabra", default=None)
    args = ap.parse_args()

    ct = resolver_ctslider()

    if args.carpeta:
        carpeta = ct / args.carpeta
        if not carpeta.is_dir():
            sys.exit(f"No existe la carpeta: {carpeta}")
        display = args.display_tema or args.carpeta.replace("-", " ").title()
        short = args.short_tema or display
        generar_copy_redes(carpeta, display, short, funnel=args.funnel,
                           cta_palabra=args.cta_palabra, repo=args.repo,
                           vertical=args.vertical, landing=args.landing,
                           landing2=args.landing2,
                           landing2_texto=args.landing2_texto)
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
