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


# ── F2: carpetas por red (unidad, sin Chromium) ────────────────────

def test_argv_para_red_quita_flags_y_fija_perfil():
    argv = ["--tema", "x", "--color", "#06B6D4", "--slides", "10",
            "--formato", "9:16", "--redes", "todas", "--slides-tiktok", "6",
            "--workers", "2"]
    cmd = tc._argv_para_red(argv, "tiktok", 8, "9:16", [1, 2, 4, 9, 10])
    assert "--redes" not in cmd and "todas" not in cmd
    assert cmd.count("--slides") == 1
    assert cmd[cmd.index("--slides") + 1] == "8"
    assert cmd[cmd.index("--formato") + 1] == "9:16"
    assert cmd[cmd.index("--red-destino") + 1] == "tiktok"
    assert cmd[cmd.index("--recorte") + 1] == "1,2,4,9,10"
    assert "--slides-tiktok" not in cmd and "6" not in cmd
    assert cmd[cmd.index("--workers") + 1] == "2"


def test_orquestar_redes_abre_un_proceso_por_red(monkeypatch, capsys):
    llamadas = []

    class _R:
        returncode = 0

    def fake_run(cmd, **kw):
        llamadas.append(cmd)
        return _R()

    monkeypatch.setattr(tc.subprocess, "run", fake_run)
    plan = redes.planear(10, ["tiktok", "instagram", "facebook"])
    fallidos = tc._orquestar_redes(
        type("A", (), {"red_destino": None})(), plan,
        ["--tema", "x", "--color", "#06B6D4", "--slides", "10"])
    assert fallidos == []
    assert len(llamadas) == 3
    for cmd, item in zip(llamadas, plan):
        assert "--red-destino" in cmd
        assert cmd[cmd.index("--red-destino") + 1] == item["red"]


def test_orquestar_redes_no_recursa(monkeypatch):
    llamadas = []
    monkeypatch.setattr(tc.subprocess, "run",
                        lambda cmd, **kw: llamadas.append(cmd))
    plan = redes.planear(10, ["tiktok"])
    tc._orquestar_redes(type("A", (), {"red_destino": "tiktok"})(), plan,
                        ["--tema", "x"])
    assert llamadas == []


def test_escribir_perfil(tmp_path, capsys):
    import json
    from types import SimpleNamespace
    args = SimpleNamespace(red_destino="facebook", formato="4:5",
                           tema="mi-tema")
    slides = []
    tc._escribir_perfil(tmp_path, args, 6, [1, 2, 5, 9, 10], slides)
    datos = json.loads((tmp_path / "perfil.json").read_text())
    assert datos["red"] == "facebook"
    assert datos["formato"] == "4:5"
    assert datos["slides"] == 6
    assert datos["recorte"] == [1, 2, 5, 9, 10]
    assert datos["copy"]["hashtags"] == 5
    assert "bottom" in datos["zona_segura"]


def test_escribir_perfil_no_op_en_legacy(tmp_path):
    from types import SimpleNamespace
    args = SimpleNamespace(red_destino=None, formato="9:16", tema="x")
    tc._escribir_perfil(tmp_path, args, 8, None, [])
    assert not (tmp_path / "perfil.json").exists()


# ── F3: copy por red ──────────────────────────────────────────────

def test_presupuestos_coinciden_con_los_perfiles():
    from generar_copy_tech import PRESUPUESTO
    nombre = {"instagram": "Instagram", "tiktok": "TikTok",
              "facebook": "Facebook"}
    for red, p in redes.PERFILES.items():
        assert PRESUPUESTO[nombre[red]] == (p.copy_min, p.copy_max)


def test_copy_por_red_escribe_caption_y_copy(tmp_path):
    from generar_copy_tech import generar_copy_redes
    for red in ("instagram", "tiktok", "facebook"):
        p = redes.perfil(red)
        r = generar_copy_redes(
            tmp_path, "IDOR en APIs REST", "IDOR", "CHMODX",
            vertical="cybersec", landing="https://chmodxcode.pro",
            solo=red, destino=tmp_path / red)
        assert (tmp_path / red / "caption.txt").is_file()
        assert (tmp_path / red / "copy.md").is_file()
        assert p.copy_min <= r["palabras"] <= p.copy_max, (red, r["palabras"])
        md = (tmp_path / red / "copy.md").read_text(encoding="utf-8")
        assert f"utm_source={red}" in md
        tags = (tmp_path / red / "caption.txt").read_text().count("#")
        assert tags >= p.hashtags


def test_copy_red_desconocida_falla(tmp_path):
    from generar_copy_tech import generar_copy_redes
    with pytest.raises(ValueError):
        generar_copy_redes(tmp_path, "X", "X", "CHMODX", solo="myspace")


def test_copy_red_usa_el_slug_real_no_el_de_la_carpeta(tmp_path):
    """La carpeta de destino es `tiktok/`: el slug debe seguir siendo el tema."""
    from generar_copy_tech import generar_copy_redes
    generar_copy_redes(tmp_path, "IDOR en APIs REST", "IDOR", "CHMODX",
                       vertical="cybersec", solo="tiktok",
                       destino=tmp_path / "tiktok", slug="idor-apis-rest")
    md = (tmp_path / "tiktok" / "copy.md").read_text(encoding="utf-8")
    assert "`idor-apis-rest`" in md
    caption = (tmp_path / "tiktok" / "caption.txt").read_text()
    assert "#tiktok" not in caption
