"""Texto: conteo de palabras y utilidades de copy."""

import re


def contar_palabras(texto):
    """Cuenta palabras visibles (sin markdown ni HTML)."""
    limpio = re.sub(r"<[^>]+>", " ", texto or "")
    limpio = re.sub(r"[#*>\-\[\]|_`]", " ", limpio)
    return len([p for p in limpio.split() if p])


def en_rango(texto, minimo, maximo):
    n = contar_palabras(texto)
    return minimo <= n <= maximo, n


def recortar(texto, max_palabras):
    """Corta en N palabras respetando finales de frase."""
    if not texto:
        return ""
    palabras = texto.split()
    if len(palabras) <= max_palabras:
        return texto
    corte = max_palabras
    for i in range(max_palabras, max(0, max_palabras - 8), -1):
        if re.search(r"[.!?…:]$", palabras[i - 1]):
            corte = i
            break
    return " ".join(palabras[:corte]) + "…"
