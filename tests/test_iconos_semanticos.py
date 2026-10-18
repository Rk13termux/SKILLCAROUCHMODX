"""Iconos profesionales: librería Lucide, selección semántica y roles."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from icons import (  # noqa: E402
    CATEGORIAS, TEMA_GLYPHS, elegir_icono, get_icon, glyph_por_texto,
)
from icons import registry as R  # noqa: E402

ACC = {"rgb": (250, 204, 21), "bright_rgb": (255, 235, 120)}


def test_libreria_ampliada():
    total = len({n for s in CATEGORIAS.values() for n in s.GLYPHS})
    assert total >= 200, f"esperaba una librería amplia, hay {total}"
    for cat in ("cybersec", "dev", "ai", "infra"):
        assert len(CATEGORIAS[cat].GLYPHS) >= 40


def test_todos_los_glyphs_son_validos():
    malos = []
    for cat, s in CATEGORIAS.items():
        for nombre, cuerpo in s.GLYPHS.items():
            errs = R._test_glyph(nombre, cuerpo)
            if errs:
                malos.append(f"{cat}/{nombre}: {'; '.join(errs)}")
    assert not malos, "\n".join(malos[:10])


def test_icono_semantico_por_texto():
    casos = {
        "Tu correo esta en una fuga de datos": "mail-warning",
        "Detecta el phishing con Python": "link-2-off",
        "Docker y contenedores en produccion": "container",
        "Ransomware: secuestran tus datos": "lock-keyhole",
        "Roadmap para aprender Linux": "roadmap",
        "Backups que si funcionan": "database",
        "Regex: domina las expresiones regulares": "regex",
    }
    for texto, esperado in casos.items():
        assert glyph_por_texto(texto) == esperado, texto


def test_no_hay_falsos_positivos_por_prefijo():
    # "funciona" no debe caer en la regla de "funciones"; "pipeline" no en "pip"
    assert glyph_por_texto("Como funciona un LLM") == "brain-circuit"
    assert glyph_por_texto("Un pipeline de CI/CD") == "workflow"


def test_claves_matchean_limite_de_palabra():
    # "metadatos" no debe disparar la regla de "metas"; "apilar" no "api"
    assert glyph_por_texto("Analiza los metadatos del archivo") != "trophy"


def test_roles_entregan_data_uri():
    for i in (1, 3, 5):
        uri = elegir_icono(i, 6, ACC, tema="cybersec")[1]
        assert uri and uri.startswith("data:image/svg+xml;base64,")
    # la portada usa el primer glyph del orden y el cierre un glyph de CTA
    assert elegir_icono(1, 6, ACC, tema="cybersec")[0] == \
        CATEGORIAS["cybersec"].ORDEN[0]
    assert elegir_icono(6, 6, ACC, tema="dev")[0] in ("rocket", "arrow-right")


def test_glyph_por_texto_evita_repetir_usados():
    usados = {"container"}
    g = glyph_por_texto("Docker y contenedores en produccion", usados)
    assert g != "container"


def test_keywords_declaradas_apuntan_a_glyphs_instalados():
    instalados = {n for s in CATEGORIAS.values() for n in s.GLYPHS}
    faltan = [(c, g) for claves, g in TEMA_GLYPHS
              for c in claves if g not in instalados]
    assert not faltan, f"reglas sin glyph: {faltan[:8]}"


def test_overlays_locales_por_defecto():
    from icons import lucide_extra, tema_extra
    assert lucide_extra.SETS == {}
    assert tema_extra.TEMA_GLYPHS == ()


def test_get_icon_de_lucide_y_de_la_casa():
    # un glyph de Lucide y uno hecho a mano conviven en el mismo set
    assert get_icon("shield-alert", ACC, "cybersec")
    assert get_icon("firewall", ACC, "cybersec")
