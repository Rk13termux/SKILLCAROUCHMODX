"""Reglas locales de icono-por-tema — las escribe `icon_smith.py agregar --kw`.

Se evalúan ANTES que las reglas de `registry.TEMA_GLYPHS`, así que sirven
para afinar el match de un tema puntual sin tocar el registry.

Formato:
    TEMA_GLYPHS = (
        (("palabra1", "palabra2"), "nombre-del-glyph"),
    )
"""

TEMA_GLYPHS = ()
