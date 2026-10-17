"""Smoke de los 23 componentes con props reales (sin Chromium)."""

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
    "tree": {
        "titulo": "mi-app/",
        "nodos": [{"v": "src/", "tipo": "dir"},
                  {"v": "main.py", "depth": 1},
                  {"v": "core/", "depth": 1, "tipo": "dir"},
                  {"v": "auth.py", "depth": 2}]},
    "http": {
        "metodo": "GET", "ruta": "/api/users/1", "codigo": "200 OK",
        "nota_estado": "sin auth",
        "response": '{\n  "id": 1,\n  "rol": "admin"\n}'},
    "browser": {
        "url": "https://panel.local/login",
        "vista": "Bienvenido al panel de control"},
    "diff": {
        "titulo": "Validación en servidor",
        "antes": "login(user_input)",
        "despues": "if valido(user_input):\n    login(user_input)"},
    "stats": {
        "titulo": "El carrusel en números",
        "items": [{"valor": "1", "etiqueta": "idea por slide"},
                  {"valor": "0", "etiqueta": "payloads ejecutables"}]},
    "tabla": {
        "titulo": "Dónde miran vs dónde está",
        "headers": ["Miran", "Realidad"],
        "filas": [["CPU", "cola saturada"], ["red", "consulta lenta"]]},
    "layers": {
        "titulo": "Dónde buscar el cuello",
        "capas": [{"v": "Red", "sub": "latencia"},
                  {"v": "App", "sub": "colas", "tipo": "api"},
                  {"v": "Base de datos", "sub": "queries", "tipo": "db"}]},
    "pipeline": {
        "titulo": "Deploy aburrido",
        "etapas": [{"v": "test", "estado": "ok"},
                   {"v": "canaria", "estado": "run"},
                   {"v": "prod", "estado": "idle"}]},
    "faq": {
        "pregunta": "¿Por qué falla en silencio?",
        "respuesta": "Porque nadie mira ese log."},
    "quote": {
        "texto": "Aburrido es fiable.",
        "autor": "TechEdu", "rol": "línea editorial"},
    "quiz": {
        "pregunta": "¿Qué revisas primero?",
        "opciones": [{"v": "Logs"}, {"v": "Métricas", "ok": True}]},
    "editor": {
        "archivo": "main.py", "lenguaje": "python",
        "codigo": "def saludar(nombre):\n    return f\"hola {nombre}\"",
        "salida": "hola mundo"},
    "gh-stats": {
        "repo": "ejemplo/demo", "desc": "Demo de prueba",
        "stars": "1.2k", "forks": "300", "issues": "12",
        "licencia": "MIT",
        "lenguajes": [{"n": "Python", "p": 70}, {"n": "Shell", "p": 30}]},
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


def test_props_con_mayor_dentro_de_comillas():
    """Un > dentro del JSON (ej. <think>) no debe truncar el atributo."""
    import re
    from components import expandir
    body = ('<div class="componente" data-component="diagram" '
            'data-props=\'{"titulo":"loop","nodos":[{"v":"Modelo",'
            '"sub":"razona con <think>"}]}\'></div>')
    avisos = []
    html, usados = expandir(body, {"accent": "#06B6D4"}, avisos)
    assert usados == ["diagram"] and not avisos
    assert "think" in html


def test_dialecto_sin_falsos_positivos():
    from copywriting.base import (corregir_dialecto, regionalismos_presentes,
                                  rituales_presentes, voseo_presente)
    assert regionalismos_presentes("TechEdu · tu checklist") == []
    assert rituales_presentes("lee el material") == []
    assert not voseo_presente("Fija este comentario")
    texto, cambios = corregir_dialecto("Mirá y fijá el deploy")
    assert (texto, cambios) == ("mira y fija el deploy", 1)


def test_tree_usa_svg_por_formato_sin_emoji():
    from components import expandir
    import json
    props = {"nodos": [{"v": "app.py"}, {"v": "conf.yaml"},
                       {"v": "notas.md"}, {"v": "data.db"},
                       {"v": "src/", "tipo": "dir"},
                       {"v": "main", "depth": 1, "modo": "x"}]}
    body = ('<div class="componente" data-component="tree" data-props=\'%s\'>'
            "</div>" % json.dumps(props))
    avisos = []
    html, usados = expandir(body, {"accent": "#06B6D4"}, avisos)
    assert usados == ["tree"] and not avisos
    assert html.count("<svg") == 6
    for emoji in ("📁", "📄", "🧠", "❓"):
        assert emoji not in html
    for color in ("#EAB308", "#10B981", "#60A5FA", "#9CA3AF", "#34D399"):
        assert color in html


def test_tree_modo_git():
    from components import expandir
    import json
    props = {"modo": "git", "ramas": ["main*", "feature/auth"]}
    body = ('<div class="componente" data-component="tree" data-props=\'%s\'>'
            "</div>" % json.dumps(props))
    avisos = []
    html, usados = expandir(body, {"accent": "#06B6D4"}, avisos)
    assert usados == ["tree"] and not avisos
    assert "* " in html and "feature/auth" in html
