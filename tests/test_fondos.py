"""Fondos: variantes, rol/vertical, determinismo y tokens del template."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tech_carousel import FORMATOS, generar_html  # noqa: E402
from theme import colors as _colors  # noqa: E402
from theme import fondos  # noqa: E402

ACC = "#FACC15"
KW = {"__resalte__": ACC, "__resalte_brillo__": "#FDE68A",
      "__resalte_rgba32__": "rgba(250,204,21,0.32)",
      "__resalte_rgba38__": "rgba(250,204,21,0.38)"}


def _capas(css: str) -> int:
    """Cuenta capas de primer nivel (paréntesis balanceados)."""
    if not css or css == "none":
        return 0
    n, d = 0, 0
    for ch in css:
        if ch == "(":
            d += 1
        elif ch == ")":
            d -= 1
        elif ch == "," and d == 0:
            n += 1
    return n + 1


def _html(i, n, **kw):
    data = {"number": f"{i}/{n}",
            "body": '<div class="titulo">Titular <span class="clave">k</span>'
                    '</div><div class="cuerpo">Cuerpo.</div>',
            "footer": "CHMODX · demo"}
    return generar_html(i, n, data, "9:16", FORMATOS["9:16"],
                        _colors.acento_vars(ACC), None, "CHMODX",
                        resalte_vars=KW, semilla="demo",
                        comandos_finales=["python3 script.py", "git status"],
                        **kw)


def _capas_lista(css: str) -> list:
    """Separa capas de primer nivel respetando los paréntesis."""
    if not css or css == "none":
        return []
    capas, actual, d = [], [], 0
    for ch in css:
        if ch == "(":
            d += 1
        elif ch == ")":
            d -= 1
        if ch == "," and d == 0:
            capas.append("".join(actual).strip())
            actual = []
        else:
            actual.append(ch)
    if "".join(actual).strip():
        capas.append("".join(actual).strip())
    return capas


def test_cada_capa_del_fondo_es_una_imagen():
    """background-image no acepta colores sueltos: un `#0B0B0D` al final
    invalida TODA la declaración y el fondo desaparece (bug real)."""
    for v in fondos.VARIANTES:
        for rol in fondos.ROLES:
            css = fondos.fondo(rol=rol, vertical="dev", variante=v)["fondo"]
            capas = _capas_lista(css)
            assert capas, v
            for capa in capas:
                assert capa.startswith(("radial-gradient(", "linear-gradient(",
                                        "conic-gradient(", "url(")), (v, capa[:40])


def test_todas_las_variantes_producen_capas():
    for v in fondos.VARIANTES:
        f = fondos.fondo(rol="contenido", vertical="dev", rgb=(250, 204, 21),
                         variante=v)
        assert _capas(f["fondo"]) >= 2, v
        # textura y tamaños tienen que estar en fase (CSS exige listas parejas)
        if f["textura"] != "none":
            assert _capas(f["textura"]) == _capas(f["textura_size"]), v
            assert f["textura_mask"] != "none", v


def test_determinista():
    a = fondos.fondo(rol="cover", vertical="ai", rgb=(6, 182, 212))
    b = fondos.fondo(rol="cover", vertical="ai", rgb=(6, 182, 212))
    assert a == b
    c = fondos.fondo(rol="cover", vertical="ai", rgb=(6, 182, 212),
                     semilla=1)
    assert a != c


def test_el_rol_cambia_el_mesh():
    cub = fondos.fondo(rol="cover", variante="mesh", rgb=(250, 204, 21))
    con = fondos.fondo(rol="contenido", variante="mesh", rgb=(250, 204, 21))
    assert _capas(cub["fondo"]) > _capas(con["fondo"])


def test_el_fondo_por_defecto_es_circuito():
    """La casa usa circuitos en TODOS los verticales y roles."""
    assert fondos.VARIANTE_DEFECTO == "circuitos"
    for vertical in ("cybersec", "dev", "ai", "infra", "data", "tech"):
        f = fondos.fondo(vertical=vertical, variante="auto")
        assert f["textura_size"].startswith("100% 100%"), vertical
        assert "svg" in f["textura"], vertical
    # `auto` y `circuitos` explícito dan el mismo look, código incluido
    auto = fondos.fondo(vertical="dev", variante="auto", comandos=["ls -la"])
    circ = fondos.fondo(vertical="dev", variante="circuitos",
                        comandos=["ls -la"])
    assert auto["fondo"] == circ["fondo"]
    assert auto["textura"] == circ["textura"]
    assert auto["codigo"] == circ["codigo"] != ""


def test_las_estrellas_ya_no_existen():
    """Se fueron por completo: ni capas blancas, ni el módulo, ni la tabla."""
    import importlib

    import pytest

    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("theme.stars")
    assert not hasattr(fondos, "TEXTURA_VERTICAL")
    for v in fondos.VARIANTES:
        for rol in fondos.ROLES:
            capas = fondos.fondo(rol=rol, variante=v)["fondo"]
            assert "255,255,255" not in capas, (v, rol)
            # la viñeta sigue: es lo que apaga los bordes y centra la atención
            assert "radial-gradient(ellipse 74% 60%" in capas, (v, rol)


def test_grano_presente_salvo_en_base():
    assert "base64" in fondos.fondo(variante="grid")["textura"]
    assert fondos.fondo(variante="base")["textura"] == "none"


def test_codigo_fantasma_escapa_html():
    html = fondos.codigo_html(comandos=['echo "<b>x</b>" && ls'])
    assert "<b>" not in html
    assert "&lt;b&gt;" in html
    assert "fondo-codigo" in html
    assert fondos.fondo(variante="base")["codigo"] == ""
    assert "fondo-codigo" in fondos.fondo(variante="codigo",
                                          comandos=["ls -la"])["codigo"]


def test_slide_generado_con_cada_variante_no_deja_tokens():
    for v in fondos.VARIANTES:
        html = _html(2, 4, fondo=v)
        assert "__fondo_img__" not in html, v
        assert "__textura_mask__" not in html, v
        assert "__fondo_codigo__" not in html, v
        assert "background-image:" in html, v


def test_roles_por_clase_de_slide():
    # En la variante `mesh` el rol cambia el numero de glows.
    cover = _html(1, 4, fondo="mesh")
    contenido = _html(2, 4, fondo="mesh")
    cierre = _html(4, 4, fondo="mesh")
    assert "radial-gradient" in cover and "radial-gradient" in cierre
    assert cover.count("radial-gradient") != contenido.count("radial-gradient") \
        or contenido.count("radial-gradient") != cierre.count("radial-gradient")


def test_fondo_fijo_iguala_todos_los_slides():
    a = _html(1, 4, fondo_fijo=True)
    b = _html(3, 4, fondo_fijo=True)
    def bloque(h):
        return h.split("background-image:")[1].split(";")[0]
    assert bloque(a) == bloque(b)
