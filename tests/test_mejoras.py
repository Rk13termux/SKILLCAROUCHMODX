"""Mejoras de infraestructura: UTM, landing2, exportadores y gh-stats real."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from generar_copy_tech import _con_utm, _landing_dominio  # noqa: E402
from tech_carousel import (  # noqa: E402
    FORMATOS, exportar_pdf, generar_contact_sheet, generar_html,
)
from theme import colors as _colors  # noqa: E402

KW = {"__resalte__": "#06B6D4", "__resalte_brillo__": "#3DD2EE",
      "__resalte_rgba32__": "rgba(6,182,212,0.32)",
      "__resalte_rgba38__": "rgba(6,182,212,0.38)"}
ACCENT = _colors.acento_vars("#06B6D4")
COMANDOS = ["python3 --version", "pip install requests"]


def _slide(i, n, **kw):
    data = {"number": f"{i}/{n}",
            "body": ('<div class="titulo">Titular <span class="clave">clave'
                     '</span></div><div class="cuerpo">Cuerpo.</div>'),
            "footer": "CHMODX · demo"}
    return generar_html(i, n, data, "9:16", FORMATOS["9:16"], ACCENT, None,
                        "CHMODX", resalte_vars=KW, semilla="demo",
                        comandos_finales=COMANDOS, cta_modo="seguir",
                        recap_titulos=["Uno", "Dos", "Tres"], **kw)


# ── UTM ────────────────────────────────────────────────────────────

def test_con_utm_agrega_parametros():
    u = _con_utm("https://chmodxcode.pro", "instagram", "python")
    assert u.startswith("https://chmodxcode.pro?")
    assert "utm_source=instagram" in u
    assert "utm_medium=carrusel" in u
    assert "utm_campaign=python" in u


def test_con_utm_respeta_query_existente():
    u = _con_utm("https://x.dev/a?b=1", "tiktok")
    assert "?b=1&utm_source=tiktok" in u


def test_con_utm_vacio():
    assert _con_utm("", "instagram") == ""
    assert _con_utm(None, "instagram") == ""


# ── landing2 en el slide final ─────────────────────────────────────

def test_final_landing2_agrega_boton_secundario():
    html = _slide(7, 7, landing="https://chmodxcode.pro",
                  landing2="https://t.me/chmodx",
                  landing2_texto="ÚNETE AL TELEGRAM")
    assert 'class="landing-boton landing-boton--sec"' in html
    assert "ÚNETE AL TELEGRAM" in html
    assert "T.ME/CHMODX" in html.upper()
    # el botón primario sigue
    assert "EMPIEZA EN" in html


def test_final_sin_landing2_no_agrega_secundario():
    html = _slide(7, 7, landing="https://chmodxcode.pro")
    assert 'class="landing-boton landing-boton--sec"' not in html


# ── Exportadores (toleran carpeta sin PNG) ────────────────────────

def test_contact_sheet_tolera_sin_png(tmp_path):
    assert generar_contact_sheet(tmp_path, ["slide-01.html"],
                                 FORMATOS["9:16"]) is None


def test_exportar_pdf_tolera_sin_png(tmp_path):
    assert exportar_pdf(tmp_path, ["slide-01.html"], FORMATOS["9:16"]) is None


# ── gh-stats real (sin red → no explota) ──────────────────────────

def test_gh_stats_repo_invalido_no_explota():
    from components.gh_stats import render
    av = []
    h = render({"repo": "no-es-repo", "auto": True, "stars": "1.2k"}, {}, av)
    assert "ghstats" in h
    assert av  # avisó que no pudo leer la API


def test_github_props_desde_repo_invalido():
    from utils.github import fetch_repo, props_desde_repo
    assert fetch_repo("sin-barra") is None
    assert props_desde_repo("sin-barra") is None


# ── brief.py importa ──────────────────────────────────────────────

def test_brief_importa():
    import brief
    assert callable(brief.main)
    assert brief.PRESETS["3"][0] == "python"


# ── QA de repetición ──────────────────────────────────────────────

def test_qa_repeticion_detecta_texto_identico(tmp_path):
    from tech_carousel import qa_repeticion
    for i in (1, 2, 3):
        texto = "mismo texto repetido en dos slides" if i in (1, 3) else "otra cosa muy distinta aqui"
        (tmp_path / f"slide-{i:02d}.html").write_text(
            f'<div class="contenido"><div class="titulo">{texto}</div></div>',
            encoding="utf-8")
    avisos = qa_repeticion(tmp_path,
                           ["slide-01.html", "slide-02.html", "slide-03.html"])
    assert any("slide-01" in a and "slide-03" in a for a in avisos)


def test_qa_repeticion_detecta_componente_repetido(tmp_path):
    from tech_carousel import qa_repeticion
    nombres = []
    for i in range(1, 7):
        n = f"slide-{i:02d}.html"
        nombres.append(n)
        (tmp_path / n).write_text(
            '<div class="componente" data-component="card-info"></div>',
            encoding="utf-8")
    avisos = qa_repeticion(tmp_path, nombres)
    assert any("card-info" in a for a in avisos)


def test_qa_repeticion_ignora_numero_y_pie(tmp_path):
    """El número y el pie son constantes: no deben contar como repetición."""
    from tech_carousel import qa_repeticion
    contenidos = [
        "Instala Python y verifica la versión con un comando simple",
        "Las variables guardan datos y los tipos cambian el comportamiento",
        "Los bucles repiten tareas aburridas sin escribir de más",
        "Las funciones empaquetan lógica para reutilizarla sin copiar",
        "Los módulos separan tu código en archivos manejables",
    ]
    nombres = []
    for i, contenido in enumerate(contenidos, 1):
        n = f"slide-{i:02d}.html"
        nombres.append(n)
        (tmp_path / n).write_text(
            f'<div class="numero">{i}/5</div>'
            f'<div class="contenido"><div class="cuerpo">{contenido}</div></div>'
            '<div class="pie">CHMODX · Demo</div>',
            encoding="utf-8")
    assert qa_repeticion(tmp_path, nombres) == []


# ── Plan de publicación en copy-redes ─────────────────────────────

def test_copy_redes_incluye_plan_publicacion(tmp_path):
    from generar_copy_tech import generar_copy_redes
    (tmp_path / "slide-01.html").write_text("<div>demo</div>", encoding="utf-8")
    generar_copy_redes(tmp_path, "Tema de prueba", "Tema", landing=None)
    md = (tmp_path / "copy-redes.md").read_text(encoding="utf-8")
    assert "Plan de publicación sugerido" in md
    assert "Día 1" in md


# ── El wrapper .ajuste debe ser flex column ───────────────────────

def test_ajuste_es_flex_column_para_centrar_hijos():
    """Regresión: sin display:flex, .badge/.cta/.ind-swipe (align-self:
    center) quedan pegados a la izquierda."""
    import re
    html = _slide(1, 5)
    m = re.search(r"\.ajuste \{[^}]*\}", html)
    assert m, "no se encontró la regla .ajuste"
    regla = m.group(0)
    assert "display: flex" in regla
    assert "flex-direction: column" in regla
    # el badge confía en align-self: center
    assert "align-self: center" in re.search(r"\.badge \{[^}]*\}", html).group(0)
