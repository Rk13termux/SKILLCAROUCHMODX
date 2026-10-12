"""Tipografías: modo offline y fallbacks locales (sin dependencia de red)."""

from theme import fonts


def setup_function(_):
    fonts.set_offline(False)


def teardown_function(_):
    fonts.set_offline(False)


def test_online_enlaza_google_fonts():
    links = fonts.links()
    assert "fonts.googleapis.com" in links
    assert "rel=\"stylesheet\"" in links


def test_offline_no_emite_ningun_enlace():
    fonts.set_offline(True)
    assert fonts.offline() is True
    assert fonts.links() == ""
    assert "http" not in fonts.links()


def test_fallbacks_de_font_family_son_locales():
    for stack in (fonts.DISPLAY, fonts.MONO):
        assert "http" not in stack
    assert fonts.DISPLAY.endswith("sans-serif")
    assert fonts.MONO.endswith("monospace")
    # mono siempre cierra en un stack de sistema (requisito del plan)
    for necesario in ("SFMono-Regular", "Menlo", "Consolas"):
        assert necesario in fonts.MONO


def test_offline_tambien_aplica_a_body_css():
    fonts.set_offline(True)
    css = fonts.body_css()
    assert "font-family" in css and "http" not in css
