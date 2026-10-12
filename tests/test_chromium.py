"""Fallback de GPU: si Chromium crashea, se reintenta una vez con bandera."""

import tech_carousel as tc


class _Resultado:
    def __init__(self, returncode=0, stdout=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = ""


def test_reintenta_con_in_process_gpu(monkeypatch):
    monkeypatch.setattr(tc, "_GPU_PROBLEMA", False)
    corridas = []

    def falso_run(cmd, **_kw):
        corridas.append(list(cmd))
        return _Resultado(returncode=1 if len(corridas) == 1 else 0)

    monkeypatch.setattr(tc.subprocess, "run", falso_run)
    r = tc._correr_chromium(tc._cmd_chromium("--dump-dom", "file:///x.html"),
                            espera=r'data-lineas="\d+"')
    assert len(corridas) == 2
    assert "--in-process-gpu" in corridas[1]
    assert "--in-process-gpu" not in corridas[0]
    assert r.returncode == 0


def test_bandera_queda_activa_para_no_repetir(monkeypatch):
    monkeypatch.setattr(tc, "_GPU_PROBLEMA", True)
    corridas = []

    def falso_run(cmd, **_kw):
        corridas.append(list(cmd))
        return _Resultado()

    monkeypatch.setattr(tc.subprocess, "run", falso_run)
    tc._correr_chromium(tc._cmd_chromium("--dump-dom", "file:///x.html"),
                        espera="nunca-va-a-aparecer")
    assert len(corridas) == 1
    assert "--in-process-gpu" in corridas[0]


def test_no_reintenta_si_la_salida_es_correcta(monkeypatch):
    monkeypatch.setattr(tc, "_GPU_PROBLEMA", False)
    corridas = []

    def falso_run(cmd, **_kw):
        corridas.append(list(cmd))
        return _Resultado(stdout='data-lineas="2"')

    monkeypatch.setattr(tc.subprocess, "run", falso_run)
    r = tc._correr_chromium(tc._cmd_chromium("--dump-dom", "file:///x.html"),
                            espera=r'data-lineas="\d+"')
    assert len(corridas) == 1
    assert r.stdout == 'data-lineas="2"'


def test_si_ya_lleva_la_bandera_no_duplica(monkeypatch):
    monkeypatch.setattr(tc, "_GPU_PROBLEMA", False)
    corridas = []

    def falso_run(cmd, **_kw):
        corridas.append(list(cmd))
        return _Resultado(returncode=1)

    monkeypatch.setattr(tc.subprocess, "run", falso_run)
    cmd = [tc.CHROMIUM, "--headless", "--no-sandbox", "--disable-gpu",
           "--in-process-gpu", "--dump-dom"]
    tc._correr_chromium(cmd)
    assert len(corridas) == 1


def test_comando_base_no_lleva_bandera_por_defecto(monkeypatch):
    monkeypatch.setattr(tc, "_GPU_PROBLEMA", False)
    cmd = tc._cmd_chromium("--dump-dom")
    assert cmd[0] == tc.CHROMIUM
    assert "--in-process-gpu" not in cmd
    assert "--disable-gpu" in cmd
