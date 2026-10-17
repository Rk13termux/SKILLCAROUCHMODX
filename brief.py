#!/usr/bin/env python3
"""brief.py — brief interactivo del tech-carousel.

Hace las 4 preguntas del brief (tipo de post → tema/color/slides →
componentes → extras) y lanza tech_carousel.py con el comando ya armado.

Uso:
    python3 brief.py            # interactivo
    python3 brief.py --dry-run  # sólo imprime el comando, no lo ejecuta
"""

import argparse
import shlex
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent

PRESETS = {
    "1": ("repo", "Reseña de repo (GitHub, estrellas, comandos de instalación)"),
    "2": ("comandos", "Comandos/CLI (terminal, pasos, errores típicos)"),
    "3": ("python", "Programación (editor, código, ruta de aprendizaje)"),
    "4": ("mixto", "Mixto (deja que la skill elija componentes)"),
}

FORMATOS = {"1": "9:16", "2": "4:5", "3": "1:1", "4": "3:4"}

VERTICALES = {
    "1": "prog", "2": "cybersec", "3": "ai", "4": "infra", "5": "auto",
}

COLORES = {
    "1": "#FACC15", "2": "#10B981", "3": "#06B6D4", "4": "#8B5CF6",
    "5": "#F97316", "6": "#EF4444", "7": "#3B82F6",
}


def _pedir(prompt, default=None, validador=None):
    sufijo = f" [{default}]" if default else ""
    while True:
        r = input(f"{prompt}{sufijo}: ").strip()
        if not r and default is not None:
            return default
        if not r:
            print("  (obligatorio)")
            continue
        if validador and not validador(r):
            print("  valor inválido, prueba de nuevo")
            continue
        return r


def _menu(titulo, opciones):
    print(f"\n{titulo}")
    for k, v in opciones.items():
        etiqueta = v[1] if isinstance(v, tuple) else v
        print(f"  {k}) {etiqueta}")
    return _pedir("Elige", default="1", validador=lambda x: x in opciones)


def main():
    ap = argparse.ArgumentParser(description="Brief interactivo del carrusel")
    ap.add_argument("--dry-run", action="store_true",
                    help="Sólo imprime el comando, sin ejecutarlo")
    args = ap.parse_args()

    print("== Brief del carrusel ==")
    print("(Enter para el valor por defecto)\n")

    tipo = _menu("1. Tipo de post:", PRESETS)
    preset = PRESETS[tipo][0]

    tema = _pedir("2. Slug del tema (ej: git-a-fondo)")
    display = _pedir("   Título visible", default=tema.replace("-", " ").title())
    short = _pedir("   Título corto", default=display)

    fmt = _menu("3. Formato:", {k: v for k, v in FORMATOS.items()})
    formato = FORMATOS[fmt]

    print("\n   Slides: 7-10 recomendado; 20+ para guía profunda.")
    slides = _pedir("4. Cantidad de slides", default="9",
                    validador=lambda x: x.isdigit() and int(x) >= 3)

    color_op = _menu("5. Color de acento:", COLORES)
    color = COLORES[color_op]

    def _es_color(x):
        if x.startswith("#") and len(x) == 7:
            try:
                int(x[1:], 16)
                return True
            except ValueError:
                return False
        try:
            sys.path.insert(0, str(SKILL_DIR))
            from theme import colors as _c
            _c.normalizar_hex(x)
            return True
        except Exception:
            return False

    color = _pedir("   (o escribe tu #RRGGBB)", default=color,
                   validador=_es_color)

    vertical_op = _menu("6. Vertical:", VERTICALES)
    vertical = VERTICALES[vertical_op]

    print("\n7. Extras (opcional):")
    marca = _pedir("   Marca", default="CHMODX")
    cta = _pedir("   Palabra CTA (slide final)", default=short.split()[0].upper())
    landing = _pedir("   Landing propia (vacío = sin landing)", default="")
    landing2 = ""
    if landing:
        landing2 = _pedir("   Segunda URL (Telegram; vacío = ninguna)")
    repo = ""
    if preset == "repo":
        repo = _pedir("   Repo GitHub (owner/name)")

    cmd = [sys.executable, str(SKILL_DIR / "tech_carousel.py"),
           "--tema", tema, "--color", color, "--slides", str(slides),
           "--formato", formato, "--vertical", vertical,
           "--display-tema", display, "--short-tema", short,
           "--marca", marca, "--cta-palabra", cta,
           "--preset", preset, "--copy-redes",
           "--contact-sheet"]
    if landing:
        cmd += ["--landing", landing]
    if landing2:
        cmd += ["--landing2", landing2]
    if repo:
        cmd += ["--repo", repo]

    print("\n== Comando ==")
    print("cd", SKILL_DIR)
    print(" ".join(shlex.quote(c) for c in cmd))
    if args.dry_run:
        return
    confirmar = input("\n¿Ejecutar ahora? [S/n]: ").strip().lower()
    if confirmar in ("n", "no"):
        print("Cancelado.")
        return
    print()
    raise SystemExit(subprocess.call(cmd, cwd=str(SKILL_DIR)))


if __name__ == "__main__":
    main()
