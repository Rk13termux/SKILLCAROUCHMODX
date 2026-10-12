"""Resolución de rutas y binarios compartida por el builder y el generador."""

import os
import shutil
from pathlib import Path


def resolver_ctslider() -> Path:
    """Carpeta CTSLIDER: env > /mnt/sdcard > home."""
    for c in (os.environ.get("CTSLIDER_DIR"), "/mnt/sdcard/CTSLIDER",
              str(Path.home() / "CTSLIDER")):
        if c and Path(c).is_dir():
            return Path(c)
    return Path(next((c for c in (os.environ.get("CTSLIDER_DIR"),
                                  "/mnt/sdcard/CTSLIDER") if c),
                     "/mnt/sdcard/CTSLIDER"))


def resolver_chromium() -> str:
    """Binario de Chromium/Chrome headless: env > Termux > PATH."""
    env = os.environ.get("CHROMIUM")
    if env:
        return env
    termux = "/data/data/com.termux/files/usr/bin/chromium-browser"
    if Path(termux).exists():
        return termux
    for nombre in ("chromium-browser", "chromium", "google-chrome",
                   "google-chrome-stable", "chromium-headless-shell"):
        ruta = shutil.which(nombre)
        if ruta:
            return ruta
    return termux
