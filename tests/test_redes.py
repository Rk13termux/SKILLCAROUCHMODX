"""Perfiles de red: resolución, recorte de slides y no-regresión de la salida."""

import sys

import pytest

import redes
import tech_carousel as tc

PLANTILLA = """<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
.titulo {{ font-weight: 700; }} .cuerpo {{ font-weight: 400; }}
.clave {{ font-weight: 700; color: #06B6D4; }}
</style></head><body>
  <div class="numero">{i}/{n}</div>
  <div class="slide"><div class="contenido">
    <div class="titulo">Slide {i}</div>
    <div class="cuerpo">Contenido de prueba con una <span class="clave">idea</span>.</div>
  </div><div class="pie"><span class="logo"></span>CHMODX · Test</div></div>
</body></html>
"""


def _tema(base, n=6):
    carpeta = base / "tema-redes"
    carpeta.mkdir(parents=True, exist_ok=True)
    for i in range(1, n + 1):
        (carpeta / f"slide-{i:02d}.html").write_text(
            PLANTILLA.format(i=i, n=n), encoding="utf-8")
    return carpeta


# ── Perfiles ──────────────────────────────────────────────────────

def test_resolver_todas():
    assert redes.resolver_redes("todas") == ["tiktok", "instagram", "facebook"]


def test_resolver_orden_canonico_sin_duplicados():
    assert redes.resolver_redes("facebook, tiktok, facebook") == [
        "tiktok", "facebook"]


def test_resolver_vacio():
    assert redes.resolver_redes(None) == []
    assert redes.resolver_redes("") == []


def test_resolver_desconocida():
    with pytest.raises(ValueError) as exc:
        redes.resolver_redes("myspace")
    assert "myspace" in str(exc.value)


def test_formatos_por_perfil():
    assert redes.perfil("tiktok").formato == "9:16"
    assert redes.perfil("instagram").formato == "4:5"
    assert redes.perfil("facebook").formato == "4:5"


# ── Recorte de slides ─────────────────────────────────────────────

def test_sin_recorte_si_entra():
    idx, fuera = redes.seleccion("instagram", 8)
    assert idx == list(range(1, 9)) and fuera == []


def test_recorta_por_perfil_y_conserva_portada_y_cierre():
    idx, fuera = redes.seleccion("tiktok", 10)
    assert len(idx) == redes.perfil("tiktok").slides_max
    assert idx[0] == 1 and idx[-1] == 10
    assert 9 in idx          # el puente nunca se cae
    assert fuera and 3 not in idx


def test_recorte_forzado():
    idx, _ = redes.seleccion("facebook", 10, forzado=4)
    assert len(idx) == 4
    assert idx[0] == 1 and idx[-1] == 10


def test_fuente_corta_falla():
    with pytest.raises(ValueError):
        redes.seleccion("tiktok", 2)


def test_plan_avisa_slides_fuera():
    plan = redes.planear(10, ["tiktok", "instagram"])
    tiktok, insta = plan
    assert tiktok["avisos"] and "slide-" in tiktok["avisos"][0]
    assert insta["avisos"] == []
    assert insta["n"] == 10


# ── CLI ───────────────────────────────────────────────────────────

def _main(monkeypatch, *args):
    monkeypatch.setattr(sys, "argv", ["tech_carousel.py", *args])
    with pytest.raises(SystemExit) as exc:
        tc.main()
    return exc.value


def test_cli_red_invalida(monkeypatch):
    codigo = _main(monkeypatch, "--tema", "tema-redes", "--color", "#06B6D4",
                   "--slides", "6", "--redes", "myspace")
    assert "myspace" in str(codigo)


def test_check_con_redes_no_escribe_carpetas(tmp_path, monkeypatch, capsys):
    _tema(tmp_path, 6)
    monkeypatch.setattr(tc, "CTSLIDER", tmp_path)
    codigo = _main(monkeypatch, "--tema", "tema-redes", "--color", "#06B6D4",
                   "--slides", "6", "--redes", "todas", "--check")
    assert codigo.code == 0
    texto = capsys.readouterr().out
    assert "Perfiles de red:" in texto
    for red in ("tiktok", "instagram", "facebook"):
        assert red in texto
        # F1 no escribe nada: las carpetas aparecen recién en F2.
        assert not (tmp_path / "tema-redes" / red).exists()


def test_sin_redes_no_hay_plan(tmp_path, monkeypatch, capsys):
    _tema(tmp_path, 6)
    monkeypatch.setattr(tc, "CTSLIDER", tmp_path)
    _main(monkeypatch, "--tema", "tema-redes", "--color", "#06B6D4",
          "--slides", "6", "--check")
    assert "Perfiles de red:" not in capsys.readouterr().out
