"""Modo landing: el cierre (N-1 y N) enlaza a un dominio propio.

`--landing https://chmodxcode.pro` reemplaza la lógica de "SÍGUENOS" por un
funnel al dominio, manteniendo los comandos del primer comentario. Sin el
flag, los slides tienen que quedar EXACTAMENTE como antes (regresión).
"""

from tech_carousel import FORMATOS, _landing_dominio, generar_html
from theme import colors as _colors

KW = {"__resalte__": "#06B6D4", "__resalte_brillo__": "#3DD2EE",
      "__resalte_rgba32__": "rgba(6,182,212,0.32)",
      "__resalte_rgba38__": "rgba(6,182,212,0.38)"}
COMANDOS = ["python3 --version", "pip install requests", "git clone repo"]

ACCENT = _colors.acento_vars("#06B6D4")


def _slide(i, n, landing=None, body=""):
    data = {"number": f"{i}/{n}",
            "body": body or ('<div class="titulo">Titular <span '
                             'class="clave">clave</span></div>'
                             '<div class="cuerpo">Cuerpo de prueba.</div>'),
            "footer": "CHMODX · demo"}
    return generar_html(i, n, data, "9:16", FORMATOS["9:16"], ACCENT, None,
                        "CHMODX", resalte_vars=KW, semilla="demo",
                        comandos_finales=COMANDOS, cta_modo="seguir",
                        recap_titulos=["Instala Python hoy",
                                       "Escribe tu primera función",
                                       "Publica tu proyecto"], landing=landing)


# ── _landing_dominio ───────────────────────────────────────────────

def test_dominio_limpia_url():
    assert _landing_dominio("https://chmodxcode.pro/") == "chmodxcode.pro"
    assert _landing_dominio("http://www.chmodxcode.pro") == "chmodxcode.pro"
    assert _landing_dominio("chmodxcode.pro") == "chmodxcode.pro"
    assert _landing_dominio("") == ""


# ── Slide N con landing ────────────────────────────────────────────

def test_final_con_landing_muestra_dominio_como_cta_primario():
    html = _slide(7, 7, landing="https://chmodxcode.pro")
    assert 'class="landing-card"' in html
    assert "chmodxcode.pro" in html
    assert "EMPIEZA EN" in html
    # botón sin flecha
    assert "&#8594" not in html and "→" not in html
    # los comandos siguen presentes y la línea fina apunta al comentario
    assert "terminal" in html
    assert "primer comentario" in html


def test_final_con_landing_no_ofrece_siguens():
    html = _slide(7, 7, landing="https://chmodxcode.pro")
    assert "SÍGUENOS" not in html
    assert "COPIA LOS COMANDOS DEL" not in html


def test_final_con_landing_limita_los_comandos_del_terminal():
    html = _slide(7, 7, landing="https://chmodxcode.pro")
    for cmd in COMANDOS:
        assert cmd in html


# ── Slide N-1 con landing ──────────────────────────────────────────

def test_puente_con_landing_invita_a_programar_y_muestra_dominio():
    html = _slide(6, 7, landing="https://chmodxcode.pro")
    assert 'class="landing-mini"' in html
    assert "chmodxcode.pro" in html
    assert "empieza a programar" in html
    # mantiene el recap de 3 ideas
    assert "Lo esencial en 3 ideas" in html


# ── Regresión sin el flag ──────────────────────────────────────────

def test_sin_landing_se_mantiene_el_cierre_viejo():
    html = _slide(7, 7)
    assert 'class="landing-card"' not in html
    assert "COPIA LOS COMANDOS DEL" in html
    assert "SÍGUENOS" in html


def test_puente_sin_landing_usa_el_titulo_de_recap():
    html = _slide(6, 7)
    assert 'class="landing-mini"' not in html
    assert "Antes del final: el resumen" in html
