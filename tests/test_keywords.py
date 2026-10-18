"""Regla de keywords por línea (bug B1).

El conteo no depende del tipo de comilla: un copy escrito con class='clave'
contaba 0 claves y desactivaba la regla sin avisar.
"""

import re

from tech_carousel import (CUERPO_MAX_PALABRAS, HOOK_MAX_PALABRAS, _RE_CLAVE,
                           _clave_candidatas, _partir_token, _texto_de,
                           contar_claves)


def test_cuenta_comillas_dobles():
    assert contar_claves('<span class="clave">sql</span>') == 1


def test_cuenta_comillas_simples():
    assert contar_claves("<span class='clave'>sql</span>") == 1


def test_cuenta_mixtas():
    html = ('<span class="clave">a</span> y <span class=\'clave\'>b</span>')
    assert contar_claves(html) == 2


def test_no_cuenta_atributos_parecidos():
    assert contar_claves('<div class="clave-vieja">x</div>') == 0
    assert contar_claves('<div class="mi-clave">x</div>') == 0
    assert contar_claves("clave sin atributo") == 0


def test_regex_acepta_ambas_comillas():
    assert _RE_CLAVE.search('class="clave"')
    assert _RE_CLAVE.search("class='clave'")


def test_una_linea_da_una_clave():
    assert contar_claves(_clave_candidatas("Cómo se defiende", 1)) == 1


def test_dos_lineas_dan_dos_claves():
    titulo = "Cómo se defiende de la inyección SQL"
    assert contar_claves(_clave_candidatas(titulo, 2)) == 2


def test_candidatas_respeta_claves_existentes():
    titulo = 'Antes de <span class="clave">publicar</span>, medí el recorte'
    assert contar_claves(_clave_candidatas(titulo, 1)) == 1


# ── La puntuación no entra en el span (bug real en portada publicada) ──

def test_partir_token_deja_solo_la_palabra():
    assert _partir_token("¿Tu") == ("¿", "Tu", "")
    assert _partir_token("fuga?") == ("", "fuga", "?")
    assert _partir_token("(Python),") == ("(", "Python", "),")
    assert _partir_token("...") == ("", "", "...")  # sin núcleo


def test_clave_no_se_come_la_puntuacion():
    """«...una fuga?» marcaba también el signo de interrogación."""
    salida = _clave_candidatas("¿Tu correo ya está en una fuga?", 2)
    dentro = re.findall(r'<span class="clave">(.*?)</span>', salida)
    assert len(dentro) == 2
    for d in dentro:
        assert d == d.strip("¿?¡!.,;:'\"()")
    # El texto visible no cambia: solo se agregan spans.
    assert re.sub(r"<[^>]+>", "", salida) == "¿Tu correo ya está en una fuga?"


def test_clave_con_guion_se_mantiene_entera():
    salida = _clave_candidatas("Herramientas zero-day para pentest", 2)
    dentro = re.findall(r'<span class="clave">(.*?)</span>', salida)
    assert "zero-day" in dentro


# ── Límites de copy (documentados en SKILL.md) ─────────────────────

def test_texto_de_extrae_sin_entidades():
    assert _texto_de('<div class="cuerpo">Hola &amp; adiós</div>',
                     "cuerpo") == "Hola & adiós"
    assert _texto_de('<div class="cuerpo-x">nada</div>', "cuerpo") == ""


def test_limites_de_copy():
    assert HOOK_MAX_PALABRAS == 8
    assert 40 <= CUERPO_MAX_PALABRAS <= 55
