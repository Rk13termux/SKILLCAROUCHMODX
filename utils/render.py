"""Resolución de rutas y binarios compartida por el builder y el generador."""

import os
import shutil
from pathlib import Path


def resolver_ctslider() -> Path:
    """Carpeta CTSLIDER: env > /mnt/sdcard (Termux) > home."""
    env = os.environ.get("CTSLIDER_DIR")
    sdcard = "/sdcard/CTSLIDER"
    termux = "/mnt/sdcard/CTSLIDER"
    home = Path.home() / "CTSLIDER"
    for c in (env, sdcard, termux, str(home)):
        if c and Path(c).is_dir():
            return Path(c)
    # Ninguna existe todavía: prioriza la que se pueda crear.
    if env:
        return Path(env)
    for c in (sdcard, termux):
        if Path(c).parent.is_dir() and os.access(Path(c).parent, os.W_OK):
            return Path(c)
    return home


def resolver_chromium() -> str:
    """Binario de Chromium/Chrome headless: env > Termux > PATH."""
    env = os.environ.get("CHROMIUM")
    if env:
        return env
    termux = "/data/data/com.termux/files/usr/bin/chromium-browser"
    if Path(termux).exists():
        return termux
    for nombre in ("chromium-browser", "chromium", "google-chrome",
                   "google-chrome-stable", "chromium-headless-shell",
                   "chrome-headless-shell"):
        ruta = shutil.which(nombre)
        if ruta:
            return ruta
    # Builds de Playwright/Puppeteer sin registrar en PATH (aarch64 sin root).
    cache = Path.home() / ".cache"
    patrones = ("ms-playwright/chromium*_*/chrome-headless-shell-*/chrome-headless-shell",
                "ms-playwright/chromium*_*/chrome-linux*/chrome",
                "puppeteer/chrome*/*/chrome-headless-shell-linux-*/chrome-headless-shell")
    for patron in patrones:
        for ruta in sorted(cache.glob(patron), reverse=True):
            if ruta.is_file() and os.access(ruta, os.X_OK):
                return str(ruta)
    return termux
