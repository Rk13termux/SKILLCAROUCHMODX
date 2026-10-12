"""Regla de keywords por línea (bug B1).

El conteo no depende del tipo de comilla: un copy escrito con class='clave'
contaba 0 claves y desactivaba la regla sin avisar.
"""

from tech_carousel import _RE_CLAVE, _clave_candidatas, contar_claves


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
