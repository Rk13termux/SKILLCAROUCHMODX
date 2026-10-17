"""Tests de los componentes nuevos: qr, stack, error, timeline, index."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from components import base  # noqa: E402
from components.extra import (  # noqa: E402
    render_error, render_index, render_stack, render_timeline,
)
from components.qr import render as render_qr  # noqa: E402


def test_alias_registrados():
    for nombre in ("qr", "qrcode", "codigo-qr",
                   "tecnologias", "tech-stack",
                   "error", "traceback", "traza",
                   "roadmap", "ruta", "fases",
                   "indice", "toc", "tabla-contenidos"):
        assert base.html_valido(nombre), nombre


def test_stack_renderiza_chips():
    h = render_stack({"titulo": "Stack", "items": [
        {"v": "Python", "sub": "3.14"}, "Git", "Docker"]}, {})
    assert "stack__chip" in h
    assert "Python" in h and "3.14" in h
    assert "stack__dot" in h


def test_stack_recorta_y_avisa():
    av = []
    props = {"items": [f"T{i}" for i in range(12)]}
    h = render_stack(props, {}, av)
    assert av and "stack" in av[0]
    assert h.count("stack__chip") == 8


def test_error_clasifica_lineas():
    av = []
    h = render_error({
        "archivo": "main.py", "titulo": "KeyError típico",
        "texto": 'Traceback (most recent call last):\n  File "main.py", line 3\nKeyError: "nombre"',
        "linea": "Falta la clave antes de leerla",
    }, {}, av)
    assert not av
    assert "err__line--err-head" in h
    assert "err__line--err" in h
    assert "err__resumen" in h
    assert "main.py" in h


def test_timeline_estados():
    h = render_timeline({"titulo": "Ruta", "etapas": [
        {"v": "Semana 1", "sub": "Sintaxis", "estado": "ok"},
        {"v": "Semana 2", "sub": "Proyectos", "estado": "run"},
        {"v": "Semana 3", "sub": "Deploy", "estado": "error"},
    ]}, {})
    assert "tl__mark--ok" in h
    assert "tl__mark--run" in h
    assert "tl__mark--error" in h


def test_index_numerado():
    h = render_index({"titulo": "Lo que verás",
                      "items": ["Instalar", "Variables", "Tu primer script"]}, {})
    assert h.count("idx__item") == 3
    assert "idx__n" in h and "idx__v" in h


def test_qr_genera_svg_inline():
    h = render_qr({"url": "https://chmodxcode.pro",
                   "titulo": "Tu próximo paso"}, {})
    assert "<svg" in h
    assert "qr__caja" in h


def test_qr_sin_url_no_explota():
    av = []
    h = render_qr({}, {}, av)
    assert "qr--vacio" in h or "qr__vacio" in h
    assert av


def test_expandir_componentes_nuevos():
    import json
    for nombre, props in (
        ("qr", {"url": "https://chmodxcode.pro"}),
        ("tecnologias", {"items": ["Python", "Git"]}),
        ("error", {"texto": "ValueError: algo falló"}),
        ("roadmap", {"etapas": [{"v": "Fase 1"}]}),
        ("indice", {"items": ["Uno", "Dos"]}),
    ):
        body = (f'<div class="componente" data-component="{nombre}" '
                f"data-props='{json.dumps(props)}'></div>")
        av = []
        html, usados = base.expandir(body, {"accent": "#06B6D4"}, av)
        assert usados == [nombre], (nombre, usados, av)
        assert "<div" in html and not av, (nombre, av)
