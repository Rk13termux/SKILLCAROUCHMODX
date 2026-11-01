#!/usr/bin/env python3
"""Regenera la muestra visual de TODOS los componentes.

Lee `MANIFEST.json` (componente → props), arma carruseles de 8 slides en
$CTSLIDER/_catalogo-N, los renderiza con `tech_carousel.py --workers 1` y
compone `componentes.png` (una miniatura por componente con su nombre).

Uso:
    python3 componentes-test/regenerar.py            # todo
    python3 componentes-test/regenerar.py --solo-html # no renderiza (debug)
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SKILL = AQUI.parent
sys.path.insert(0, str(SKILL))

from utils.render import resolver_ctslider  # noqa: E402

SLIDE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  .titulo {{ font-weight: 700; }}
  .cuerpo {{ font-weight: 400; }}
  .clave {{ font-weight: 700; color: #06B6D4; }}
</style>
</head>
<body>
  <div class="numero">{i}/{n}</div>
  <div class="slide">
    <div class="contenido">
      <div class="titulo">Componente: <span class="clave">{comp}</span></div>
      <div class="cuerpo">Muestra de referencia del componente gráfico.</div>
      <div class="componente" data-component="{comp}" data-props='{props}'></div>
    </div>
    <div class="pie">
      <span class="logo"></span>CHMODX · Catálogo
    </div>
  </div>
</body>
</html>
"""

CIERRE = """<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"><style>*{{margin:0;padding:0;box-sizing:border-box}}</style></head>
<body>
  <div class="numero">{i}/{n}</div>
  <div class="slide"><div class="contenido">
    <div class="titulo">{t}</div>
    <div class="cuerpo">Slide fijo del builder.</div>
  </div><div class="pie"><span class="logo"></span>CHMODX · Catálogo</div></div>
</body>
</html>
"""

PORTADA = """<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}} .titulo{{font-weight:700}} .cuerpo{{font-weight:400}}
.clave{{font-weight:700;color:#06B6D4}}
</style></head>
<body>
  <div class="numero">1/{n}</div>
  <div class="slide"><div class="contenido">
    <div class="titulo">Catálogo de <span class="clave">componentes</span> gráficos</div>
    <div class="cuerpo">Referencia visual de las piezas del builder.</div>
  </div><div class="pie"><span class="logo"></span>CHMODX · Catálogo</div></div>
</body>
</html>
"""


def escribir_tema(base: Path, comps, indice: int):
    # Slide 1 = portada fija: si un componente cae en el slide 1, el builder
    # reemplaza el título por un hook y la muestra deja de ser neutra.
    n = len(comps) + 3
    base.mkdir(parents=True, exist_ok=True)
    for viejo in base.glob("slide-*.html"):
        viejo.unlink()
    (base / "slide-01.html").write_text(PORTADA.format(n=n), encoding="utf-8")
    for i, (comp, props) in enumerate(comps, 2):
        props_txt = json.dumps(props, ensure_ascii=False).replace("'", "&#39;")
        (base / f"slide-{i:02d}.html").write_text(
            SLIDE.format(i=i, n=n, comp=comp, props=props_txt),
            encoding="utf-8")
    for i in (n - 1, n):
        (base / f"slide-{i:02d}.html").write_text(
            CIERRE.format(i=i, n=n, t="Cierre" if i == n else "Resumen"),
            encoding="utf-8")
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--solo-html", action="store_true",
                    help="arma los slides sin renderizar PNG")
    args = ap.parse_args()

    manifiesto = json.loads((AQUI / "MANIFEST.json").read_text(encoding="utf-8"))
    comps = manifiesto["muestras"]
    raiz = resolver_ctslider()

    grupos = [comps[i:i + 8] for i in range(0, len(comps), 8)]
    pngs = []
    for k, grupo in enumerate(grupos, 1):
        tema = f"_catalogo-{k}"
        carpeta = raiz / tema
        n = escribir_tema(carpeta, grupo, k)
        print(f"[{k}/{len(grupos)}] {tema}: {n} slides "
              f"({', '.join(c for c, _ in grupo)})")
        if args.solo_html:
            continue
        cmd = [sys.executable, str(SKILL / "tech_carousel.py"),
               "--tema", tema, "--color", "#06B6D4", "--slides", str(n),
               "--vertical", "cybersec", "--no-auto", "--workers", "1"]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout[-1500:], r.stderr[-1500:])
            raise SystemExit(f"falló el render de {tema}")
        for i, (comp, _props) in enumerate(grupo, 2):
            pngs.append((comp, carpeta / "preview" / f"slide-{i:02d}.png"))

    if args.solo_html:
        return

    from PIL import Image, ImageDraw
    TH, COLS, GAP, LBL, M = 230, 8, 10, 26, 18
    h = round(1920 * TH / 1080)
    filas = (len(pngs) + COLS - 1) // COLS
    W = M * 2 + COLS * TH + (COLS - 1) * GAP
    H = M * 2 + filas * (h + LBL) + (filas - 1) * GAP
    hoja = Image.new("RGB", (W, H), (8, 8, 12))
    d = ImageDraw.Draw(hoja)
    for idx, (nombre, ruta) in enumerate(pngs):
        if not ruta.exists():
            print(f"  ! falta {ruta}")
            continue
        f, c = divmod(idx, COLS)
        x = M + c * (TH + GAP)
        y = M + f * (h + LBL + GAP)
        im = Image.open(ruta).convert("RGB").resize((TH, h), Image.LANCZOS)
        hoja.paste(im, (x, y + LBL))
        d.text((x + 2, y + 8), nombre, fill=(90, 220, 230))
    salida = AQUI / "componentes.png"
    hoja.save(salida)
    print(f"\n✓ {len(pngs)} componentes -> {salida}")


if __name__ == "__main__":
    main()
