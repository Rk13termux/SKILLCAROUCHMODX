"""Validación de data-props (fail-fast antes de tocar Chromium)."""

import json

import pytest

from components import expandir
from tech_carousel import validar_props


def _slide(componente, props):
    return ('<div class="contenido">\n'
            f'  <div class="componente" data-component="{componente}" '
            f"data-props='{json.dumps(props, ensure_ascii=False)}'></div>\n"
            '</div>\n<div class="pie">')


def test_props_validos_no_reportan():
    assert validar_props(_slide("diagram", {"nodos": [{"v": "a"}]}),
                         "slide-01.html") == []


def test_props_rotos_reportan_slide_componente_y_ubicacion():
    html = '<div class="componente" data-component="code" ' \
           "data-props='{\"codigo\": }'></div>"
    errores = validar_props(html, "slide-07.html")
    assert len(errores) == 1
    err = errores[0]
    assert "slide-07.html" in err
    assert '"code"' in err
    assert "línea" in err and "JSON inválido" in err


def test_props_vacios_no_son_error():
    """Sin data-props el JSON se lee del interior: no hay nada que validar."""
    assert validar_props('<div class="componente" data-component="social"></div>',
                         "slide-02.html") == []


def test_varios_componentes_acumulan_errores():
    html = ('<div class="componente" data-component="a" data-props="{"></div>'
            '<div class="componente" data-component="b" data-props="{"></div>')
    assert len(validar_props(html, "slide-03.html")) == 2


def test_render_tolera_json_roto_con_aviso():
    """Si alguien se salta la validación, el slide no debe morir."""
    avisos = []
    html, usados = expandir(
        '<div class="componente" data-component="social" '
        "data-props='{\"titulo\": }'></div>",
        {"accent": "#06B6D4"}, avisos)
    assert usados == ["social"]
    assert avisos and "JSON inválido" in avisos[0]
    assert "comp-error" in html
