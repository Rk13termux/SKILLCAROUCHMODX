#!/usr/bin/env python3
"""Comparador de fondos: renderiza una variante por fila y arma un contact-sheet.

Sirve para ELEGIR el fondo mirando: cada fila es una variante de `--fondo` y
cada columna un rol de slide (portada / contenido / puente / cierre).

Uso:
    python3 comparar_fondos.py                       # todas las variantes, dev
    python3 comparar_fondos.py --verticales          # 1 fila por vertical (auto)
    python3 comparar_fondos.py --solo grid mesh codigo
    python3 comparar_fondos.py --accent "#06B6D4" --destino /ruta/salida

Salida por defecto: /sdcard/CTSLIDER/_comparador-fondos/
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ))

from theme import fondos as _fondos  # noqa: E402

TEMA = "fondo-cmp"
ROLES = ("Portada", "Contenido", "Puente", "Cierre")

# Textos de prueba: título + cuerpo con keyword y un componente real.
FUENTES = (
    ("<div class='titulo'>Por qué tu script de Python se cae en producción"
     "</div><div class='cuerpo'>Un <span class='clave'>error</span> silencioso "
     "y cómo cazarlo antes de que rompa todo.</div>"
     "<div class='componente' data-component='card-info' data-props="
     "'{\"variante\": \"warn\", \"titulo\": \"Cuidado\", "
     "\"cuerpo\": \"El proceso muere sin log.\"}'>x</div>"),
    ("<div class='titulo'>Detecta la fuga antes que el atacante</div>"
     "<div class='cuerpo'>Tu <span class='clave'>correo</span> puede estar en "
     "una brecha de datos y no lo sabes.</div>"
     "<div class='componente' data-component='terminal' data-props="
     "'{\"titulo\": \"chequeo\", \"lines\": [{\"t\": \"cmd\", "
     "\"v\": \"python3 brecha.py --correo tu@mail.com\"}]}'>x</div>"),
    ("<div class='titulo'>Todo lo que vimos, en una sola pantalla</div>"
     "<div class='cuerpo'>Repaso rápido de los puntos que más pesan.</div>"
     "<div class='componente' data-component='checklist' data-props="
     "'{\"titulo\": \"Pasos\", \"items\": [\"Instala\", \"Configura\", "
     "\"Verifica\"]}'>x</div>"),
    ("<div class='titulo'>Empieza hoy con el curso completo</div>"
     "<div class='cuerpo'>En el primer comentario está el enlace al "
     "<span class='clave'>curso</span>.</div>"),
)


def escribir_fuentes(destino: Path):
    destino.mkdir(parents=True, exist_ok=True)
    for i, cuerpo in enumerate(FUENTES, 1):
        (destino / f"slide-{i:02d}.html").write_text(f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><style>
.titulo {{ font-weight: 700; }} .cuerpo {{ font-weight: 400; }}
.clave {{ font-weight: 700; color: #CC3300; }}
</style></head><body>
  <div class="numero">{i}/4</div>
  <div class="slide"><div class="contenido">
    {cuerpo}
  </div><div class="pie"><span class="logo"></span>CHMODX · demo</div></div>
</body></html>""", encoding="utf-8")


def renderizar(base: Path, variante: str, vertical: str, accent: str,
               etiqueta: str = None) -> list:
    """Corre el builder con --fondo <variante> y devuelve los PNG copiados.

    Cada corrida reescribe `preview/`, así que los PNG se copian a
    `base/shots/<variante>-NN.png` antes de lanzar la siguiente.
    """
    shots = base / "shots"
    shots.mkdir(parents=True, exist_ok=True)
    copiados = [shots / f"{etiqueta or variante}-{i:02d}.png"
                for i in range(1, len(FUENTES) + 1)]
    # Reanudable: si ya están los 4 PNG, no se vuelve a renderizar.
    if all(p.exists() for p in copiados):
        print(f"    · {etiqueta or variante}: ya renderizado")
        return copiados
    cmd = [sys.executable, str(RAIZ / "tech_carousel.py"),
           "--tema", TEMA, "--color", accent, "--slides", str(len(FUENTES)),
           "--formato", "9:16", "--vertical", vertical, "--marca", "CHMODX",
           "--fondo", variante, "--workers", "2", "--no-auto", "--sin-guia"]
    env = dict(os.environ, CTSLIDER_DIR=str(base))
    r = subprocess.run(cmd, cwd=str(RAIZ), env=env, capture_output=True,
                       text=True, timeout=900)
    if r.returncode != 0:
        print(f"    ! falló {variante}: {r.stderr.strip()[-300:]}")
        return []
    for i, dst in enumerate(copiados, 1):
        src = base / TEMA / "preview" / f"slide-{i:02d}.png"
        if not src.exists():
            print(f"    ! falta slide {i} de {variante}")
            return []
        shutil.copy2(src, dst)
    return copiados


def _fuente(tam):
    from PIL import ImageFont

    for cand in ("DejaVuSans-Bold.ttf",
                 "/system/fonts/Roboto-Bold.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(cand, tam)
        except Exception:
            continue
    return ImageFont.load_default()


def hoja(filas, destino: Path, ancho_tile=270, etiqueta=170):
    """filas = [(titulo, [png, png, png, png]), ...]"""
    from PIL import Image, ImageDraw

    if not filas:
        return None
    con_png = [f for f in filas if f[1]]
    if not con_png:
        print("  ! ninguna variante renderizó")
        return None
    o = Image.open(con_png[0][1][0])
    alto_tile = int(ancho_tile * o.height / o.width)
    cab = 64
    hoja = Image.new("RGB", (etiqueta + ancho_tile * len(ROLES),
                             cab + alto_tile * len(filas)), "#0A0A0C")
    d = ImageDraw.Draw(hoja)
    f_tit = _fuente(30)
    f_rol = _fuente(22)
    for c, rol in enumerate(ROLES):
        d.text((etiqueta + c * ancho_tile + 16, 20), rol, fill="#FACC15",
               font=f_rol)
    for f, (titulo, pngs) in enumerate(filas):
        y = cab + f * alto_tile
        d.text((20, y + 20), titulo, fill="#FFFFFF", font=f_tit)
        for c, png in enumerate(pngs[:len(ROLES)]):
            if not png or not Path(png).exists():
                continue
            im = Image.open(png).convert("RGB")
            im = im.resize((ancho_tile, alto_tile), Image.LANCZOS)
            hoja.paste(im, (etiqueta + c * ancho_tile, y))
        d.line([(0, y), (hoja.width, y)], fill="#26262B")
    destino.parent.mkdir(parents=True, exist_ok=True)
    hoja.save(destino, optimize=True)
    return destino


def zona_vacia(png, lado):
    """Bloque `lado`×`lado` con menos varianza (donde no hay texto)."""
    from PIL import Image, ImageStat

    g = Image.open(png).convert("L")
    mejor, mejor_v = (0, 0), 1e9
    paso = 40
    for y in range(0, g.height - lado, paso):
        for x in range(0, g.width - lado, paso):
            v = ImageStat.Stat(g.crop((x, y, x + lado, y + lado))).stddev[0]
            if v < mejor_v:
                mejor_v, mejor = v, (x, y)
    return mejor


def hoja_detalles(base: Path, destino: Path, variantes, lado=400):
    """Grilla de recortes 1:1: así sí se ve la textura real, sin reescalado."""
    from PIL import Image, ImageDraw

    shots = base / "shots"
    ref = shots / "base-02.png"
    if not ref.exists():
        ref = next(iter(sorted(shots.glob("*-02.png"))), None)
        if ref is None:
            print("  ! sin recortes de referencia")
            return None
    x, y = zona_vacia(ref, lado)
    titulos = []
    for v in variantes:
        p = shots / f"{v}-02.png"
        if p.exists():
            titulos.append((v, p))
    if not titulos:
        return None
    sep, cab, etiq = 10, 56, 150
    hoja = Image.new("RGB",
                     (etiq + len(titulos) * (lado + sep), cab + lado + 40),
                     "#0A0A0C")
    d = ImageDraw.Draw(hoja)
    f = _fuente(24)
    d.text((12, 14), f"detalle 1:1 · recorte {lado}×{lado} en ({x},{y})",
           fill="#FACC15", font=f)
    for i, (v, p) in enumerate(titulos):
        im = Image.open(p).convert("RGB").crop((x, y, x + lado, y + lado))
        px = etiq + i * (lado + sep)
        hoja.paste(im, (px, cab))
        d.text((px + 6, cab + lado + 10), v, fill="#FFFFFF", font=f)
    destino.parent.mkdir(parents=True, exist_ok=True)
    hoja.save(destino, optimize=True)
    return destino


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--accent", default="#FACC15")
    ap.add_argument("--destino", default="/sdcard/CTSLIDER/_comparador-fondos")
    ap.add_argument("--base", default="/tmp/opencode/fondo-cmp")
    ap.add_argument("--solo", nargs="*", default=None)
    ap.add_argument("--verticales", action="store_true",
                    help="en vez de variantes, 1 fila por vertical con fondo auto")
    ap.add_argument("--detalles", action="store_true",
                    help="hoja de recortes 1:1 (sólo compone, no renderiza)")
    ap.add_argument("--lado", type=int, default=400,
                    help="lado del recorte 1:1 (default 400)")
    ap.add_argument("--vertical", default="prog",
                    choices=["cybersec", "prog", "ai", "infra"])
    args = ap.parse_args(argv)

    base = Path(args.base)
    tema_dir = base / TEMA
    shutil.rmtree(tema_dir, ignore_errors=True)
    escribir_fuentes(tema_dir)
    salida = Path(args.destino)
    salida.mkdir(parents=True, exist_ok=True)

    filas = []
    if args.detalles:
        # sólo compone: usa los recortes ya renderizados (no lanza Chromium)
        variantes = args.solo or [f"{v}-02" for v in _fondos.VARIANTES]
        variantes = [v[:-3] if v.endswith("-02") else v for v in variantes]
        destino = salida / "detalles-1a1.png"
        if hoja_detalles(base, destino, variantes, lado=args.lado):
            print(f"\n  ✓ {destino}")
            return 0
        print("  ! no hay recortes; corré primero el comparador")
        return 1

    if args.verticales:
        verticales = args.solo or ["cybersec", "prog", "ai", "infra"]
        for v in verticales:
            print(f"· vertical {v} (auto)")
            pngs = renderizar(base, "auto", v, args.accent, etiqueta=f"auto-{v}")
            filas.append((f"auto · {v}", pngs))
        # la hoja final se arma con TODOS los verticales disponibles
        filas = [(f"auto · {v}",
                  [base / "shots" / f"auto-{v}-{i:02d}.png"
                   for i in range(1, len(FUENTES) + 1)])
                 for v in ["cybersec", "prog", "ai", "infra"]]
        destino = salida / "comparador-verticales.png"
    else:
        variantes = args.solo or list(_fondos.VARIANTES)
        for v in variantes:
            print(f"· fondo {v}")
            pngs = renderizar(base, v, args.vertical, args.accent)
            filas.append((v, pngs))
        destino = salida / "comparador-fondos.png"

    hoja(filas, destino)
    print(f"\n  ✓ {destino}")
    print(f"  (tiles sueltos en {base / TEMA / 'preview'})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
