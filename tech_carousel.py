#!/usr/bin/env python3
"""
tech_carousel.py — TechEdu carousel builder (ciberseguridad · programación · IA).

Construye los HTML finales (isotipo tintado, badge, barra de progreso, ícono
de categoría, componentes gráficos, CTA) y renderiza los PNG con chromium
headless UNO A LA VEZ (un loop produce páginas en blanco). También genera
caption.txt y la story teaser.

Uso (un solo comando, de cero a PNG):

  python3 tech_carousel.py \
    --tema <carpeta_fuente> \
    --color "#RRGGBB" \
    --slides 8 \
    [--formato 9:16|3:4|4:5|1:1] \
    [--vertical auto|cybersec|prog|ai|infra] \
    [--iconos auto|<categoria>] [--componentes auto|a,b,c] \
    [--display-tema "..."] [--short-tema "..."] \
    [--badge "..."] [--cta-palabra "..."] [--hashtags "a,b,c"] \
    [--marca TechEdu] [--resalte "#RRGGBB"] \
    [--copy-redes] [--offline] [--solo-story] [--no-auto]

Si la carpeta no tiene slide-*.html, el mismo comando escribe el copy con el
banco de la vertical y sigue (quitá eso con --no-auto, que falla con aviso).

Salidas (en la carpeta fuente):
  renders/slide-NN.html · preview/slide-NN.png · stories/story-01.png
  caption.txt · copy-redes.md (con --copy-redes)
"""

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import time
import zlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

try:
    from PIL import Image
except ImportError:
    Image = None

from components import expandir
from icons import detectar_categoria, elegir_icono, icono_slide
from theme import colors as _colors
from theme import fondos as _fondos
from theme import fonts as _fonts
from theme import stars as _stars
from theme import tokens as _tokens
from copywriting.base import resolver_cta_palabra
from utils.render import resolver_chromium, resolver_ctslider

MARCA_DEFECTO = "CHMODX"

CTSLIDER = resolver_ctslider()
CHROMIUM = resolver_chromium()

FORMATOS = {
    "9:16": {"w": 1080, "h": 1920},
    "3:4": {"w": 1080, "h": 1440},
    "4:5": {"w": 1080, "h": 1350},
    "1:1": {"w": 1080, "h": 1080},
}

# ── Presets de tipo de post (brief → receta) ───────────────────────
# Cada preset fija vertical + whitelist de componentes para que el banco
# de copy solo use esos (en auto) y el builder avise si otro se cuela.

PRESETS = {
    "repo": {"vertical": "prog",
             "componentes": "card-repo,gh-stats,tree,code,terminal"},
    "comandos": {"vertical": "infra",
                 "componentes": "terminal,tabla,code,checklist,quiz"},
    "python": {"vertical": "prog",
               "componentes": "editor,code,terminal,diff,quiz"},
    "mixto": {"vertical": "auto", "componentes": "auto"},
}

# ── Chromium (con fallback de GPU) ─────────────────────────────────
# En algunos equipos el proceso GPU de Chromium crashea al arrancar
# ("GPU process isn't usable", rc=-6) y la corrida entera muere. Se corre
# siempre sin él; si la salida viene vacía, con error o sin el marcador
# esperado, se reintenta UNA vez con --in-process-gpu y a partir de ahí la
# bandera queda activa para no pagar dos corridas por slide.

_GPU_PROBLEMA = False


def _cmd_chromium(*args):
    global _GPU_PROBLEMA
    cmd = [CHROMIUM, "--headless", "--no-sandbox", "--disable-gpu"]
    if _GPU_PROBLEMA:
        cmd.append("--in-process-gpu")
    cmd.extend(args)
    return cmd


def _correr_chromium(cmd, espera=None, existe=None, cwd=None):
    """Ejecuta Chromium y reintenta con --in-process-GPU si no cumple."""
    global _GPU_PROBLEMA

    def cumple(r_ok, r_stdout, r_stderr, r_code):
        if r_code != 0:
            return False
        if existe is not None and not existe.exists():
            return False
        if espera is not None and not re.search(espera, r_stdout or ""):
            return False
        return True

    try:
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    except Exception:
        raise

    if cumple(r, r.stdout, r.stderr, r.returncode) or "--in-process-gpu" in cmd:
        return r
    _GPU_PROBLEMA = True
    cmd2 = list(cmd)
    if "--disable-gpu" in cmd2:
        cmd2.insert(cmd2.index("--disable-gpu") + 1, "--in-process-gpu")
    if existe is not None and existe.exists():
        try:
            existe.unlink()
        except OSError:
            pass
    return subprocess.run(cmd2, capture_output=True, text=True, cwd=cwd)


# ── Validación de props de componentes (fail-fast) ─────────────────

_RE_COMP_APERTURA = re.compile(r'<div\s+class="componente"([^>]*)>', re.S)
_RE_ATTR = re.compile(r'(\w[\w-]*)=(["\'])(.*?)\2', re.S)


def validar_props(html: str, nombre: str):
    """Valida el JSON de cada data-props antes de renderizar.

    Devuelve una lista de errores con slide y ubicación exacta; vacía si
    todo está bien. El renderizador tolera JSON roto (pinta un aviso en el
    slide), pero publicar con eso es peor que frenar acá.
    """
    errores = []
    for apertura in _RE_COMP_APERTURA.finditer(html):
        attrs = apertura.group(1)
        atributos = {m.group(1): m.group(3)
                     for m in _RE_ATTR.finditer(attrs)}
        txt = (atributos.get("data-props") or "").strip()
        if not txt:
            continue  # sin data-props: el JSON se lee del interior
        try:
            json.loads(txt)
        except json.JSONDecodeError as e:
            comp = atributos.get("data-component", "?")
            errores.append(
                f'{nombre}: JSON inválido en data-props del componente '
                f'"{comp}" (línea {e.lineno}, col {e.colno}): {e.msg}')
    return errores


def contar_claves(html: str):
    """Cuenta .clave aceptando comillas simples o dobles (B1)."""
    return len(_RE_CLAVE.findall(html))

# ── Derivación de marca (badge / hashtag / pie) ────────────────────

_STOPWORDS = {
    "de", "la", "el", "los", "las", "y", "a", "con", "para", "como", "en",
    "del", "al", "que", "lo", "un", "una", "tu", "su", "contra", "hacia",
    "por", "e", "o", "algun", "esta", "este", "te", "se", "no", "me", "mi",
    "nos", "les", "le", "yo", "eso",
}


def _palabras(texto):
    return re.findall(r"[A-Za-zÁÉÍÓÚáéíóúÑñ]+", texto or "")


def _palabra_clave(tema_texto, cantidad=1):
    palabras = _palabras(tema_texto)
    claves = [p for p in palabras if p.lower() not in _STOPWORDS] or palabras
    return " ".join(claves[:cantidad]).upper() if claves else ""


def _normalizar(palabra):
    import unicodedata
    return "".join(
        c for c in unicodedata.normalize("NFD", palabra.lower())
        if unicodedata.category(c) != "Mn"
    )


def _hashtags_tema(tema_texto, marca, maximo=5):
    hashtags, vistos = [], set()
    for p in _palabras(tema_texto):
        norm = _normalizar(p)
        if norm in _STOPWORDS or norm in vistos:
            continue
        vistos.add(norm)
        hashtags.append(f"#{norm}")
        if len(hashtags) >= maximo:
            break
    hashtags.append(f"#{_normalizar(marca).replace(' ', '')}")
    return " ".join(hashtags)


def _indice_estable(semilla, modulo):
    """Índice determinista (crc32): misma entrada → misma elección."""
    if modulo <= 0:
        return 0
    return zlib.crc32(_normalizar(semilla).encode("utf-8")) % modulo


# ── Isotipo tintado ────────────────────────────────────────────────

def _tint_logo(hex_color: str):
    if Image is None:
        return None
    logo = CTSLIDER / "logo.png"
    if not logo.is_file():
        alt = SKILL_DIR / "logo.png"
        if alt.is_file():
            logo = alt
        else:
            print(f"  ! No hay logo.png en {CTSLIDER} ni junto al script: "
                  "los slides salen sin isotipo.")
            return None
    try:
        src = Image.open(str(logo)).convert("RGBA")
    except Exception as e:  # noqa: BLE001
        print(f"  ! No se pudo abrir logo.png ({e}): los slides salen sin isotipo.")
        return None
    w, h = src.size
    accent = tuple(int(hex_color.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    px = src.load()
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    opx = out.load()

    def curva(lum: float) -> float:
        if lum <= 0.04:
            return max(0.0, lum * 6.0)
        t = (min(lum, 1.0) - 0.04) / 0.96
        return 0.55 + 0.45 * (t ** 0.5)

    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
            m = curva(lum) * (a / 255.0)
            opx[x, y] = (accent[0], accent[1], accent[2], int(round(m * 255)))
    buf = Path("/tmp/techedu_tint.png")
    out.save(str(buf))
    b64 = base64.b64encode(buf.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{b64}"


# ── Parseo de fuente (contrato HTML intacto) ───────────────────────

def parse_slide(filepath: Path):
    html = filepath.read_text(encoding="utf-8")

    num_match = re.search(r'<div class="numero">(\d+/\d+)</div>', html)
    number = num_match.group(1) if num_match else "1/7"

    body_match = re.search(
        r'<div class="contenido">\s*(.*?)\s*</div>\s*<div class="pie">',
        html, re.DOTALL)
    body = body_match.group(1).strip() if body_match else ""

    icono = ""
    m = re.search(r'<div class="icono">(.*?)</div>', body, re.DOTALL)
    if m:
        icono = m.group(1).strip()
        body = body.replace(m.group(0), "")

    for patron in (
        r'<div class="cover"></div>',
        r'<div class="number"></div>',
        r'<div class="cta-final"></div>',
    ):
        body = re.sub(patron, "", body, flags=re.DOTALL)
    body = re.sub(r"<!--P\.IRR-->", "", body)
    body = re.sub(r"\s+", " ", body).strip()

    footer_match = re.search(
        r'<span class="logo"></span>\s*(.*?)\s*</div>\s*</div>\s*</body>',
        html, re.DOTALL)
    footer = footer_match.group(1).strip() if footer_match else ""

    return {"number": number, "body": body, "footer": footer, "icono": icono}


# ── Template base ──────────────────────────────────────────────────

TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>__marca__</title>
__links_fuentes__
<style>
  :root {
    --negro: #0B0B0D;
    --negro-suave: #141417;
    --borde: #26262B;
    --gris: #8E8E93;
    --gris-oscuro: #57575F;
    --blanco: #FFFFFF;
    --acento: __accent__;
    --acento-brillo: __accent_bright__;
    --acento-rgba-b: __accent_rgba_b__;
    --acento-rgba-30: __accent_rgba_30__;
    --acento-rgba-40: __accent_rgba_40__;
    --resalte: __resalte__;
    --resalte-brillo: __resalte_brillo__;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  html, body { overflow: hidden; height: 100%; }
  ::-webkit-scrollbar { display: none; }
  body {
    font-family: __font_display__;
    background: var(--negro);
    color: var(--blanco);
    -webkit-font-smoothing: antialiased;
  }
  .slide {
    width: __slide_w__px;
    height: __slide_h__px;
    padding: __pad_top__px __pad_lr__px __pad_bottom__px __pad_lr__px;
    display: flex;
    flex-direction: column;
    position: relative;
    overflow: hidden;
    isolation: isolate;  /* el código fantasma usa z-index negativo */
  }
  .slide::before {
    content: "";
    position: absolute;
    inset: 0;
    background-image: __fondo_img__;
    pointer-events: none;
  }
  /* Textura del fondo (grid / circuitos / nodos / topología / puntos / beams):
     va enmascarada para desvanecerse hacia los bordes y no competir con el texto. */
  .slide::after {
    content: "";
    position: absolute;
    inset: 0;
    background-image: __textura_img__;
    background-size: __textura_size__;
    -webkit-mask-image: __textura_mask__;
    mask-image: __textura_mask__;
    opacity: __textura_op__;
    pointer-events: none;
  }
  /* Código fantasma: los comandos reales del carrusel, casi imperceptibles. */
  .slide > .fondo-codigo {
    position: absolute;
    inset: 0;
    z-index: -1;
    padding: 120px 86px;
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 25px;
    line-height: 2.05;
    color: var(--blanco);
    opacity: 0.05;
    overflow: hidden;
    pointer-events: none;
  }
  .slide > .fondo-codigo .ln {
    color: var(--acento);
    opacity: 0.75;
    margin-right: 20px;
  }
  .slide > * { position: relative; z-index: 1; }

  .encabezado { display: flex; align-items: center; gap: 26px; }
  .marca { position: relative; }
  .marca .isotipo {
    width: __logo_size__px;
    height: auto;
    object-fit: contain;
    filter: drop-shadow(0 0 16px var(--acento-rgba-30));
  }
  .numero {
    margin-left: auto;
    font-weight: 600;
    font-size: __num_size__px;
    color: var(--acento);
    border: 2px solid var(--acento-rgba-40);
    border-radius: 50%;
    width: __num_box__px;
    height: __num_box__px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 18px var(--acento-rgba-30);
    flex: 0 0 auto;
  }
  .progreso {
    margin-top: __prog_margin__px;
    height: __prog_h__px;
    background: var(--negro-suave);
    border: 1px solid var(--borde);
    border-radius: 60px;
    overflow: hidden;
  }
  .progreso .relleno {
    width: __progreso_pct__%;
    height: 100%;
    border-radius: 60px;
    background: linear-gradient(90deg, var(--acento), var(--acento-brillo));
    box-shadow: 0 0 14px var(--acento-rgba-40);
  }

  .contenido {
    display: flex;
    flex-direction: column;
    justify-content: center;
    flex: 1;
    min-height: 0;
  }
  /* El wrapper del auto-fit reproduce el flex column de .contenido: sin esto,
     los hijos con align-self:center (.badge, .cta, .ind-swipe, .secundario)
     quedan pegados a la izquierda. */
  .ajuste { width: 100%; display: flex; flex-direction: column; zoom: __contenido_zoom__; /* AJUSTE_ZOOM */ }
  /* Placa duotono: el glyph vive dentro de una placa con acento y glow.
     Ocupa el mismo __icon_size__, así que no altera el layout ni el auto-fit. */
  .icono-box { display: flex; justify-content: center; margin-bottom: __icon_margin__px; }
  .icono-box .icono-svg {
    width: __icon_size__px;
    height: __icon_size__px;
    padding: calc(__icon_size__px * 0.18);
    border-radius: 28%;
    background:
      radial-gradient(circle at 50% 32%, var(--acento-rgba-40), transparent 62%),
      linear-gradient(150deg, rgba(255, 255, 255, 0.09), rgba(0, 0, 0, 0.32));
    border: 2px solid var(--acento-rgba-40);
    box-shadow:
      inset 0 1px 0 rgba(255, 255, 255, 0.10),
      inset 0 -14px 28px rgba(0, 0, 0, 0.30),
      0 20px 50px rgba(0, 0, 0, 0.55),
      0 0 70px var(--acento-rgba-30);
    filter:
      drop-shadow(0 0 10px var(--acento-rgba-40))
      drop-shadow(0 0 30px var(--acento-rgba-30));
  }
  /* Modo clásico (sin placa): --sin-placa agrega .plano al <body>. */
  body.plano .icono-box .icono-svg {
    padding: 0;
    border: 0;
    border-radius: 0;
    background: none;
    box-shadow: none;
    filter: drop-shadow(0 12px 30px rgba(0, 0, 0, 0.45))
            drop-shadow(0 0 26px var(--acento-rgba-40));
  }
  .titulo {
    font-weight: 800;
    font-size: __title_size__px;
    line-height: 1.12;
    margin-bottom: __title_margin__px;
    text-align: center;
    text-shadow: 0 0 44px var(--acento-rgba-30), 0 0 88px var(--acento-rgba-b);
  }
  .cuerpo {
    font-weight: 400;
    font-size: __body_size__px;
    line-height: 1.42;
    color: var(--blanco);
    text-align: center;
  }
  .titulo .clave,
  .cuerpo .clave {
    color: var(--resalte);
    font-weight: 800;
    font-size: 1.15em;
    text-shadow: 0 0 27px __resalte_rgba32__, 0 2px 6px rgba(0, 0, 0, 0.55);
  }
  .cuerpo .gris { color: var(--gris); }
  .cuerpo .dato { display: inline; font-weight: 700; color: var(--acento); }
  .cuerpo .cita { font-style: italic; }
  .cuerpo .resaltar { font-weight: 700; }

  .badge {
    display: inline-block;
    align-self: center;
    margin-bottom: __badge_margin__px;
    padding: __badge_pad_v__px __badge_pad_h__px;
    border-radius: 60px;
    font-weight: 700;
    font-size: __badge_size__px;
    letter-spacing: 3px;
    color: var(--negro);
    background: linear-gradient(135deg, var(--acento), var(--acento-brillo));
    box-shadow: 0 0 24px var(--acento-rgba-40);
  }

  .cta {
    align-self: center;
    display: inline-flex;
    align-items: center;
    gap: 14px;
    margin-top: __cta_margin__px;
    font-weight: 700;
    font-size: __cta_size__px;
    color: var(--negro);
    background: linear-gradient(135deg, var(--acento), var(--acento-brillo));
    box-shadow: 0 0 34px var(--acento-rgba-40), 0 8px 24px rgba(0,0,0,0.35);
    border-radius: 60px;
    padding: __cta_pad_v__px __cta_pad_h__px;
    white-space: nowrap;
  }

  .secundario {
    margin-top: __sec_margin__px;
    font-size: __sec_size__px;
    color: var(--gris);
    text-align: center;
  }
  .secundario::before {
    content: "";
    display: block;
    width: 220px;
    height: 1px;
    margin: 0 auto 26px auto;
    background: linear-gradient(90deg, transparent, var(--gris-oscuro), transparent);
  }

  .ind-swipe {
    align-self: center;
    display: __ind_disp__;
    align-items: center;
    justify-content: center;
    gap: 14px;
    min-height: __ind_h__px;
    margin-top: __ind_margin__px;
    padding: 18px 32px;
    border: 2px solid var(--acento-rgba-40);
    border-radius: 60px;
    background: linear-gradient(180deg, rgba(255,255,255,0.07), rgba(255,255,255,0.02));
    font-weight: 600;
    font-size: __ind_size__px;
    letter-spacing: 0.4px;
    color: #DCDCE2;
    text-align: center;
    box-shadow: 0 10px 28px rgba(0, 0, 0, 0.45);
  }
  .ind-swipe .flecha {
    color: var(--acento-brillo);
    font-weight: 700;
    text-shadow: 0 0 14px var(--acento-rgba-40);
  }

  .pie {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 14px;
    font-size: __footer_size__px;
    font-weight: 500;
    color: var(--gris);
    border-top: 2px solid var(--borde);
    padding: __pie_pad_v__px __pad_lr__px __pie_pad_b__px __pad_lr__px;
  }
  .pie .isotipo {
    width: __footer_logo__px;
    height: auto;
    object-fit: contain;
    opacity: 0.92;
  }

  .slide.puente .contenido { align-items: center; text-align: center; }
  .slide.puente .cuerpo { max-width: 880px; margin: 0 auto; }
  .slide.final-cta .contenido { align-items: center; text-align: center; }
  .slide.final-cta .cuerpo { max-width: 880px; }
  .slide.final-cta .cta .clave {
    color: #0F0F10;
    font-weight: 800;
    font-size: 1em;
    text-shadow: none;
    border-bottom: 3px solid rgba(15, 15, 16, 0.45);
  }
  .slide.final-cta .cta {
    display: inline-block;
    margin-left: auto;
    margin-right: auto;
    max-width: 860px;
    padding: 26px 44px;
    line-height: 1.34;
    text-align: center;
    white-space: normal;
    background: linear-gradient(135deg, var(--resalte), var(--resalte-brillo));
    color: #0F0F10;
    box-shadow: 0 0 34px __resalte_rgba38__, 0 8px 24px rgba(0, 0, 0, 0.35);
  }
  .slide.final-cta .secundario {
    margin-top: __sec_margin__px;
    font-size: __sec_size__px;
    color: var(--gris);
    text-align: center;
    line-height: 1.38;
    max-width: 820px;
  }
  .slide.final-cta .cta-seguir {
    display: inline-block;
    margin-left: auto;
    margin-right: auto;
    margin-top: 28px;
    max-width: 860px;
    padding: 26px 44px;
    line-height: 1.34;
    text-align: center;
    white-space: normal;
    background: #000000;
    color: #FFFFFF;
    border: 3px solid var(--acento);
    border-radius: 60px;
    font-weight: 800;
    font-size: __cta_size__px;
    box-shadow: 0 0 34px __accent_rgba_30__, 0 8px 24px rgba(0, 0, 0, 0.35);
  }
  .slide.final-cta .cta-seguir .verbo { color: var(--acento); }
  .slide.final-cta .guia-final {
    margin-top: 22px;
    max-width: 840px;
    border: 2px solid var(--acento);
    border-radius: 18px;
    padding: 18px 26px;
    font-size: 34px;
    line-height: 1.42;
    color: #E5E7EB;
    text-align: center;
    background: rgba(255, 255, 255, 0.03);
  }
  .slide.final-cta .guia-final b { color: #FFFFFF; }
  .slide.final-cta .cta-grande {
    margin-top: 28px;
    max-width: 880px;
    border: 3px solid var(--acento);
    border-radius: 24px;
    padding: 24px 34px;
    font-weight: 800;
    font-size: 54px;
    line-height: 1.28;
    color: #FFFFFF;
    text-align: center;
    background: rgba(255, 255, 255, 0.03);
    box-shadow: 0 0 40px __accent_rgba_30__;
  }
  .slide.final-cta .cta-grande .clave { color: var(--acento); }
  .slide.final-cta .comp-wrap { zoom: 0.82; margin-top: 20px; }
  /* ── Modo landing: cierre que empuja a un dominio propio ───────── */
  .landing-card {
    margin-top: 26px;
    max-width: 900px;
    border: 3px solid var(--acento);
    border-radius: 26px;
    padding: 26px 34px;
    text-align: center;
    background: #000000;
    box-shadow: 0 0 44px __accent_rgba_30__, 0 10px 30px rgba(0, 0, 0, 0.4);
  }
  .landing-card__tag {
    font-size: 26px;
    font-weight: 800;
    letter-spacing: 4px;
    color: var(--acento);
  }
  .landing-card__dominio {
    font-weight: 800;
    font-size: __landing_dom_size__px;
    line-height: 1.12;
    color: var(--acento);
    margin: 10px 0 12px;
    word-break: break-word;
  }
  .landing-card__sub {
    font-size: 31px;
    line-height: 1.42;
    color: #E5E7EB;
  }
  .landing-boton {
    display: inline-block;
    margin-top: 20px;
    padding: 20px 40px;
    background: #000000;
    color: #FFFFFF;
    border: 3px solid var(--acento);
    border-radius: 60px;
    font-weight: 800;
    font-size: 34px;
    box-shadow: 0 0 30px __accent_rgba_30__;
  }
  .landing-boton .clave { color: var(--acento); }
  .landing-boton--sec {
    margin-top: 14px;
    background: transparent;
    border: 2px dashed var(--acento);
    color: #E5E7EB;
    font-size: 28px;
    padding: 15px 34px;
    box-shadow: none;
  }
  .slide.final-cta .comandos-linea {
    margin-top: 22px;
    font-size: 30px;
    line-height: 1.4;
    color: #9CA3AF;
    text-align: center;
  }
  .slide.final-cta .comandos-linea b { color: #FFFFFF; }
  .slide.puente .landing-mini {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    flex-wrap: wrap;
    margin-top: 20px;
    border: 2px solid var(--acento);
    border-radius: 14px;
    background: #000000;
    padding: 14px 24px;
  }
  .slide.puente .landing-mini__dom {
    font-weight: 800;
    font-size: 34px;
    color: var(--acento);
  }
  .slide.puente .landing-mini__sub {
    font-size: 26px;
    color: #E5E7EB;
  }
  .guia-card {
    margin-top: 26px;
    border-left: 6px solid var(--acento);
    border-radius: 0 16px 16px 0;
    background: rgba(255, 255, 255, 0.04);
    padding: 16px 22px;
    text-align: left;
  }
  .guia-card__tag {
    font-size: 26px;
    font-weight: 800;
    letter-spacing: 3px;
    color: var(--acento);
    margin-bottom: 6px;
  }
  .guia-card__t { font-weight: 800; font-size: 36px; color: #FFFFFF; line-height: 1.3; }
  .guia-card__s { font-size: 32px; color: #C9CDD3; line-height: 1.4; margin-top: 4px; }
  .comp-error {
    margin-top: 24px;
    padding: 18px 22px;
    border: 2px solid #EF4444;
    background: rgba(239, 68, 68, 0.1);
    color: #FCA5A5;
    border-radius: 14px;
    font-size: 0.9em;
    text-align: left;
  }
__componentes_css__
</style>
</head>
<body__body_class__>
  <div class="slide __slide_class__">
    __fondo_codigo__
    <div class="encabezado">
      <div class="marca">
        <img class="isotipo" src="__isotipo__" alt="__marca__">
      </div>
      <div class="numero">__number__</div>
    </div>
    <div class="progreso"><div class="relleno"></div></div>
    <div class="contenido">
      <div class="ajuste">
      __contenido__
      </div>
    </div>
    <div class="pie">
      <img class="isotipo" src="__isotipo__" alt="__marca__">
      __pie__
    </div>
  </div>
</body>
</html>
"""


def _clase_slide(i, n):
    if i == 1:
        return "cover"
    if i == n:
        return "cta-final"
    return ""


def _format_scaling(fmt_key):
    """Factores de escala por formato (safe zones de 9:16 heredadas).

    Los formatos cortos (4:5, 3:4, 1:1) reducen además icono/título y
    encogen los componentes (`__comp_zoom__`) para que nada se recorte:
    el CSS clipa con overflow:hidden, así que el ajuste es estructural.
    """
    if fmt_key == "1:1":
        sc = {
            "__pad_top__": 16, "__pad_lr__": 44, "__pad_bottom__": 60,
            "__logo_size__": 64, "__num_size__": 22, "__num_box__": 46,
            "__prog_margin__": 12, "__prog_h__": 6, "__icon_margin__": 10,
            "__icon_size__": 120, "__title_size__": 76, "__title_margin__": 14,
            "__body_size__": 44, "__badge_margin__": 18, "__badge_pad_v__": 10,
            "__badge_pad_h__": 28, "__badge_size__": 32, "__cta_margin__": 14,
            "__cta_size__": 32, "__cta_pad_v__": 12, "__cta_pad_h__": 26,
            "__sec_margin__": 10, "__sec_size__": 26, "__ind_margin__": 22,
            "__ind_size__": 21, "__footer_size__": 22, "__pie_pad_v__": 14,
            "__pie_pad_b__": 28, "__footer_logo__": 36,
            "__landing_dom_size__": 54,
            "__contenido_zoom__": 1,
        }
        sc.update({
            "__comp_zoom__": 0.72, "__comp_margin__": 14, "__comp_base__": 45,
            "__icon_size__": 76, "__icon_margin__": 10,
            "__title_size__": 54, "__title_margin__": 8, "__body_size__": 37,
            "__ind_margin__": 14, "__ind_size__": 20,
            "__ind_disp__": "none", "__ind_h__": 72,
        })
        return sc
    s = {"4:5": 0.88, "3:4": 0.92}.get(fmt_key, 1.0)
    sc = {
        "__pad_top__": round(130 * s), "__pad_lr__": round(90 * s),
        "__pad_bottom__": round(240 * s), "__logo_size__": round(96 * s),
        "__num_size__": round(30 * s), "__num_box__": round(64 * s),
        "__prog_margin__": round(26 * s), "__prog_h__": 10,
        "__icon_margin__": round(26 * s), "__icon_size__": round(152 * s),
        "__title_size__": round(76 * s), "__title_margin__": round(38 * s),
        "__body_size__": round(44 * s), "__badge_margin__": round(34 * s),
        "__badge_pad_v__": round(14 * s), "__badge_pad_h__": round(32 * s),
        "__badge_size__": round(32 * s), "__cta_margin__": round(46 * s),
        "__cta_size__": round(40 * s), "__cta_pad_v__": round(22 * s),
        "__cta_pad_h__": round(44 * s), "__sec_margin__": round(34 * s),
        "__sec_size__": round(30 * s), "__ind_margin__": round(34 * s),
        "__ind_size__": round(26 * s), "__footer_size__": 28,
        "__pie_pad_v__": round(34 * s), "__pie_pad_b__": round(56 * s),
        "__footer_logo__": round(54 * s),
        "__landing_dom_size__": round(72 * s),
        "__contenido_zoom__": 1,
    }
    ajustes = {
        "3:4": {"__pad_top__": 62, "__pad_bottom__": 160,
                "__comp_zoom__": 0.80, "__comp_margin__": 20,
                "__icon_size__": 96, "__icon_margin__": 14,
                "__title_size__": 70, "__title_margin__": 22,
                "__ind_margin__": 16, "__ind_h__": 54},
        "4:5": {"__pad_top__": 60, "__pad_bottom__": 138,
                "__comp_zoom__": 0.80, "__comp_margin__": 16,
                "__icon_size__": 80, "__icon_margin__": 10,
                "__title_size__": 66, "__title_margin__": 20,
                "__ind_margin__": 12, "__ind_h__": 56},
    }
    sc.update(ajustes.get(fmt_key, {
        "__comp_zoom__": 1.0, "__comp_margin__": 34,
    }))
    sc.setdefault("__comp_base__", 40)
    sc.setdefault("__ind_h__", 72)
    sc.setdefault("__ind_disp__", "inline-flex")
    return sc


# ── Retención (hooks, puentes, CTA) ────────────────────────────────

MAX_PALABRAS_CUBIERTA = 12

HOOKS_CUBIERTA = (
    '<span class="clave">{kw}</span>: lo que casi nadie revisa.',
    'Tu <span class="clave">{kw}</span> falla en silencio.',
    'El fallo más caro casi siempre es <span class="clave">{kw}</span>.',
    'Antes de escalar, entiende <span class="clave">{kw}</span>.',
    'Configura <span class="clave">{kw}</span> antes de que falle.',
)

INDICADORES_SWIPE = (
    "Siguiente: el porqué",
    "Siguiente: el mecanismo",
    "Siguiente: la práctica",
    "Siguiente: el error común",
    "Siguiente: la checklist",
)

# Slide N-1: puente técnico real (sin promesa de sorpresa).
PUENTES = (
    ("El fallo casi siempre es reproducible.",
     "Si no lo repites, no lo puedes arreglar."),
    ("Si no se loguea, no existe.",
     "Observabilidad antes que adivinación."),
    ("El valor por defecto casi nunca es seguro.",
     "Revisa cada configuración automática."),
    ("El incidente empieza por lo simple.",
     "Antes del 0-day está el error humano."),
    ("Escalar sin medir es fe.",
     "Mide antes de añadir capacidad."),
)

PALABRAS_SUELTAS = {
    "y", "o", "u", "e", "de", "del", "la", "el", "los", "las", "en", "con",
    "para", "que", "a", "al", "sin", "por", "lo", "un", "una", "unos", "unas",
    "es", "son", "como", "pero", "su", "sus", "mas", "ni", "ya", "muy",
}


def _recortar_html(texto, max_palabras):
    """Recorta a N palabras visibles sin romper el HTML."""
    if not texto:
        return ""
    plano = re.sub(r"<br\s*/?>", " ", texto, flags=re.I)
    salida, abiertos, palabras, truncado = [], [], 0, False
    corte = None
    for tok in re.findall(r"<[^>]+>|[^<\s]+|\s+", plano):
        if tok.startswith("<"):
            salida.append(tok)
            nombre = re.match(r"</?(\w+)", tok)
            if nombre and tok.startswith("</"):
                if abiertos and abiertos[-1] == nombre.group(1):
                    abiertos.pop()
            elif nombre and not tok.endswith("/>"):
                abiertos.append(nombre.group(1))
            continue
        if tok.strip():
            palabras += 1
            if palabras > max_palabras:
                truncado = True
                break
        salida.append(tok)
        if re.search(r"[.!?…:]$", tok) and palabras >= max(1, max_palabras // 2):
            corte = (len(salida), tuple(abiertos))
    if corte:
        largo, ab = corte
        salida = salida[:largo]
        abiertos = list(ab)
    if truncado:
        while len(salida) > 1:
            if not salida[-1].strip():
                salida.pop()
                continue
            ultimo = salida[-1].strip().lower()
            if re.fullmatch(r"[\wÁÉÍÓÚáéíóúÑñ]+", ultimo) and ultimo in PALABRAS_SUELTAS:
                salida.pop()
                continue
            break
    res = "".join(salida).rstrip(" ,;:—…-")
    for nombre in reversed(abiertos):
        res += f"</{nombre}>"
    return res


def _contar_palabras(html):
    return len(re.sub(r"<[^>]+>", " ", html or "").split())


def _elegir(plantillas, semilla):
    """Elección determinista (crc32) dentro de una tupla de plantillas."""
    return plantillas[_indice_estable(semilla, len(plantillas))]


def _hook_portada(body, kw, semilla):
    m_t = re.search(r'<div class="titulo">(.*?)</div>', body, re.DOTALL)
    m_c = re.search(r'<div class="cuerpo">(.*?)</div>', body, re.DOTALL)
    titulo = _recortar_html(m_t.group(1).strip() if m_t else "",
                            MAX_PALABRAS_CUBIERTA)
    subtitulo = _recortar_html(m_c.group(1).strip() if m_c else body,
                               MAX_PALABRAS_CUBIERTA)
    if _contar_palabras(titulo) < 3:
        titulo = _recortar_html(_elegir(HOOKS_CUBIERTA, semilla).format(kw=kw),
                                MAX_PALABRAS_CUBIERTA)
    if _contar_palabras(subtitulo) < 3:
        subtitulo = ""
    return titulo, subtitulo


def _micro_indicador(i, n, semilla, modo="comentar"):
    if i == 1:
        return f"{n} ideas, una por slide"
    if i == n - 1:
        if (modo or "comentar") == "seguir":
            return "El cierre está en el último slide"
        return "La palabra está en la última"
    return INDICADORES_SWIPE[(i - 2) % len(INDICADORES_SWIPE)]


_FRASES_INDICADOR = INDICADORES_SWIPE + ("La palabra está en la última",
                                        "El cierre está en el último slide")

_RE_INDICADOR = re.compile(
    r"(?:\s*<br\s*/?>)*\s*(?:[\u2190-\u2199\u21B5]+\s*)?(?:"
    + "|".join(re.escape(f) for f in _FRASES_INDICADOR)
    + r"|\d+\s+ideas,\s+una\s+por\s+slide)\s*[.!]?\s*$",
    re.IGNORECASE,
)


def _quitar_indicador(body):
    if not body:
        return ""

    def _limpio(txt):
        return _RE_INDICADOR.sub("", txt).strip()

    def _reemplaza(m):
        return f'<div class="cuerpo">{_limpio(m.group(1))}</div>'

    nuevo, cuantos = re.subn(r'<div class="cuerpo">(.*?)</div>', _reemplaza,
                             body, flags=re.DOTALL)
    return nuevo if cuantos else _limpio(body)


def _ya_tiene_indicador(body):
    return "ind-swipe" in body or any(f in body for f in _FRASES_INDICADOR)


def _html_indicador(texto):
    return f'<div class="ind-swipe"><span class="flecha">&#8594;</span> {texto}</div>'


# ── Regla estricta de keywords por líneas (medida en Chromium) ─────

_JS_MEDIR = """<script>(function(){
var t=document.querySelector('.titulo');
if(!t){return;}
var fs=parseFloat(getComputedStyle(t).fontSize)||40;
var r=document.createRange(); r.selectNodeContents(t);
var rects=r.getClientRects(), tops=[];
for(var i=0;i<rects.length;i++){
  var q=rects[i];
  if(q.width<1||q.height<1){continue;}
  var top=Math.round(q.top), merged=false;
  for(var j=0;j<tops.length;j++){
    if(Math.abs(top-tops[j])<=fs*0.6){merged=true;break;}
  }
  if(!merged){tops.push(top);}
}
t.setAttribute('data-lineas',tops.length);
})();</script>"""

_RE_CLAVE = re.compile(r"""class=["']clave["']""")
_RE_TOKEN = re.compile(r"(<[^>]+>|[^\s<]+)")


def _clave_candidatas(titulo_html, cuantas):
    """Título con EXACTAMENTE `cuantas` keywords. Determinista."""
    if cuantas < 1:
        return titulo_html
    plano = re.sub(r"<[^>]+>", "", titulo_html)
    plano = re.sub(r"\s+", " ", plano).strip()
    tokens = _RE_TOKEN.findall(plano)
    ids_palabra = [i for i, t in enumerate(tokens) if not t.startswith("<")]
    if not ids_palabra:
        return titulo_html

    ultimo = len(tokens) - 1

    def _peso(i):
        palabra = tokens[i]
        limpio = re.sub(r"[^\wÁÉÍÓÚÜÑáéíóúüñ]", "", palabra).lower()
        if not limpio or limpio in PALABRAS_SUELTAS:
            return 0.0
        puntos = float(len(limpio))
        if i <= 1 or i >= ultimo - 2:
            puntos += 4.0
        if len(limpio) > 9:
            puntos += 1.5
        return puntos

    elegidas = []
    for i in sorted(ids_palabra, key=lambda k: (-_peso(k), k)):
        if _peso(i) <= 0:
            continue
        elegidas.append(i)
        if len(elegidas) == cuantas:
            break
    if not elegidas:
        return titulo_html

    elegidas = set(elegidas)
    salida = []
    for i, tok in enumerate(tokens):
        if i in elegidas and not tok.startswith("<"):
            salida.append(f'<span class="clave">{tok}</span>')
        else:
            salida.append(tok)
    return " ".join(salida)


def _reemplazar_titulo(html, titulo_html):
    return re.sub(r'(<div class="titulo">).*?(</div>)',
                  lambda m: m.group(1) + titulo_html + m.group(2),
                  html, count=1, flags=re.DOTALL)


def _medir_titulos(renders_dir, nombres, ancho, alto):
    probe_dir = renders_dir / "_probe"
    probe_dir.mkdir(parents=True, exist_ok=True)
    lineas = {}
    for nombre in nombres:
        src = renders_dir / nombre
        probe = probe_dir / nombre
        probe.write_text(
            src.read_text(encoding="utf-8").replace("</body>", _JS_MEDIR + "</body>"),
            encoding="utf-8")
        cmd = _cmd_chromium(
            f"--window-size={ancho},{alto}",
            "--virtual-time-budget=4000", "--dump-dom",
            f"file://{probe.resolve()}",
        )
        salida = _correr_chromium(cmd, espera=r'data-lineas="\d+"').stdout
        m = re.search(r'data-lineas="(\d+)"', salida)
        if not m:
            print(f"  ! {nombre}: no se pudo medir el título en Chromium "
                  f"(se deja sin reajustar claves).")
            continue
        lineas[nombre] = int(m.group(1))
    for f in probe_dir.glob("*.html"):
        f.unlink()
    try:
        probe_dir.rmdir()
    except OSError:
        pass
    return lineas


def ajustar_claves_por_lineas(renders_dir, nombres, ancho, alto, max_pasadas=3):
    """1 línea = 1 keyword; 2-3 líneas = 2. Medido, no estimado."""
    for _ in range(max_pasadas):
        lineas = _medir_titulos(renders_dir, nombres, ancho, alto)
        cambios = 0
        for nombre, n_lineas in lineas.items():
            objetivo = 1 if n_lineas <= 1 else 2
            path = renders_dir / nombre
            html = path.read_text(encoding="utf-8")
            m = re.search(r'<div class="titulo">(.*?)</div>', html, re.DOTALL)
            if not m:
                continue
            actual = m.group(1)
            if contar_claves(actual) == objetivo:
                continue
            nuevo = _clave_candidatas(actual, objetivo)
            if nuevo != actual:
                path.write_text(_reemplazar_titulo(html, nuevo), encoding="utf-8")
                cambios += 1
        if cambios == 0:
            print(f"  ✓ Claves por línea: {len(lineas)} título(s) medidos en Chromium.")
            return
    lineas = _medir_titulos(renders_dir, nombres, ancho, alto)
    for nombre, n_lineas in lineas.items():
        path = renders_dir / nombre
        html = path.read_text(encoding="utf-8")
        m = re.search(r'<div class="titulo">(.*?)</div>', html, re.DOTALL)
        if not m:
            continue
        objetivo = 1 if n_lineas <= 1 else 2
        actuales = contar_claves(m.group(1))
        if actuales != objetivo:
            print(f"  ! {nombre}: {n_lineas} líneas y {actuales} claves (revisar)")
    print(f"  ✓ Claves por línea: {len(lineas)} título(s) medidos en Chromium.")


_JS_OVERFLOW = """<script>window.addEventListener('load', function(){
var c=document.querySelector('.contenido');
if(!c){return;}
var t=document.querySelector('.ajuste')||c;
var cr=c.getBoundingClientRect(), bottom=-1e9, top=1e9, n=0;
for(var i=0;i<t.children.length;i++){
  var r=t.children[i].getBoundingClientRect();
  if(r.height>0){ n++; bottom=Math.max(bottom,r.bottom); top=Math.min(top,r.top); }
}
if(!n){return;}
var recorte=Math.max(c.scrollHeight-c.clientHeight,
                     Math.round(bottom-cr.bottom), Math.round(cr.top-top));
c.setAttribute('data-recorte',recorte);
});</script>"""


# ── Auto-fit: baja el zoom del contenido hasta que nada se recorte ──

_ZOOM_RE = re.compile(r"(\.ajuste \{[^}]*?zoom:\s*)([0-9.]+)")


def _zoom_de(html):
    m = _ZOOM_RE.search(html)
    return float(m.group(2)) if m else 1.0


def _set_zoom(html, z):
    return _ZOOM_RE.sub(lambda m: f"{m.group(1)}{z:g}", html, count=1)


def _medir_recortes(renders_dir, nombres, ancho, alto, workers=1):
    """{nombre: px_recortadas} (px<=0 = OK; -1 = no se pudo medir)."""
    probe_dir = renders_dir / "_probe"
    probe_dir.mkdir(parents=True, exist_ok=True)

    def medir(nombre):
        src = renders_dir / nombre
        # Archivo de sonda único por slide: seguro en paralelo.
        probe = probe_dir / nombre
        try:
            probe.write_text(
                src.read_text(encoding="utf-8").replace(
                    "</body>", _JS_OVERFLOW + "</body>"),
                encoding="utf-8")
        except OSError:
            return (nombre, -1)
        cmd = _cmd_chromium(
            f"--window-size={ancho},{alto}",
            "--virtual-time-budget=4000", "--dump-dom",
            f"file://{probe.resolve()}",
        )
        salida = _correr_chromium(cmd, espera=r'data-recorte="-?\d+"').stdout
        m = re.search(r'data-recorte="(-?\d+)"', salida)
        return (nombre, int(m.group(1)) if m else -1)

    if workers and workers > 1:
        with ThreadPoolExecutor(max_workers=workers) as ex:
            res = list(ex.map(medir, nombres))
    else:
        res = [medir(n) for n in nombres]
    for f in probe_dir.glob("*.html"):
        f.unlink()
    try:
        probe_dir.rmdir()
    except OSError:
        pass
    return dict(res)


def autoajustar_recortes(renders_dir, nombres, ancho, alto,
                         minimo=0.70, paso=0.94, max_iter=8, workers=1):
    """Reduce el zoom del contenido slide por slide hasta que no recorte.

    Devuelve {nombre: px} de los que siguen recortando tras el piso (`minimo`).
    """
    pendientes = list(nombres)
    for _ in range(max_iter):
        if not pendientes:
            break
        medidos = _medir_recortes(renders_dir, pendientes, ancho, alto, workers)
        malos = {n: px for n, px in medidos.items() if px > 0}
        if not malos:
            return {}
        for nombre, _px in malos.items():
            path = renders_dir / nombre
            try:
                html = path.read_text(encoding="utf-8")
            except OSError:
                continue
            z = _zoom_de(html)
            nz = round(max(minimo, z * paso), 4)
            if nz < z:
                path.write_text(_set_zoom(html, nz), encoding="utf-8")
        pendientes = list(malos)
    finales = _medir_recortes(renders_dir, pendientes, ancho, alto, workers)
    return {n: px for n, px in finales.items() if px > 0}


def chequear_overflow(renders_dir, nombres, ancho, alto, workers=1):
    """Mide el recorte real de .contenido (compat: lista de tuplas).

    El CSS clipa con overflow:hidden: sin esta medición un lienzo corto
    (4:5, 3:4, 1:1) puede recortar componentes sin ningún aviso.
    Devuelve [(nombre, px_recortadas), ...] de los slides afectados.
    """
    medidos = _medir_recortes(renders_dir, nombres, ancho, alto, workers)
    return [(n, px) for n, px in medidos.items() if px != 0]


# ── Puente-recap: las 3 ideas clave del propio carrusel ────────────

def _texto_titulo(body):
    """Primer .titulo del body en texto plano (sin tags ni entidades)."""
    m = re.search(r'<div class="titulo">(.*?)</div>', body or "", re.DOTALL)
    if not m:
        return ""
    txt = re.sub(r"<[^>]+>", "", m.group(1))
    txt = (txt.replace("&nbsp;", " ").replace("&amp;", "&")
              .replace("&lt;", "<").replace("&gt;", ">")
              .replace("&quot;", '"'))
    return re.sub(r"\s+", " ", txt).strip()


def _landing_dominio(url):
    """'https://chmodxcode.pro/' → 'chmodxcode.pro' (para mostrar limpio)."""
    d = (url or "").strip()
    for pre in ("https://", "http://", "www."):
        if d.lower().startswith(pre):
            d = d[len(pre):]
    return d.rstrip("/") or (url or "").strip()


def _elegir_recap(titulos):
    """3 títulos repartidos (inicio/medio/cierre), 7 palabras máx c/u."""
    limpios = [t for t in titulos if _contar_palabras(t) >= 2]
    if len(limpios) < 2:
        return []
    idx = [0, len(limpios) // 2, len(limpios) - 1]
    vistos, recap = set(), []
    for k in idx:
        PALABRAS = " ".join(limpios[k].split()[:7])
        if PALABRAS.lower() not in vistos:
            vistos.add(PALABRAS.lower())
            recap.append(PALABRAS)
    return recap


# ── Generación de HTML por slide ───────────────────────────────────

def generar_html(i, n, data, fmt_key, fmt, accent_vars, isotipo, marca,
                  icono=None, badge=None, cta_palabra="CLAVE",
                  resalte_vars=None, semilla="", warnings=None,
                  guia=True, guia_tag=None, guia_titulo=None, guia_sub=None,
                  comandos_finales=None, cta_modo="seguir", recap_titulos=None,
                  landing=None, landing2=None, landing2_texto=None,
                  plano=False, categoria=None, fondo="auto", fondo_fijo=False):
    numero = data["number"] if data["number"] else f"{i}/{n}"
    cuerpo = _quitar_indicador(data["body"])
    cls = _clase_slide(i, n)
    extra = ""
    reemplaza = False

    # Componentes gráficos declarados en el slide fuente
    cuerpo, usados = expandir(cuerpo, {"accent": accent_vars["accent"]},
                              warnings)
    if usados:
        print(f"    · slide {i}: componentes {', '.join(usados)}")

    if i == 1:
        reemplaza = True
        kw = (cta_palabra or badge or "CLAVE").strip()
        # La portada puede traer UN componente (ej. terminal con gancho):
        # expandir() lo deja al final en .comp-wrap; se separa para que
        # _hook_portada lea solo título/subtítulo y se re-anexa después.
        comp_html = ""
        corte = cuerpo.find('<div class="comp-wrap">')
        if corte != -1:
            comp_html = cuerpo[corte:]
            cuerpo = cuerpo[:corte]
        titulo_c, subtitulo_c = _hook_portada(cuerpo, kw, semilla)
        extra = f'<div class="titulo">{titulo_c}</div>'
        if subtitulo_c:
            extra += f'<div class="cuerpo">{subtitulo_c}</div>'
        if comp_html:
            extra += comp_html
        extra += _html_indicador(_micro_indicador(i, n, semilla, cta_modo))
    elif i == n - 1:
        cls = "puente"
        reemplaza = True
        recap = _elegir_recap(recap_titulos or [])
        landing_mini = ""
        if landing:
            dom = _landing_dominio(landing)
            landing_mini = (
                f'<div class="landing-mini">'
                f'<span class="landing-mini__dom">{dom}</span>'
                f'<span class="landing-mini__sub">Curso de Python + '
                f'canal de Telegram</span></div>')
        if recap:
            props_chk = {"titulo": "Lo esencial en 3 ideas",
                         "items": recap}
            cuerpo_chk, _u = expandir(
                '<div class="componente" data-component="checklist" '
                f"data-props='{json.dumps(props_chk, ensure_ascii=False)}'>"
                "</div>", {"accent": accent_vars["accent"]}, warnings)
            titulo_p = ("Ver no es hacer: empieza a programar hoy"
                        if landing else "Antes del final: el resumen")
            extra = (f'<div class="titulo">{titulo_p}</div>'
                     f'{cuerpo_chk}{landing_mini}'
                     f'{_html_indicador(_micro_indicador(i, n, semilla, cta_modo))}')
        else:
            t, c = _elegir(PUENTES, semilla)
            if landing:
                t = "La mejor hora para tu primer script es hoy"
                c = ("Cada programador empezó con una sola línea. "
                     "La tuya puede ser la próxima.")
            extra = (f'<div class="titulo">{t}</div>'
                     f'<div class="cuerpo">{c}</div>{landing_mini}'
                     f'{_html_indicador(_micro_indicador(i, n, semilla, cta_modo))}')
    elif i == n:
        cls = "final-cta"
        reemplaza = True
        palabra = cta_palabra or "CLAVE"
        if (cta_modo or "comentar") == "seguir":
            boton_cta = ('<div class="cta-seguir"><span class="verbo">SÍGUENOS'
                         '</span> Y NO TE PIERDAS LO QUE SIGUE</div>')
            secundario = (f'<div class="secundario">Guarda este carrusel: lo '
                          f'vas a necesitar · El próximo tema lo eligen los '
                          f'seguidores · {marca}</div>')
        else:
            boton_cta = (
                f'<div class="cta">Comenta <span class="clave">{palabra}</span> '
                'y te paso la checklist completa</div>')
            secundario = (
                f'<div class="secundario">Guarda este carrusel o pásaselo a tu '
                f'equipo técnico · {marca}</div>')
        terminal_html = ""
        if comandos_finales:
            tope_term = 6 if landing else 12
            props_term = {"titulo": "comandos · listos para copiar",
                          "lines": [{"t": "cmd", "v": c}
                                    for c in comandos_finales[:tope_term]]}
            cuerpo_term, _usados = expandir(
                '<div class="componente" data-component="terminal" '
                f"data-props='{json.dumps(props_term, ensure_ascii=False)}'>"
                "</div>", {"accent": accent_vars["accent"]}, warnings)
            terminal_html = cuerpo_term
        if landing:
            dom = _landing_dominio(landing)
            sec = ""
            if landing2:
                dom2 = _landing_dominio(landing2)
                txt2 = (landing2_texto or "ÚNETE AL TELEGRAM").strip()
                sec = (f'<div class="landing-boton landing-boton--sec">{txt2} '
                       f'<span class="clave">{dom2.upper()}</span></div>')
            extra = (
                '<div class="titulo">De mirar a programar</div>'
                + terminal_html +
                '<div class="landing-card">'
                '<div class="landing-card__tag">TU SIGUIENTE PASO</div>'
                f'<div class="landing-card__dominio">{dom}</div>'
                '<div class="landing-card__sub">Curso de Python completo y '
                'canal de Telegram para resolver dudas en comunidad.</div>'
                f'<div class="landing-boton">EMPIEZA EN <span class="clave">'
                f'{dom.upper()}</span></div>'
                + sec +
                '</div>'
                '<div class="comandos-linea">Todos los comandos completos '
                'están en el <b>primer comentario</b></div>'
            )
        else:
            extra = (
                '<div class="titulo">¿Listo para aplicarlo?</div>'
                + terminal_html +
                '<div class="cta-grande">COPIA LOS COMANDOS DEL '
                '<span class="clave">PRIMER COMENTARIO</span></div>'
                + boton_cta
                + secundario
            )
    else:
        if not _ya_tiene_indicador(cuerpo):
            extra = _html_indicador(_micro_indicador(i, n, semilla, cta_modo))

    contenido = ""
    if icono:
        contenido += (f'<div class="icono-box"><img class="icono-svg" '
                      f'src="{icono}" alt=""></div>')
    if i == 1 and badge:
        contenido += f'<div class="badge">{badge}</div>'
    contenido += extra if reemplaza else cuerpo + extra

    # Funnel: card fija en el slide 2 que empuja al último slide.
    if guia and i == 2 and n >= 3:
        tag = guia_tag or "NO TE LO PIERDAS"
        tit = guia_titulo or "Los comandos completos están al final"
        sub = (guia_sub or "Desliza hasta el último slide: repo + comandos "
                           "listos para copiar y primer comentario con todo")
        if landing and not guia_titulo:
            dom = _landing_dominio(landing)
            tit = "Comandos y tu próximo paso, al final"
            sub = f"Y en {dom}: curso de Python + Telegram"
        card_style = (' style="margin-top:14px;padding:12px 22px"'
                      if landing else "")
        contenido += (
            f'<div class="guia-card"{card_style}>'
            f'<div class="guia-card__tag">{tag}</div>'
            f'<div class="guia-card__t">{tit}</div>'
            f'<div class="guia-card__s">{sub}</div></div>'
        )

    pie = data["footer"] or f"{marca}"
    pie = pie.replace("AudioBlaze", marca)

    # Fondo: el rol del slide decide la intensidad del mesh; el vertical, la
    # textura. --fondo-fijo fuerza el perfil "contenido" para todos.
    rol_fondo = "contenido" if fondo_fijo else {
        "cover": "cover", "puente": "puente",
        "final-cta": "cierre"}.get(cls, "contenido")
    capas_fondo = _fondos.fondo(
        rol=rol_fondo, vertical=categoria or "tech",
        rgb=accent_vars.get("rgb", (250, 204, 21)),
        variante=fondo, comandos=comandos_finales)

    sc = _format_scaling(fmt_key)
    html = TEMPLATE
    for k, v in {
        "__slide_class__": cls,
        "__body_class__": ' class="plano"' if plano else "",
        "__accent__": accent_vars["accent"],
        "__accent_bright__": accent_vars["accent_bright"],
        "__accent_rgba__": accent_vars["accent_rgba"],
        "__accent_rgba_b__": accent_vars["accent_rgba_b"],
        "__accent_rgba_30__": accent_vars["accent_rgba_30"],
        "__accent_rgba_40__": accent_vars["accent_rgba_40"],
        "__componentes_css__": _tokens.COMPONENTES_CSS,
        "__fondo_img__": capas_fondo["fondo"],
        "__textura_img__": capas_fondo["textura"],
        "__textura_size__": capas_fondo["textura_size"],
        "__textura_mask__": capas_fondo["textura_mask"],
        "__textura_op__": capas_fondo["textura_op"],
        "__fondo_codigo__": capas_fondo["codigo"],
        "__links_fuentes__": _fonts.links(),
        "__font_display__": _fonts.DISPLAY,
        "__marca__": marca,
        **(resalte_vars or {}),
        "__slide_w__": fmt["w"],
        "__slide_h__": fmt["h"],
        "__progreso_pct__": round(i / n * 100, 2),
        "__isotipo__": isotipo or "",
        "__number__": numero,
        "__contenido__": contenido,
        "__pie__": pie,
        **sc,
    }.items():
        html = html.replace(k, str(v))
    return html


# ── Render (UN slide a la vez) ─────────────────────────────────────

def renderizar(html_path, preview_dir, w, h, intentos=3, reusar=False):
    preview_dir.mkdir(parents=True, exist_ok=True)
    render_h = h + 87  # Chrome resta 87px de chrome de ventana al viewport
    dest = preview_dir / html_path.with_suffix(".png").name
    if dest.exists() and reusar:
        print(f"  = PNG {dest.name} (sin cambios)")
        return True
    if dest.exists():
        dest.unlink()
    # Nombre único: varios Chromium pueden renderizar en paralelo sin pisarse.
    shot = f"__shot_{html_path.stem}.png"
    src = html_path.parent / shot
    cmd = _cmd_chromium(
        f"--screenshot={shot}",
        f"--window-size={w},{render_h}",
        "--virtual-time-budget=8000",
        "--hide-scrollbars",
        f"file://{html_path.resolve()}",
    )
    for intento in range(1, intentos + 1):
        if src.exists():
            try:
                src.unlink()
            except OSError:
                pass
        r = _correr_chromium(cmd, existe=src, cwd=str(html_path.parent))
        if r.returncode == 0 and src.exists():
            break
        if intento == intentos:
            print(f"  ✗ {dest.name}: Chromium falló {intentos} veces. "
                  f"Falta este PNG: no publiques la carpeta hasta reintentar.")
            return False
        time.sleep(3)
    try:
        img = Image.open(str(src))
        img.crop((0, 0, w, h)).save(str(src))
        img.close()
        src.replace(dest)
    except Exception as e:
        print(f"  ✗ {dest.name}: PNG ilegible ({e}). "
              f"No publiques la carpeta hasta reintentar.")
        return False
    print(f"  OK PNG: {dest.name}")
    return True


def renderizar_paralelo(html_paths, preview_dir, w, h, workers=4, reusar=False):
    """Renderiza N slides con varios Chromium a la vez. Devuelve los fallidos.

    Con `reusar`, salta los slides cuyo HTML no cambió desde la última vez
    (hash guardado en `preview/.hashes.json`) y cuyo PNG ya existe.
    """
    import hashlib
    preview_dir.mkdir(parents=True, exist_ok=True)
    man_path = preview_dir / ".hashes.json"
    try:
        manifest = json.loads(man_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        manifest = {}

    pendientes, reusados = [], 0
    for p in html_paths:
        dest = preview_dir / p.with_suffix(".png").name
        if reusar and dest.exists():
            try:
                sha = hashlib.sha1(p.read_bytes()).hexdigest()
            except OSError:
                sha = None
            if sha and manifest.get(p.name) == sha:
                reusados += 1
                continue
        pendientes.append(p)
    if reusados:
        print(f"  = {reusados} PNG sin cambios (reusados)")

    def _guardar_manifest():
        try:
            man_path.write_text(json.dumps(manifest, indent=0), encoding="utf-8")
        except OSError:
            pass

    def _anotar(p):
        try:
            manifest[p.name] = hashlib.sha1(p.read_bytes()).hexdigest()
        except OSError:
            pass

    fallidos = []
    if workers <= 1:
        for p in pendientes:
            if not renderizar(p, preview_dir, w, h):
                fallidos.append(p.name)
            else:
                _anotar(p)
                _guardar_manifest()
    else:
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futuros = {ex.submit(renderizar, p, preview_dir, w, h): p
                       for p in pendientes}
            for fut in futuros:
                p = futuros[fut]
                try:
                    ok = fut.result()
                except Exception as e:  # noqa: BLE001
                    print(f"  ✗ {p.name}: error de render ({e}).")
                    ok = False
                if not ok:
                    fallidos.append(p.name)
                else:
                    # Manifiesto al día tras cada slide: si el proceso se corta,
                    # lo ya renderizado se reutiliza con --incremental.
                    _anotar(p)
                    _guardar_manifest()

    for p in pendientes:
        if p.name in fallidos:
            continue
        if p.name not in manifest:
            _anotar(p)
    _guardar_manifest()
    return fallidos


# ── QA de repetición (componentes y texto) ─────────────────────────


def _texto_visible(html):
    """Texto plano del contenido del slide (sin chrome, tags ni atributos)."""
    import html as _h
    sin_style = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html,
                       flags=re.S | re.I)
    # El número y el pie son constantes en todos los slides: fuera.
    sin_chrome = re.sub(
        r'<div class="(numero|pie|ind-swipe|marca)"[^>]*>.*?</div>', " ",
        sin_style, flags=re.S | re.I)
    txt = re.sub(r"<[^>]+>", " ", sin_chrome)
    txt = _h.unescape(txt)
    return re.sub(r"\s+", " ", txt).strip().lower()


def _componentes_fuente(input_dir, nombres):
    """{nombre: [componentes declarados]} leyendo el slide fuente."""
    por_slide = {}
    for nombre in nombres:
        p = input_dir / nombre
        try:
            txt = p.read_text(encoding="utf-8")
        except OSError:
            continue
        comps = re.findall(r'data-component="([^"]+)"', txt)
        if comps:
            por_slide[nombre] = [c.lower().strip() for c in comps]
    return por_slide


def qa_repeticion(input_dir, nombres, umbral=0.85):
    """Avisa de texto casi idéntico entre slides y de componentes repetidos.

    Compara el contenido REAL de los slides fuente (no el render, que repite
    footer/número en todos y daría falsos positivos). No bloquea: devuelve la
    lista de avisos para imprimir.
    """
    import difflib
    avisos = []

    # 1) Texto casi idéntico en slides no consecutivos.
    textos = {}
    for nombre in nombres:
        p = input_dir / nombre
        try:
            textos[nombre] = _texto_visible(p.read_text(encoding="utf-8"))
        except OSError:
            pass
    nombres_ok = [n for n in nombres if textos.get(n)]
    for a in range(len(nombres_ok)):
        for b in range(a + 1, len(nombres_ok)):
            na, nb = nombres_ok[a], nombres_ok[b]
            if abs(a - b) == 1:
                continue
            ta, tb = textos[na], textos[nb]
            if not ta or not tb or abs(len(ta) - len(tb)) > 0.4 * max(len(ta), len(tb)):
                continue
            r = difflib.SequenceMatcher(None, ta, tb).ratio()
            if r >= umbral:
                avisos.append(f"{na} y {nb} comparten {round(r * 100)}% del "
                              f"texto: revisá que no digan lo mismo.")

    # 2) Mismo componente en demasiados slides.
    fuentes = _componentes_fuente(input_dir, nombres)
    conteo = {}
    for comps in fuentes.values():
        for c in set(comps):
            conteo[c] = conteo.get(c, 0) + 1
    total = len(fuentes) or 1
    for c, k in sorted(conteo.items(), key=lambda x: -x[1]):
        if k >= 4 and k / total >= 0.5:
            avisos.append(f"componente '{c}' aparece en {k}/{total} slides: "
                          f"variá el ritmo visual.")
    return avisos


# ── Contact sheet · export PDF/Reel ────────────────────────────────


def generar_contact_sheet(input_dir, nombres, fmt, cols=5, thumb=360):
    """Grilla PNG con todo el carrusel para revisarlo de un vistazo."""
    if Image is None:
        print("  ! Contact sheet: falta Pillow.")
        return None
    renders = input_dir / "preview"
    pngs = []
    for nombre in nombres:
        p = renders / Path(nombre).with_suffix(".png")
        if p.exists():
            pngs.append(p)
    if not pngs:
        return None
    escala = thumb / fmt["w"]
    th, tw = int(fmt["h"] * escala), thumb
    gap = 18
    filas = (len(pngs) + cols - 1) // cols
    ancho = cols * tw + (cols + 1) * gap
    alto = filas * th + (filas + 1) * gap
    hoja = Image.new("RGB", (ancho, alto), (11, 11, 13))
    for i, p in enumerate(pngs):
        try:
            im = Image.open(str(p)).convert("RGB").resize((tw, th))
        except Exception:
            continue
        fila, col = divmod(i, cols)
        x = gap + col * (tw + gap)
        y = gap + fila * (th + gap)
        hoja.paste(im, (x, y))
        im.close()
    dest = input_dir / "contact-sheet.png"
    hoja.save(str(dest))
    hoja.close()
    print(f"  OK contact-sheet.png ({len(pngs)} slides)")
    return dest


def exportar_pdf(input_dir, nombres, fmt):
    """Carrusel completo en un PDF (una página por slide)."""
    if Image is None:
        print("  ! PDF: falta Pillow.")
        return None
    renders = input_dir / "preview"
    imgs = []
    for nombre in nombres:
        p = renders / Path(nombre).with_suffix(".png")
        if p.exists():
            try:
                imgs.append(Image.open(str(p)).convert("RGB"))
            except Exception:
                pass
    if not imgs:
        return None
    dest = input_dir / f"{input_dir.name}.pdf"
    imgs[0].save(str(dest), save_all=True, append_images=imgs[1:],
                 resolution=100.0)
    for im in imgs:
        im.close()
    print(f"  OK {dest.name} ({len(imgs)} páginas)")
    return dest


def exportar_reel(input_dir, nombres, fmt, fps=1.6):
    """Reel MP4 con ffmpeg (si está instalado). Silencioso si no lo está."""
    import shutil
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        print("  ! Reel: ffmpeg no está instalado; se omite el MP4.")
        return None
    renders = input_dir / "preview"
    pngs = [renders / Path(n).with_suffix(".png") for n in nombres]
    pngs = [p for p in pngs if p.exists()]
    if not pngs:
        return None
    lista = input_dir / ".reel.txt"
    dur = round(1.0 / fps, 3)
    with lista.open("w", encoding="utf-8") as f:
        for p in pngs:
            f.write(f"file '{p.resolve()}'\nduration {dur}\n")
        f.write(f"file '{pngs[-1].resolve()}'\n")
    dest = input_dir / f"{input_dir.name}.mp4"
    cmd = [ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", str(lista),
           "-vf", f"scale={fmt['w']}:{fmt['h']}:force_original_aspect_ratio=decrease,"
                  f"pad={fmt['w']}:{fmt['h']}:(ow-iw)/2:(oh-ih)/2:color=0x0B0B0D,"
                  f"format=yuv420p", "-r", "30", "-c:v", "libx264", "-preset",
           "medium", str(dest)]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True)
    except Exception as e:  # noqa: BLE001
        print(f"  ! Reel: ffmpeg falló ({e}).")
        return None
    finally:
        try:
            lista.unlink()
        except OSError:
            pass
    if r.returncode != 0 or not dest.exists():
        print("  ! Reel: ffmpeg no pudo generar el MP4.")
        return None
    print(f"  OK {dest.name} ({len(pngs)} slides)")
    return dest


# ── Story teaser (propia, sin dependencias externas) ───────────────

STORY_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>__marca__ story</title>
__links_fuentes__
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  /* Sin estas vars el background entero se cae (var() indefinido invalida la
     declaración): el glow, el borde de la píldora y las keywords dependen de
     que existan. */
  :root {
    --acento: __accent__;
    --acento-brillo: __accent_bright__;
    --acento-rgba-b: __accent_rgba_b__;
    --acento-rgba-30: __accent_rgba_30__;
    --acento-rgba-40: __accent_rgba_40__;
    --resalte: __resalte__;
    --resalte-brillo: __resalte_brillo__;
  }
  body {
    font-family: __font_display__;
    background: #0B0B0D;
    color: #FFFFFF;
    -webkit-font-smoothing: antialiased;
  }
  .story {
    width: 1080px; height: 1920px;
    padding: 150px 90px;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    text-align: center;
    position: relative;
    background:
      radial-gradient(circle at 85% 8%, __accent_rgba__, transparent 45%),
      radial-gradient(circle at 8% 92%, var(--acento-rgba-b), transparent 45%),
      __estrellas__,
      #0B0B0D;
  }
  .isotipo { width: 130px; margin-bottom: 70px;
    filter: drop-shadow(0 0 26px var(--acento-rgba-30)); }
  .titulo {
    font-size: 92px; font-weight: 800; line-height: 1.1;
    text-shadow: 0 0 54px var(--acento-rgba-30);
  }
  .titulo .clave {
    color: var(--resalte); font-weight: 800;
    text-shadow: 0 0 27px __resalte_rgba32__, 0 2px 6px rgba(0,0,0,.55);
  }
  .story-sub {
    margin-top: 36px; max-width: 860px;
    font-size: 40px; line-height: 1.45; color: #C9CDD3;
  }
  .story .terminal {
    width: 100%; margin-top: 70px;
    background: #000000; border: 2px solid #334155; border-radius: 22px;
    overflow: hidden; text-align: left;
    font-size: 36px;
    box-shadow: 0 14px 34px rgba(0, 0, 0, 0.45);
  }
  .story .terminal__bar {
    display: flex; align-items: center; gap: 12px;
    padding: 16px 24px; border-bottom: 1px solid #334155;
  }
  .story .terminal__dot { width: 16px; height: 16px; border-radius: 50%; }
  .story .terminal__dot--r { background: #EF4444; }
  .story .terminal__dot--y { background: #F59E0B; }
  .story .terminal__dot--g { background: #10B981; }
  .story .terminal__titulo {
    margin-left: 10px;
    font-family: 'Hasklig', 'JetBrains Mono', 'SFMono-Regular', Menlo, Consolas, monospace;
    font-size: 0.85em; color: #9CA3AF; letter-spacing: 0.4px;
  }
  .story .terminal__body { padding: 24px 28px; }
  .story .terminal__line {
    font-family: 'Hasklig', 'JetBrains Mono', 'SFMono-Regular', Menlo, Consolas, monospace;
    font-size: 0.92em; line-height: 1.6;
    word-break: break-word; white-space: pre-wrap; color: #E5E7EB;
  }
  .story .terminal__line + .terminal__line { margin-top: 8px; }
  .story .terminal__line .prompt { color: #10B981; font-weight: 700; }
  .story .terminal__line--cmd { color: #F8FAFC; font-weight: 500; }
  .story .terminal__line--out { color: #9CA3AF; }
  .story .terminal__line--ok { color: #10B981; }
  .story .terminal__line--err { color: #EF4444; }
  .story .terminal__line--warn { color: #F59E0B; }
  .btn-perfil {
    margin-top: 70px;
    padding: 30px 54px;
    border: 3px solid var(--acento);
    border-radius: 70px;
    background: #000000;
    font-size: 44px; font-weight: 800; color: #FFFFFF;
    box-shadow: 0 0 34px var(--acento-rgba-30), 0 8px 24px rgba(0, 0, 0, 0.35);
  }
  .btn-perfil .verbo { color: var(--acento); }
  .pill {
    margin-top: 90px;
    padding: 26px 46px;
    border: 2px solid var(--acento-rgba-40);
    border-radius: 60px;
    background: linear-gradient(180deg, rgba(255,255,255,.07), rgba(255,255,255,.02));
    font-size: 34px; font-weight: 600; color: #DCDCE2;
    box-shadow: 0 10px 28px rgba(0,0,0,.45);
  }
  .marca-pie {
    position: absolute; bottom: 110px;
    font-size: 30px; color: #8E8E93; letter-spacing: 2px;
  }
</style>
</head>
<body>
  <div class="story">
    __isotipo__
    <div class="titulo">__titulo__</div>
    __subtitulo__
    __terminal__
    <div class="btn-perfil"><span class="verbo">VER POST COMPLETO</span> EN EL PERFIL</div>
    <div class="marca-pie">__marca__</div>
  </div>
</body>
</html>
"""


def generar_story(input_dir: Path, display, resalte_hex, isotipo,
                  accent_vars, marca) -> bool:
    fuente = input_dir / "story-fuente.html"
    if not fuente.is_file():
        print("  · story: no hay story-fuente.html (opcional, se omite)")
        return False
    html_src = fuente.read_text(encoding="utf-8")
    m = re.search(r'<div class="titulo">(.*?)</div>', html_src, re.DOTALL)
    titulo = m.group(1).strip() if m else _html_escape(display)
    m_sub = re.search(r'<div class="cuerpo">(.*?)</div>', html_src, re.DOTALL)
    subtitulo = ""
    if m_sub and m_sub.group(1).strip():
        subtitulo = (f'<div class="story-sub">{m_sub.group(1).strip()}</div>')
    # Terminal con los primeros comandos reales del carrusel
    terminal_html = ""
    try:
        import generar_copy_tech as _gct
        cmds = _gct.extraer_comandos(input_dir)[:3]
        if cmds:
            props_term = {"titulo": "desde el carrusel",
                          "lines": [{"t": "cmd", "v": c} for c in cmds]}
            cuerpo_term, _u = expandir(
                '<div class="componente" data-component="terminal" '
                f"data-props='{json.dumps(props_term, ensure_ascii=False)}'>"
                "</div>", {"accent": accent_vars["accent"]}, [])
            terminal_html = cuerpo_term
    except Exception:
        terminal_html = ""
    rr, rg, rb = (int(resalte_hex.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    brillo = f"#{min(255, int(rr + (255 - rr) * 0.45)):02x}" \
             f"{min(255, int(rg + (255 - rg) * 0.45)):02x}" \
             f"{min(255, int(rb + (255 - rb) * 0.45)):02x}"
    html = STORY_TEMPLATE
    for k, v in {
        "__marca__": marca,
        "__links_fuentes__": _fonts.links(),
        "__font_display__": _fonts.DISPLAY,
        "__accent__": accent_vars["accent"],
        "__accent_bright__": accent_vars["accent_bright"],
        "__accent_rgba__": accent_vars["accent_rgba"],
        "__accent_rgba_b__": accent_vars["accent_rgba_b"],
        "__accent_rgba_30__": accent_vars["accent_rgba_30"],
        "__accent_rgba_40__": accent_vars["accent_rgba_40"],
        "__estrellas__": _stars.css_estrellas(),
        "__resalte_rgba32__": f"rgba({rr},{rg},{rb},0.32)",
        "__resalte__": resalte_hex,
        "__resalte_brillo__": brillo,
        "__titulo__": titulo,
        "__subtitulo__": subtitulo,
        "__terminal__": terminal_html,
        "__isotipo__": (f'<img class="isotipo" src="{isotipo}" alt="{marca}">'
                        if isotipo else ""),
    }.items():
        html = html.replace(k, str(v))
    stories = input_dir / "stories"
    stories.mkdir(parents=True, exist_ok=True)
    out = stories / "story-01.html"
    out.write_text(html, encoding="utf-8")
    return renderizar(out, stories, 1080, 1920)


def _html_escape(t):
    return (t or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ── caption.txt ────────────────────────────────────────────────────

def escribir_caption(output_dir, display_tema, cta_palabra, hashtags, marca,
                     modo="comentar", landing=None, landing2=None,
                     landing2_texto=None):
    if landing:
        dom = _landing_dominio(landing)
        extra2 = ""
        if landing2:
            dom2 = _landing_dominio(landing2)
            txt2 = (landing2_texto or "Telegram").strip()
            extra2 = f"\n{txt2}: {dom2}."
        accion = (f"Empieza en {dom}: curso de Python completo y canal de "
                  "Telegram para resolver dudas en comunidad."
                  f"{extra2}\n"
                  "Todos los comandos, en el primer comentario.")
    elif (modo or "comentar") == "seguir":
        accion = ("Síguenos para no perderte la próxima guía: cada semana "
                  "un tema así, sin humo.\n"
                  "Guarda este post y comenta qué tema quieres ver.")
    else:
        accion = (f"Comenta {cta_palabra} y te paso la checklist completa.")
    caption = (
        f"{display_tema}. Te lo cuento corto y directo.\n"
        f"{accion}\n\n"
        "Aviso: contenido educativo y defensivo. "
        "No sustituye una auditoría profesional.\n\n"
        f"{hashtags}\n"
        f"— {marca}"
    )
    (output_dir / "caption.txt").write_text(caption + "\n", encoding="utf-8")
    print("  OK caption.txt")


# ── main ───────────────────────────────────────────────────────────

# ── Auto-generación de slides (flujo de 1 comando) ────────────────
# Paridad con crear-carousel: si la carpeta no tiene slide-*.html, el mismo
# comando escribe el copy con el banco de la vertical y sigue renderizando.

_MAPA_VERTICAL = {
    "cybersec": "cybersec", "dev": "prog", "prog": "prog",
    "ai": "ai", "ia": "ai", "infra": "infra", "data": "prog",
    "tech": "prog", "educativo": "cybersec", "common": "cybersec",
}


def _slides_existentes(input_dir: Path):
    if not input_dir.is_dir():
        return []
    return [f for f in sorted(input_dir.glob("slide-*.html"))
            if not f.name.startswith("story-")]


def _generar_slides_auto(input_dir, n, vertical, display, short, marca, slug,
                         resalte=None, permitidos=None):
    """Escribe slide-*.html + story-fuente.html con el copywriting de la skill."""
    import generar_copy_tech as gct
    input_dir.mkdir(parents=True, exist_ok=True)
    print(f"  · Sin slide-*.html: generando copy ({n} slides, "
          f"vertical {vertical})...")
    plantillas, _textos, hook = gct.generar_slides(
        slug, n, vertical, display, short, marca, permitidos=permitidos)
    for numero, contenido in plantillas:
        path = input_dir / f"slide-{numero:02d}.html"
        path.write_text(
            gct._slide_html(f"{numero}/{n}", contenido, f"{marca} · {short}",
                            resalte=resalte),
            encoding="utf-8")
        print(f"    OK slide-{numero:02d}.html")
    (input_dir / "story-fuente.html").write_text(
        gct._slide_html(
            "1/1",
            f'      <div class="titulo">'
            f'{gct._marcar_clave(short, candidata=short.split()[0] if short else None)}'
            f"</div>",
            marca, resalte=resalte),
        encoding="utf-8")
    print(f"    OK story-fuente.html  ·  hook: {hook}")
    return _slides_existentes(input_dir)


def main():
    ap = argparse.ArgumentParser(description="TechEdu carousel builder")
    ap.add_argument("--tema", required=True, help="Carpeta fuente en CTSLIDER")
    ap.add_argument("--color", required=True,
                    help="Color de acento: #RRGGBB o nombre de paleta")
    ap.add_argument("--slides", required=True, type=int,
                    help="Cantidad de diapositivas (debe coincidir con slide-*.html)")
    ap.add_argument("--formato", default="9:16",
                    choices=["9:16", "3:4", "4:5", "1:1"])
    ap.add_argument("--vertical", default="auto",
                    choices=["auto", "cybersec", "prog", "ai", "infra"],
                    help="Guía de auto-detección de íconos y del banco de copy "
                         "(default: auto, por slug)")
    ap.add_argument("--iconos", default="auto",
                    help="auto (default) o una categoría de icons/")
    ap.add_argument("--sin-placa", action="store_true",
                    help="iconos en modo clásico (sin placa duotono)")
    ap.add_argument("--fondo", default="auto", choices=list(_fondos.VARIANTES),
                    help="fondo del slide (auto = según rol y vertical)")
    ap.add_argument("--fondo-fijo", action="store_true",
                    help="mismo fondo en todos los slides (perfil contenido)")
    ap.add_argument("--componentes", default="auto",
                    help="auto o lista blanca separada por coma (QA)")
    ap.add_argument("--preset", default="mixto",
                    choices=["repo", "comandos", "python", "mixto"],
                    help="Receta de tipo de post: fija vertical + whitelist "
                         "de componentes (default: mixto, sin forzar)")
    ap.add_argument("--landing", default=None,
                    help="URL propia (ej: https://chmodxcode.pro). Activa el "
                         "cierre con landing: puente que invita a programar "
                         "y slide final con dominio como CTA primario "
                         "(los comandos siguen, en primer comentario)")
    ap.add_argument("--landing2", default=None,
                    help="Segunda URL del cierre (ej: canal de Telegram). "
                         "Agrega un botón secundario en el slide final")
    ap.add_argument("--landing2-texto", default=None,
                    help="Texto del botón secundario (default: ÚNETE AL TELEGRAM)")
    ap.add_argument("--marca", default=MARCA_DEFECTO)
    ap.add_argument("--display-tema", default=None)
    ap.add_argument("--short-tema", default=None)
    ap.add_argument("--badge", default=None)
    ap.add_argument("--cta-palabra", default=None)
    ap.add_argument("--cta-modo", default="seguir",
                    choices=["comentar", "seguir"],
                    help="comentar: botón 'Comenta X'; seguir: botón "
                         "'SÍGUENOS' con gatillo de valor")
    ap.add_argument("--hashtags", default=None)
    ap.add_argument("--resalte", default=None,
                    help="Color de las keywords (default: el mismo --color)")
    ap.add_argument("--solo-story", action="store_true")
    ap.add_argument("--solo-html", action="store_true",
                    help="Escribe los HTML finales sin renderizar PNG ni copy")
    ap.add_argument("--incremental", action="store_true",
                    help="Salta los slides cuyo HTML no cambió (reusa PNG)")
    ap.add_argument("--sin-autofit", action="store_true",
                    help="No ajusta el zoom automáticamente; solo avisa recortes")
    ap.add_argument("--workers", type=int, default=None,
                    help="Chromium en paralelo (default: núcleos-1, máx 4)")
    ap.add_argument("--contact-sheet", action="store_true",
                    help="Genera contact-sheet.png con todo el carrusel")
    ap.add_argument("--pdf", action="store_true",
                    help="Exporta el carrusel completo a PDF")
    ap.add_argument("--reel", action="store_true",
                    help="Exporta un MP4 (requiere ffmpeg instalado)")
    ap.add_argument("--copy-redes", action="store_true",
                    help="Genera también copy-redes.md (IG/TikTok/FB/Story)")
    ap.add_argument("--repo", default=None,
                    help="URL del repo (va al primer comentario de copy-redes)")
    ap.add_argument("--sin-guia", action="store_true",
                    help="No inyecta la card funnel del slide 2")
    ap.add_argument("--guia-titulo", default=None,
                    help="Título de la card funnel del slide 2")
    ap.add_argument("--guia-sub", default=None,
                    help="Subtítulo de la card funnel del slide 2")
    ap.add_argument("--offline", action="store_true",
                    help="No enlaza Google Fonts: render con fuentes locales")
    ap.add_argument("--no-auto", action="store_true",
                    help="No escribe slide-*.html si faltan (falla con aviso)")
    args = ap.parse_args()

    # ── Chromium en paralelo ──
    if args.workers and args.workers > 0:
        workers = min(args.workers, 8)
    else:
        workers = max(1, min(4, (os.cpu_count() or 2) - 1))

    # ── Color HEX (obligatorio, validado) ──
    try:
        hex_val = _colors.normalizar_hex(args.color)
    except ValueError as e:
        sys.exit(str(e))

    # ── Slides (obligatorio, validado) ──
    if args.slides < 3:
        sys.exit("--slides mínimo: 3 (1 portada + 1 contenido + 1 CTA). "
                 "Recomendado 7-10.")

    fmt = FORMATOS[args.formato]
    # Forzar input_dir a cwd si existen slides ya escritos
    cwd = Path.cwd()
    if (cwd / "slide-01.html").exists() or any(cwd.glob("slide-*.html")):
        input_dir = cwd
    else:
        input_dir = CTSLIDER / args.tema
    if not Image:
        sys.exit("PIL no está instalado: pip install pillow")

    marca = (args.marca or MARCA_DEFECTO).strip() or MARCA_DEFECTO
    tema_slug = Path(args.tema).name.lower()
    display = args.display_tema or args.tema.replace("-", " ").title()
    short = args.short_tema or display

    # ── Acento + resalte de keywords (antes del copy: el auto-copy usa
    #    el resalte para que las keywords del HTML fuente ya salgan del color)
    accent_vars = _colors.acento_vars(hex_val)
    try:
        resalte_hex = _colors.resuelve_resalte(args.resalte, hex_val)
    except ValueError as e:
        sys.exit(f"--resalte: {e}")
    aviso = _colors.avisar_contraste(resalte_hex)
    if aviso:
        print(f"  ! {aviso}")
    # El acento se usa en palabras clave, bordes y el CTA: avisa si se
    # apaga sobre el fondo del slide (basta AA-large 3:1).
    try:
        c_ac = _colors.contraste(hex_val, _colors.FONDO)
        if c_ac < 3.0:
            print(f"  ! Contraste bajo de --color {hex_val} sobre "
                  f"{_colors.FONDO}: {c_ac:.1f}:1 (< 3:1). Prueba un tono "
                  f"más claro para que el CTA y las keywords se lean en móvil.")
    except Exception:  # noqa: BLE001 - nunca bloquea el render
        pass
    rr, rg, rb = (int(resalte_hex.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    resalte_vars = {
        "__resalte__": resalte_hex,
        "__resalte_brillo__": f"#{min(255, int(rr + (255 - rr) * 0.45)):02x}"
                              f"{min(255, int(rg + (255 - rg) * 0.45)):02x}"
                              f"{min(255, int(rb + (255 - rb) * 0.45)):02x}",
        "__resalte_rgba32__": f"rgba({rr},{rg},{rb},0.32)",
        "__resalte_rgba38__": f"rgba({rr},{rg},{rb},0.38)",
    }

    # ── Vertical resuelta (auto → la decide el slug) ──
    vertical = None if args.vertical == "auto" else args.vertical

    # ── Preset de tipo de post: vertical + set de componentes ──
    if args.preset != "mixto":
        receta = PRESETS[args.preset]
        if args.vertical == "auto":
            args.vertical = receta["vertical"]
            vertical = receta["vertical"]
        if (args.componentes or "auto") == "auto":
            args.componentes = receta["componentes"]

    # ── Categoría de íconos ──
    from icons import CATEGORIAS as _CATS
    cat = args.iconos
    if cat == "auto":
        cat = detectar_categoria(tema_slug, display, short, vertical or "")
        if vertical:
            cat = {"cybersec": "cybersec", "prog": "dev",
                   "ai": "ai", "infra": "infra"}.get(vertical, cat)
    if cat not in _CATS:
        sys.exit(f"Categoría de íconos desconocida: {cat} "
                 f"(válidas: {', '.join(_CATS)})")

    # ── Fuente: slide-*.html existentes, o se escriben solos ──
    vertical_copy = vertical or _MAPA_VERTICAL.get(cat, "cybersec")
    permitidos_preset = None
    if (args.componentes or "auto") != "auto":
        permitidos_preset = {c.strip().lower()
                             for c in re.split(r"[,\s]+", args.componentes)
                             if c.strip()}
    slides = _slides_existentes(input_dir)
    if not slides:
        if args.no_auto:
            sys.exit(
                f"No hay slide-*.html en {input_dir}\n"
                f"  Dos opciones:\n"
                f"    · Sacá --no-auto: este mismo comando escribe el copy\n"
                f"      ({args.slides} slides, vertical {vertical_copy}) y sigue.\n"
                f"    · O crealos primero:\n"
                f"        python3 {SKILL_DIR / 'generar_copy_tech.py'} "
                f"--tema {tema_slug} --slides {args.slides} "
                f"--vertical {vertical_copy}")
        slides = _generar_slides_auto(input_dir, args.slides, vertical_copy,
                                      display, short, marca, tema_slug,
                                      resalte=resalte_hex,
                                      permitidos=permitidos_preset)
        if not slides:
            sys.exit(f"La auto-generación no escribió ningún slide en "
                     f"{input_dir}: revisá permisos de escritura.")
    n = len(slides)
    if n != args.slides:
        nombres = ", ".join(s.name for s in slides[:6])
        sys.exit(
            f"--slides {args.slides} no coincide: hay {n} archivo(s) "
            f"slide-*.html en {input_dir} ({nombres}"
            f"{', …' if n > 6 else ''}).\n"
            f"  Corregí los archivos o repetí con --slides {n}.")

    badge = args.badge or _palabra_clave(short, 1) or None
    cta = resolver_cta_palabra(tema_slug, forzado=args.cta_palabra)

    if args.hashtags:
        items = [h.lstrip("#").strip().lower().replace(" ", "")
                 for h in re.split(r"[,\s;]+", args.hashtags)]
        hashtags = " ".join(f"#{h}" for h in items if h)
    else:
        hashtags = _hashtags_tema(display, marca)

    slides = _slides_existentes(input_dir)
    n = len(slides)

    _fonts.set_offline(args.offline)

    # ── Fail-fast: props de componentes antes de tocar Chromium ──
    errores_props = []
    for src in slides:
        errores_props += validar_props(src.read_text(encoding="utf-8"), src.name)
    if errores_props:
        print("\n  ✗ data-props inválido en el slide fuente:")
        for e in errores_props:
            print(f"    {e}")
        sys.exit("\n  Corregí esos archivos y volvé a ejecutar el mismo comando.")

    print(f"\n  TechEdu Carousel — {input_dir.name}")
    print(f"  Color {hex_val}  ·  Slides {n}  ·  Formato {args.formato}  ·  "
          f"Categoría {cat}")
    print(f"  Marca {marca}  ·  Resalte {resalte_hex}  ·  Badge {badge}  ·  "
          f"CTA {cta}")
    if args.preset != "mixto":
        print(f"  Preset {args.preset}  ·  Componentes {args.componentes}")
    if args.landing:
        print(f"  Landing {_landing_dominio(args.landing)}  ·  "
              f"cierre enlaza al dominio propio")
    print(f"  Hashtags {hashtags}\n")

    if args.solo_story:
        isotipo = _tint_logo(hex_val)
        generar_story(input_dir, display, resalte_hex, isotipo, accent_vars, marca)
        return

    isotipo = _tint_logo(hex_val)
    final_dir = input_dir / "renders"
    final_dir.mkdir(parents=True, exist_ok=True)

    permitidos = None
    if args.componentes and args.componentes != "auto":
        permitidos = {c.strip().lower()
                      for c in re.split(r"[,\s]+", args.componentes) if c.strip()}

    warnings = []
    try:
        import generar_copy_tech as _gct
        comandos_finales = _gct.extraer_comandos(input_dir)
    except Exception:
        comandos_finales = []
    # Títulos de los slides de contenido (2..N-2) para el puente-recap
    recap_titulos = []
    try:
        for src in slides[1:n - 2]:
            recap_titulos.append(
                _texto_titulo(parse_slide(src).get("body", "")))
    except Exception:
        recap_titulos = []
    usados_iconos = set()
    for i, src in enumerate(slides, 1):
        data = parse_slide(src)
        slide_warnings = []
        # Icono semántico: el texto del slide (título, cuerpo y props de los
        # componentes) decide el glyph; si no matchea, cae al rol.
        texto_ico = re.sub(r'data-component="[^"]*"', " ",
                           data.get("body", ""))
        nombre_ico, icono = elegir_icono(
            i, n, accent_vars, tema=cat, texto=texto_ico,
            usados=usados_iconos)
        if nombre_ico:
            usados_iconos.add(nombre_ico)
        html = generar_html(i, n, data, args.formato, fmt, accent_vars,
                            isotipo, marca,
                            icono=icono, badge=badge, cta_palabra=cta,
                            resalte_vars=resalte_vars, semilla=tema_slug,
                            warnings=slide_warnings,
                            guia=not args.sin_guia,
                            guia_titulo=args.guia_titulo,
                            guia_sub=args.guia_sub,
                            comandos_finales=comandos_finales,
                            cta_modo=args.cta_modo,
                            recap_titulos=recap_titulos,
                            landing=args.landing,
                            landing2=args.landing2,
                            landing2_texto=args.landing2_texto,
                            plano=args.sin_placa,
                            categoria=cat,
                            fondo=args.fondo,
                            fondo_fijo=args.fondo_fijo)
        if permitidos is not None:
            for w in slide_warnings:
                if "componente" in w and not any(
                        p in w.lower() for p in permitidos):
                    slide_warnings.append(
                        f"componente fuera de la lista --componentes: {w}")
        warnings += [f"slide {i}: {w}" for w in slide_warnings]
        out = final_dir / f"slide-{i:02d}.html"
        out.write_text(html, encoding="utf-8")
        print(f"  OK HTML {out.name}")

    if warnings:
        print("\n  Avisos:")
        for w in warnings:
            print(f"    ! {w}")

    nombres_html = [f"slide-{i:02d}.html" for i in range(1, n + 1)]
    print("\n  Midiendo títulos para la regla de keywords...")
    ajustar_claves_por_lineas(final_dir, nombres_html, fmt["w"], fmt["h"])

    # ── Auto-fit: baja el zoom del contenido hasta que nada recorte ──
    if not args.sin_autofit:
        print("\n  Auto-fit del contenido (mide y ajusta zoom)...")
        sobra = autoajustar_recortes(final_dir, nombres_html, fmt["w"], fmt["h"],
                                     workers=workers)
        if sobra:
            for nombre, px in sorted(sobra.items()):
                print(f"    ! {nombre}: sigue recortando {px}px (piso de zoom "
                      f"alcanzado; acorta el copy de ese slide).")
        else:
            print("  ✓ Sin recortes: todo el contenido cabe en el lienzo.")
    else:
        print("\n  Verificando que nada quede recortado...")
        recortes = chequear_overflow(final_dir, nombres_html, fmt["w"], fmt["h"],
                                     workers=workers)
        if recortes:
            print("  Avisos de recorte:")
            for nombre, px in recortes:
                if px < 0:
                    print(f"    ! {nombre}: no se pudo medir el recorte.")
                else:
                    print(f"    ! {nombre}: {px}px de contenido recortadas.")
        else:
            print("  ✓ Sin recortes: todo el contenido cabe en el lienzo.")

    if args.solo_html:
        print("\n  ✓ HTML listos (--solo-html: sin PNG, story ni copy).")
        print(f"\n  Salida: {input_dir}")
        return

    print(f"\n  Renderizando ({workers} en paralelo)...")
    preview = input_dir / "preview"
    fallidos = renderizar_paralelo(
        [final_dir / nombre for nombre in nombres_html], preview,
        fmt["w"], fmt["h"], workers=workers, reusar=args.incremental)

    if args.contact_sheet:
        print("\n  Armando contact sheet...")
        generar_contact_sheet(input_dir, nombres_html, fmt)
    if args.pdf:
        print("\n  Exportando PDF...")
        exportar_pdf(input_dir, nombres_html, fmt)
    if args.reel:
        print("\n  Exportando reel MP4...")
        exportar_reel(input_dir, nombres_html, fmt)

    avisos_rep = qa_repeticion(input_dir, nombres_html)
    if avisos_rep:
        print("\n  ! QA de repetición:")
        for a in avisos_rep:
            print(f"    - {a}")

    generar_story(input_dir, display, resalte_hex, isotipo, accent_vars, marca)
    escribir_caption(input_dir, display, cta, hashtags, marca,
                     modo=args.cta_modo, landing=args.landing,
                     landing2=args.landing2, landing2_texto=args.landing2_texto)

    if args.copy_redes:
        from generar_copy_tech import generar_copy_redes
        print("\n  Generando copy-redes.md...")
        generar_copy_redes(input_dir, display, short, marca, cta_palabra=cta,
                           repo=args.repo, vertical=cat,
                           cta_modo=args.cta_modo,
                           landing=args.landing,
                           landing2=args.landing2,
                           landing2_texto=args.landing2_texto)

    print(f"\n  Salida: {input_dir}")
    if fallidos:
        print(f"\n  ✗ INCOMPLETO: {len(fallidos)} de {n} PNG(s) no se "
              f"renderizaron ({', '.join(fallidos)}).")
        print("    Vuelve a lanzar el comando: los HTML ya están correctos.")
        sys.exit(1)


if __name__ == "__main__":
    main()
