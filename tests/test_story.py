"""Story: todo `var(--x)` usado en el CSS debe estar definido en `:root`.

Si falta, la declaración entera se invalida en tiempo de cómputo y Chrome la
tira sin ruido (fue el caso: sin `--acento-rgba-b` el `background` de la story
se caía entero y salía sin glow y con las keywords blancas).
"""

import re

from tech_carousel import STORY_TEMPLATE, TEMPLATE


def _vars_usados(css: str) -> set:
    return set(re.findall(r"var\((--[a-z0-9-]+)", css))


def _vars_definidos(css: str) -> set:
    raiz = css.split(":root {", 1)
    if len(raiz) < 2:
        return set()
    return set(re.findall(r"^\s*(--[a-z0-9-]+):", raiz[1].split("}")[0],
                          re.MULTILINE))


def test_story_define_todas_las_vars_que_usa():
    usados = _vars_usados(STORY_TEMPLATE)
    definidos = _vars_definidos(STORY_TEMPLATE)
    faltan = usados - definidos
    assert not faltan, f"vars sin definir en la story: {sorted(faltan)}"


def test_slides_tambien_definen_todas_las_vars():
    usados = _vars_usados(TEMPLATE)
    definidos = _vars_definidos(TEMPLATE)
    faltan = usados - definidos
    assert not faltan, f"vars sin definir en los slides: {sorted(faltan)}"


def test_story_comparte_el_fondo_del_slide_sin_estrellas():
    """La story usa las capas del fondo de la casa, sin estrellas."""
    fondo = STORY_TEMPLATE.split(".story {")[1].split("}")[0]
    assert "__fondo_story__" in fondo
    assert "__estrellas__" not in STORY_TEMPLATE
    assert fondo.rstrip().endswith("#000000;")


def test_todos_los_tokens_del_story_estan_en_el_template():
    """Si el template pide un token, `generar_story` tiene que reemplazarlo."""
    from tech_carousel import generar_story
    import inspect
    src = inspect.getsource(generar_story)
    for token in set(re.findall(r"__[a-z0-9_]+__", STORY_TEMPLATE)):
        assert token in src, f"token {token} no se reemplaza en generar_story()"


def test_variables_acento_y_resalte_en_el_root_de_la_story():
    raiz = STORY_TEMPLATE.split(":root {", 1)[1].split("}")[0]
    for v in ("--acento:", "--acento-rgba-b:", "--acento-rgba-30:",
              "--acento-rgba-40:", "--resalte:", "--resalte-brillo:"):
        assert v in raiz, f"falta {v} en :root de la story"
