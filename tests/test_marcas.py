"""Iconos de marca: logos Simple Icons vendoreados y match sin falsos positivos."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from icons import CATEGORIAS, get_icon, glyph_por_texto  # noqa: E402
from icons import marcas  # noqa: E402
from icons import registry as R  # noqa: E402

ACC = {"rgb": (250, 204, 21), "bright_rgb": (255, 235, 120)}

# Textos que contienen substrings de marcas pero NO nombran ninguna.
TRAMPAS = ("digital", "google", "configuracion", "configuración", "compilar",
           "registro", "control", "agregar")


def test_marcas_tiene_glyphs():
    assert marcas.GLYPHS, "el set de marcas no puede estar vacío"
    assert len(marcas.GLYPHS) >= 50
    assert marcas.ORDEN, "ORDEN no puede estar vacío"
    for nombre in marcas.ORDEN:
        assert nombre in marcas.GLYPHS, f"{nombre} en ORDEN pero no en GLYPHS"


def test_registry_test_marcas_pasa():
    assert R.main(["--test", "marcas"]) == 0


def test_glyphs_sin_stroke_duplicado():
    for nombre, cuerpo in marcas.GLYPHS.items():
        assert "stroke" not in cuerpo, f"{nombre} usa stroke (debe ser relleno)"
        assert cuerpo.count("<path") == 1, f"{nombre} debe ser un único <path>"
        assert R._test_glyph(nombre, cuerpo) == [], nombre


def test_categoria_marcas_integrada():
    assert "marcas" in CATEGORIAS
    assert CATEGORIAS["marcas"].GLYPHS is not None
    assert len(CATEGORIAS["marcas"].GLYPHS) == len(marcas.GLYPHS)


def test_alias_apuntan_a_glyphs_instalados():
    for alias, nombre in marcas.ALIAS.items():
        assert alias == alias.lower(), f"alias no minúscula: {alias}"
        assert nombre in marcas.GLYPHS, f"alias {alias} → {nombre} inexistente"


def test_trampas_no_disparan_marca():
    for texto in TRAMPAS:
        elegido = glyph_por_texto(texto)
        assert elegido not in marcas.GLYPHS, f"'{texto}' disparó la marca {elegido}"


def test_marcas_reales_se_eligen():
    casos = {
        "React y Vue para frontend": "react",
        "MongoDB vs PostgreSQL": "mongodb",
        "Redis como cache": "redis",
        "Terraform en produccion": "terraform",
        "Aprende Rust hoy": "rust",
    }
    for texto, esperado in casos.items():
        assert glyph_por_texto(texto) == esperado, texto


def test_generico_no_es_robado_por_la_marca():
    # "docker" es marca y concepto genérico: gana el genérico ("container").
    assert glyph_por_texto("Docker y contenedores en produccion") == "container"
    # "linux" aparece después de "roadmap": gana el genérico.
    assert glyph_por_texto("Roadmap para aprender Linux") == "roadmap"


def test_marca_entrega_data_uri():
    uri = get_icon("docker", ACC, "marcas")
    assert uri and uri.startswith("data:image/svg+xml;base64,")
