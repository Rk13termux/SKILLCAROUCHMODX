"""Escalado por formato (bug B2 + ajustes de shell).

Los componentes se miden en `em`: sin `__comp_base__` en `.comp-wrap` heredan
los 16px del navegador y el texto sale a mitad de tamaño.
"""

import pytest

from tech_carousel import _format_scaling
from theme import tokens

FORMATOS = ["9:16", "4:5", "3:4", "1:1"]


@pytest.mark.parametrize("fmt", FORMATOS)
def test_comp_base_presente_y_grande(fmt):
    sc = _format_scaling(fmt)
    assert sc["__comp_base__"] >= 40


@pytest.mark.parametrize("fmt", FORMATOS)
def test_texto_efectivo_de_componente_minimo(fmt):
    """comp_base × zoom ≥ 32px de diseño (12 CSS px)."""
    sc = _format_scaling(fmt)
    assert round(sc["__comp_base__"] * sc["__comp_zoom__"]) >= 32


def test_zoom_por_formato():
    assert _format_scaling("9:16")["__comp_zoom__"] == 1.0
    assert _format_scaling("4:5")["__comp_zoom__"] == 0.80
    assert _format_scaling("3:4")["__comp_zoom__"] == 0.80
    assert _format_scaling("1:1")["__comp_zoom__"] == 0.72


def test_cuerpo_del_slide():
    assert _format_scaling("9:16")["__body_size__"] == 44
    assert 34 <= _format_scaling("1:1")["__body_size__"] <= 40


def test_chip_swipe_por_formato():
    """El chip no puede pisar el pie: se achica y en 1:1 se oculta."""
    assert _format_scaling("9:16")["__ind_disp__"] == "inline-flex"
    assert _format_scaling("9:16")["__ind_h__"] == 72
    assert _format_scaling("4:5")["__ind_h__"] <= 56
    assert _format_scaling("3:4")["__ind_h__"] <= 54
    assert _format_scaling("1:1")["__ind_disp__"] == "none"


def test_formatos_cortos_aligeran_el_shell():
    """Ganan espacio con padding/ícono/título, nunca achicando el texto."""
    largo, corto = _format_scaling("9:16"), _format_scaling("4:5")
    assert corto["__pad_top__"] < largo["__pad_top__"]
    assert corto["__icon_size__"] < largo["__icon_size__"]
    assert corto["__title_size__"] >= 60
    assert corto["__body_size__"] >= 36


def test_badge_y_cta_legibles():
    for fmt in FORMATOS:
        assert _format_scaling(fmt)["__badge_size__"] >= 26


def test_css_de_componentes_usa_los_tokens():
    """Guardia B2: si alguien saca los tokens, el texto vuelve a 16px."""
    from tech_carousel import TEMPLATE

    assert ".comp-wrap" in tokens.COMPONENTES_CSS
    assert "font-size: __comp_base__px" in tokens.COMPONENTES_CSS
    assert "min-height: __ind_h__px" in TEMPLATE
    assert "display: __ind_disp__" in TEMPLATE
    assert "font-size: 72px" not in TEMPLATE
    assert ".slide {" in TEMPLATE and "__body_size__" in TEMPLATE


@pytest.mark.parametrize("fmt", FORMATOS)
def test_todos_los_formatos_tienen_la_misma_clave_de_datos(fmt):
    base = set(_format_scaling("9:16"))
    assert set(_format_scaling(fmt)) == base
