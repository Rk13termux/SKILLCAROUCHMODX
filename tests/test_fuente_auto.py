"""Flujo de 1 comando: la carpeta se crea y el copy se escribe solo."""

from tech_carousel import _generar_slides_auto, _slides_existentes


def test_slides_existentes_carpeta_inexistente(tmp_path):
    assert _slides_existentes(tmp_path / "no-existe") == []


def test_slides_existentes_ignora_story(tmp_path):
    (tmp_path / "story-fuente.html").write_text("x", encoding="utf-8")
    (tmp_path / "slide-01.html").write_text("x", encoding="utf-8")
    (tmp_path / "slide-02.html").write_text("x", encoding="utf-8")
    nombres = [p.name for p in _slides_existentes(tmp_path)]
    assert nombres == ["slide-01.html", "slide-02.html"]


def test_orden_numerico(tmp_path):
    for i in (1, 2, 10):
        (tmp_path / f"slide-{i:02d}.html").write_text("x", encoding="utf-8")
    assert [p.name for p in _slides_existentes(tmp_path)] == [
        "slide-01.html", "slide-02.html", "slide-10.html"]


def test_autogenera_copy_y_story(tmp_path):
    carpeta = tmp_path / "demo-tema"
    slides = _generar_slides_auto(carpeta, 4, "cybersec", "Demo Tema",
                                  "Demo", "TechEdu", "demo-tema")
    assert len(slides) == 4
    assert (carpeta / "story-fuente.html").is_file()
    contenido = (carpeta / "slide-01.html").read_text(encoding="utf-8")
    assert "Demo Tema" in contenido or "Demo" in contenido
    # numeración coherente para el builder
    assert "1/4" in contenido


def test_autogenera_en_carpeta_nueva(tmp_path):
    """La carpeta no existía: la auto-generación la crea."""
    carpeta = tmp_path / "recien-creada"
    assert not carpeta.exists()
    slides = _generar_slides_auto(carpeta, 3, "prog", "Tema", "Tema",
                                  "TechEdu", "tema")
    assert carpeta.is_dir() and len(slides) == 3


def test_autogenera_todos_los_componentes_declarados(tmp_path):
    """Cada slide fuente debe traer su bloque de contenido y su número."""
    import re
    slides = _generar_slides_auto(tmp_path / "x", 7, "ai", "Tema IA", "IA",
                                  "TechEdu", "tema-ia")
    for p in slides:
        html = p.read_text(encoding="utf-8")
        assert 'class="contenido"' in html
        assert re.search(r'class="numero">\d+/7<', html), p.name


def test_autogenera_usa_el_resalte_en_la_fuente(tmp_path):
    """El HTML fuente pinta las keywords con el color pedido (previsualización)."""
    slides = _generar_slides_auto(tmp_path / "res", 4, "cybersec", "SQL injection",
                                  "SQL injection", "TechEdu", "sql",
                                  resalte="#E63946")
    html = slides[0].read_text(encoding="utf-8")
    assert "color: #E63946" in html
    assert "#FFB800" not in html


def test_story_fuente_lleva_una_clave(tmp_path):
    """La story se renderiza con keywords: si no hay .clave sale sin resaltar."""
    _generar_slides_auto(tmp_path / "st", 4, "cybersec", "Colores Estrellas",
                         "Colores Estrellas", "TechEdu", "colores-estrellas",
                         resalte="#06B6D4")
    story = (tmp_path / "st" / "story-fuente.html").read_text(encoding="utf-8")
    assert 'class="clave"' in story
    assert "color: #06B6D4" in story


def test_puente_recap_elige_inicio_medio_cierre():
    import tech_carousel as tc
    titulos = ["Qué es Hermes Agent", "Instalación en una línea",
               "El loop que lo hace agente", "Tu agente en Telegram",
               "Seguridad antes que magia"]
    recap = tc._elegir_recap(titulos)
    assert recap == ["Qué es Hermes Agent", "El loop que lo hace agente",
                     "Seguridad antes que magia"]


def test_puente_recap_recorta_a_7_palabras():
    import tech_carousel as tc
    recap = tc._elegir_recap(["Uno dos tres cuatro cinco seis siete ocho nueve",
                              "Otro título válido"])
    assert recap[0] == "Uno dos tres cuatro cinco seis siete"
    assert len(recap) == 2


def test_puente_recap_sin_titulos_devuelve_vacio():
    import tech_carousel as tc
    assert tc._elegir_recap([]) == []
    assert tc._texto_titulo("") == ""
    assert "Hermes" in tc._texto_titulo(
        '<div class="titulo">Qué es <span class="clave">Hermes</span></div>')
