"""Portada auto-medida y revisión de arte sobre el PNG.

El título de portada ya no es un factor fijo: se mide en Chromium el mayor
que cabe. La revisión de arte vigila bordes y contraste del PNG final.
"""

import pytest

import tech_carousel as tc

HTML_PORTADA = """<!DOCTYPE html>
<html><head><style>
  .slide.cover .titulo {
    font-size: 112px;
    line-height: 1.04;
  }
  .ajuste {
    display: flex;
    flex-direction: column;
    zoom: 0.94;
  }
</style></head><body>
  <div class="slide cover"><div class="contenido">
    <div class="ajuste"><div class="titulo">Hola</div></div>
  </div></div>
</body></html>"""


class _Resultado:
    def __init__(self, stdout=""):
        self.returncode = 0
        self.stdout = stdout
        self.stderr = ""


# ── Título de portada medido ───────────────────────────────────────

def test_titulo_portada_elige_el_mayor_y_resetea_el_zoom(tmp_path, monkeypatch):
    (tmp_path / "slide-01.html").write_text(HTML_PORTADA, encoding="utf-8")
    visto = {}

    def falso(cmd, **_kw):
        # La sonda se escribe antes de llamar: la leemos aquí.
        probe = next((a for a in cmd if str(a).startswith("file://")), "")
        from pathlib import Path
        visto["sonda"] = Path(str(probe).replace("file://", "")).read_text(
            encoding="utf-8") if probe else ""
        return _Resultado(stdout='<html>data-tam="127"</html>')

    monkeypatch.setattr(tc, "_correr_chromium", falso)
    elegido = tc.ajustar_titulo_portada(tmp_path, "9:16")

    assert elegido == 127
    salida = (tmp_path / "slide-01.html").read_text(encoding="utf-8")
    assert "font-size: 127px" in salida
    # El zoom viejo no debe sobrevivir a la remedición.
    assert "zoom: 0.94" not in salida


def test_titulo_portada_barre_candidatos_de_max_a_min(tmp_path, monkeypatch):
    (tmp_path / "slide-01.html").write_text(HTML_PORTADA, encoding="utf-8")
    visto = {}

    def falso(cmd, **_kw):
        from pathlib import Path
        probe = Path(str(next(a for a in cmd if str(a).startswith("file://")))
                     .replace("file://", ""))
        visto["html"] = probe.read_text(encoding="utf-8")
        return _Resultado(stdout='data-tam="120"')

    monkeypatch.setattr(tc, "_correr_chromium", falso)
    tc.ajustar_titulo_portada(tmp_path, "9:16")

    import json
    casos = json.loads(visto["html"].split('id="tam-casos" hidden>')[1]
                       .split("</pre>")[0])
    base = tc._format_scaling("9:16")["__title_size__"]
    assert casos == sorted(casos, reverse=True)          # de mayor a menor
    assert casos[0] == round(base * tc.TITULO_PORTADA_MAX)
    assert casos[-1] >= round(base * tc.TITULO_PORTADA_MIN)
    assert "data-tam" in visto["html"]                   # script inyectado


def test_titulo_portada_sin_regla_devuelve_none(tmp_path, monkeypatch):
    (tmp_path / "slide-01.html").write_text("<html><body>x</body></html>",
                                           encoding="utf-8")
    monkeypatch.setattr(tc, "_correr_chromium",
                        lambda *_a, **_k: _Resultado(stdout="nada"))
    assert tc.ajustar_titulo_portada(tmp_path, "9:16") is None


def test_titulo_portada_sin_archivo_devuelve_none(tmp_path):
    assert tc.ajustar_titulo_portada(tmp_path, "9:16") is None


def test_titulo_portada_si_no_cabe_ninguno_no_toca_el_html(tmp_path, monkeypatch):
    (tmp_path / "slide-01.html").write_text(HTML_PORTADA, encoding="utf-8")
    monkeypatch.setattr(tc, "_correr_chromium",
                        lambda *_a, **_k: _Resultado(stdout='data-tam="0"'))
    assert tc.ajustar_titulo_portada(tmp_path, "9:16") is None
    assert "font-size: 112px" in (tmp_path / "slide-01.html").read_text(
        encoding="utf-8")


# ── Revisión de arte (PNG sintéticos) ──────────────────────────────

Image = pytest.importorskip("PIL.Image")


def _png(path, fondo, caja, valor=255, tam=(400, 700)):
    im = Image.new("L", tam, fondo)
    for y in range(caja[1], caja[3]):
        for x in range(caja[0], caja[2]):
            im.putpixel((x, y), valor)
    im.convert("RGB").save(path)


def test_arte_detecta_tinta_pegada_al_borde(tmp_path):
    _png(tmp_path / "slide-01.png", 11, (100, 5, 300, 200))     # toca arriba
    _png(tmp_path / "slide-02.png", 11, (100, 300, 300, 640))   # centrada
    avisos, resumen = tc.revisar_arte(tmp_path, ["slide-01.png",
                                                 "slide-02.png"])
    assert any("borde superior" in a for a in avisos)
    assert not any("slide-02" in a for a in avisos)
    assert "tinta desde" in resumen


def test_arte_detecta_contraste_bajo(tmp_path):
    # Fondo medio y tinta apenas más clara: contraste < 3:1.
    _png(tmp_path / "slide-01.png", 120, (100, 300, 300, 400), valor=150)
    avisos, _ = tc.revisar_arte(tmp_path, ["slide-01.png"])
    assert any("contraste" in a for a in avisos)


def test_arte_sin_pngs_no_avisa(tmp_path):
    assert tc.revisar_arte(tmp_path, ["slide-01.png"]) == ([], "")


def test_arte_imagen_limpia_no_avisa(tmp_path):
    _png(tmp_path / "slide-01.png", 11, (150, 250, 250, 450))
    avisos, resumen = tc.revisar_arte(tmp_path, ["slide-01.png"])
    assert avisos == []
    assert "contraste mín" in resumen
