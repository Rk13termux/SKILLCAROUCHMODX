"""Cielo estrellado: capa de fondo con profundidad."""

import re

from tech_carousel import FORMATOS, STORY_TEMPLATE, TEMPLATE, generar_html
from theme import colors as _colors
from theme import stars

KW = {"__resalte__": "#06B6D4", "__resalte_brillo__": "#3DD2EE",
      "__resalte_rgba32__": "rgba(6,182,212,0.32)",
      "__resalte_rgba38__": "rgba(6,182,212,0.38)"}


def _html_slide(i=2, n=4, fmt_key="9:16"):
    data = {"number": f"{i}/{n}",
            "body": '<div class="titulo">Titular <span class="clave">clave'
                    "</span></div><div class=\"cuerpo\">Cuerpo de prueba.</div>",
            "footer": "TechEdu · demo"}
    return generar_html(i, n, data, fmt_key, FORMATOS[fmt_key],
                        _colors.acento_vars("#06B6D4"), None, "TechEdu",
                        resalte_vars=KW, semilla="demo")


def test_css_es_determinista():
    a, b = stars.css_estrellas(), stars.css_estrellas()
    assert a == b
    assert a != stars.css_estrellas(semilla=1)


def test_capa_tiene_viñeta_mas_estrellas():
    css = stars.css_estrellas()
    assert css.startswith("radial-gradient(ellipse")   # viñeta arriba de todo
    assert css.count("radial-gradient") >= 70
    assert "rgba(255,255,255,0.92)" in css              # estrellas brillantes
    # posición en % → el mismo CSS sirve en cualquier formato
    for x, y in re.findall(r"at (\d+\.\d+)% (\d+\.\d+)%", css):
        assert 0 < float(x) < 100 and 0 < float(y) < 100


def test_template_de_slide_usa_el_token():
    for tok in ("__fondo_img__", "__textura_img__", "__textura_size__",
                "__textura_mask__", "__textura_op__", "__fondo_codigo__"):
        assert tok in TEMPLATE, tok
    assert ".slide::before" in TEMPLATE and ".slide::after" in TEMPLATE
    # el fondo va por debajo de `.slide > *` (z-index 1) para no tapar el contenido
    assert TEMPLATE.index(".slide::before") < TEMPLATE.index(
        ".slide > * { position: relative; z-index: 1; }")
    # el código fantasma queda detrás del contenido (z-index negativo)
    assert "z-index: -1" in TEMPLATE


def test_template_de_story_tambien_tiene_estrellas():
    assert "__estrellas__" in STORY_TEMPLATE
    bloque = STORY_TEMPLATE.split(".story {")[1].split("}")[0]
    fondo = bloque.split("background:")[1].split(";")[0]
    assert "__estrellas__" in fondo and "#0B0B0D" in fondo


def test_slide_generado_no_deja_tokens_sin_reemplazar():
    html = _html_slide()
    for tok in ("__fondo_img__", "__textura_img__", "__textura_size__",
                "__textura_mask__", "__textura_op__", "__fondo_codigo__"):
        assert tok not in html, tok
    assert "__resalte__" not in html
    assert "__accent__" not in html
    assert html.count("radial-gradient") >= 70
    assert "color: var(--resalte)" in html


def test_estrellas_en_los_cuatro_formatos():
    for fmt_key in FORMATOS:
        html = _html_slide(fmt_key=fmt_key)
        assert html.count("radial-gradient") >= 70, fmt_key
        assert f"width: {FORMATOS[fmt_key]['w']}px" in html
