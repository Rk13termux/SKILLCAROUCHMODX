"""Colores: normalización y mensaje de error (usabilidad del CLI)."""

import pytest

from theme.colors import RESALTE_DEFECTO, acento_vars, normalizar_hex, \
    resuelve_resalte


def test_hex_normalizado_a_mayusculas():
    assert normalizar_hex("#06b6d4") == "#06B6D4"


def test_hex_corto_se_expande():
    assert normalizar_hex("#0BD") == "#00BBDD"


def test_nombres_de_paleta():
    assert normalizar_hex("cian") == "#06B6D4"
    assert normalizar_hex("Verde") == "#10B981"


def test_error_con_ejemplo_y_paleta():
    with pytest.raises(ValueError) as exc:
        normalizar_hex("turquesa")
    msg = str(exc.value)
    assert "turquesa" in msg
    assert "#RRGGBB" in msg and "#06B6D4" in msg
    assert "cian" in msg  # nombres de paleta listados


def test_error_con_none():
    with pytest.raises(ValueError):
        normalizar_hex(None)


def test_acento_vars_genera_css():
    vars_ = acento_vars("#06B6D4")
    for k in ("accent", "accent_bright", "accent_rgba_30", "accent_rgba_40",
              "rgb", "bright_rgb"):
        assert k in vars_
    assert vars_["accent"] == "#06B6D4"
    assert vars_["accent_bright"].startswith("#")


def test_keywords_usan_el_color_del_prompt():
    """Si no se pide --resalte, las keywords toman el MISMO --color."""
    assert resuelve_resalte(None, "#06B6D4") == "#06B6D4"
    assert resuelve_resalte("", "#E63946") == "#E63946"
    assert resuelve_resalte(None, "cian") == "#06B6D4"


def test_resalte_explicito_gana_sobre_el_color():
    assert resuelve_resalte("#FF0000", "#06B6D4") == "#FF0000"
    assert resuelve_resalte("dorado", "#06B6D4") == "#FFD700"


def test_resalte_invalido_sigue_lanzando():
    with pytest.raises(ValueError) as exc:
        resuelve_resalte("turquesa", "#06B6D4")
    assert "turquesa" in str(exc.value)


def test_resalte_defecto_sigue_disponible():
    """Fallback sólo cuando NO hay color de tema (no debería pasar por CLI)."""
    assert resuelve_resalte(None, RESALTE_DEFECTO) == "#FFB800"
