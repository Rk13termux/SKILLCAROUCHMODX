"""Smoke de los 10 componentes con props reales (sin Chromium)."""

import json

from components import expandir

PROPS = {
    "social": {
        "kicker": "COMPONENTES", "titulo": "Tarjeta social",
        "texto": "Titular de valor para abrir o cerrar un carrusel.",
        "cta": "Guardalo"},
    "terminal": {
        "titulo": "demo · local",
        "lines": [{"t": "cmd", "v": "python3 tech_carousel.py --tema demo"},
                  {"t": "ok", "v": "✓ Sin recortes"},
                  {"t": "err", "v": "ERROR: --slides no coincide"}]},
    "card-info": {
        "variante": "info", "titulo": "Definición",
        "cuerpo": "Bloque de contexto en una frase, sin rodeos."},
    "card-compare": {
        "titulo": "Endpoints REST vs GraphQL",
        "cols": [{"nombre": "REST", "badge": "A",
                  "items": [{"ok": True, "v": "Caché HTTP simple"},
                            {"ok": False, "v": "Over/under fetching"}]},
                 {"nombre": "GraphQL", "badge": "B",
                  "items": [{"ok": True, "v": "Consulta exacta"}]}]},
    "card-repo": {
        "repo": "techedu/componentes", "desc": "Bloques gráficos",
        "tree": "components/\n  base.py\n  terminal.py",
        "install": "python3 -m pip install .",
        "badges": ["MIT", "tests ✓", "offline"]},
    "diagram": {
        "titulo": "Del commit al deploy",
        "nodos": [{"v": "git push", "sub": "rama feature"},
                  {"v": "CI: test + lint", "sub": "2 min"},
                  {"v": "deploy", "sub": "canaria 10%"}]},
    "pasos": {
        "titulo": "Checklist de release",
        "pasos": [{"t": "Corré los tests", "d": "unit + smoke"},
                  {"t": "Bump de versión", "d": "semver estricto"}]},
    "code": {
        "lenguaje": "python", "notas": "Una función, una responsabilidad.",
        "codigo": "def filtrar(items):\n    return [i for i in items if i]"},
    "checklist": {
        "titulo": "Para aplicar hoy",
        "items": ["Validá en servidor, no solo en cliente",
                  "Medí el recorte antes de publicar"]},
    "mitos": {
        "mito": "Más componentes = mejor carrusel",
        "realidad": "Cada componente debe justificar su espacio"},
}


def _body(nombre, props):
    return ('<div class="componente" data-component="%s" data-props=\'%s\'>'
            "</div>" % (nombre, json.dumps(props, ensure_ascii=False)))


def test_todos_los_componentes_expanden():
    for nombre, props in PROPS.items():
        avisos = []
        html, usados = expandir(_body(nombre, props),
                                {"accent": "#06B6D4"}, avisos)
        assert avisos == [], f"{nombre}: {avisos}"
        assert usados == [nombre]
        assert "comp-error" not in html, nombre
        assert html.strip(), nombre


def test_alias_de_componentes():
    avisos = []
    html, usados = expandir(_body("vs", PROPS["card-compare"]),
                            {"accent": "#06B6D4"}, avisos)
    assert usados == ["vs"] and not avisos
    assert "card-compare" in html


def test_componente_desconocido_no_mata_el_slide():
    avisos = []
    html, usados = expandir(_body("no-existe", {"x": 1}),
                            {"accent": "#06B6D4"}, avisos)
    assert usados == ["no-existe"]
    assert avisos and "desconocido" in avisos[0]


def test_dos_componentes_en_un_slide():
    cuerpo = _body("diagram", PROPS["diagram"]) + \
        _body("checklist", PROPS["checklist"])
    avisos = []
    html, usados = expandir(cuerpo, {"accent": "#06B6D4"}, avisos)
    assert not avisos
    assert len(usados) == 2
    assert html.count("comp-wrap") == 2
