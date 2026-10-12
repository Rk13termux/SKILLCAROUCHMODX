"""CLI: mensajes claros y `--help` que nunca revienta (argparse % literal)."""

import sys

import pytest

import tech_carousel as tc


def _main(monkeypatch, *args):
    monkeypatch.setattr(sys, "argv", ["tech_carousel.py", *args])
    with pytest.raises(SystemExit) as exc:
        tc.main()
    return exc.value


def test_help_no_revienta(capsys, monkeypatch):
    """Un '%' literal en un help rompía argparse con TypeError."""
    salida = _main(monkeypatch, "--help")
    assert salida.code == 0
    texto = capsys.readouterr().out
    assert "--tema" in texto and "--formato" in texto
    assert "--no-auto" in texto and "--offline" in texto
    assert "--copy-redes" in texto


def test_color_invalido_explica_el_formato(capsys, monkeypatch):
    salida = _main(monkeypatch, "--tema", "zzz-test-cli",
                   "--color", "turquesa", "--slides", "5")
    texto = capsys.readouterr().out + str(salida)
    assert "turquesa" in texto
    assert "#RRGGBB" in texto and "#06B6D4" in texto
    assert "cian" in texto


def test_slides_minimo(capsys, monkeypatch):
    salida = _main(monkeypatch, "--tema", "zzz-test-cli",
                   "--color", "#06B6D4", "--slides", "2")
    assert "mínimo" in str(salida)


def test_carpeta_vacia_con_no_auto_explica_como_seguir(capsys, monkeypatch):
    salida = _main(monkeypatch, "--tema", "zzz-test-cli-que-no-existe",
                   "--color", "#06B6D4", "--slides", "5", "--no-auto")
    texto = capsys.readouterr().out + str(salida)
    assert "slide-*.html" in texto
    assert "--no-auto" in texto
    assert "generar_copy_tech.py" in texto


def test_recuento_no_coincide_lista_los_archivos(tmp_path, monkeypatch, capsys):
    carpeta = tmp_path / "parcial"
    carpeta.mkdir()
    for i in (1, 2):
        (carpeta / f"slide-{i:02d}.html").write_text("x", encoding="utf-8")
    monkeypatch.setattr(tc, "CTSLIDER", tmp_path)
    salida = _main(monkeypatch, "--tema", "parcial", "--color", "#06B6D4",
                   "--slides", "5")
    texto = capsys.readouterr().out + str(salida)
    assert "no coincide" in texto and "hay 2" in texto
    assert "slide-01.html" in texto
    assert "--slides 2" in texto
