"""Slug: nombres de carpeta estables para CTSLIDER."""

import re
import unicodedata


def slugificar(texto, max_palabras=8):
    """Minúsculas, sin acentos, guiones. Máximo N palabras."""
    norm = "".join(
        c for c in unicodedata.normalize("NFKD", (texto or "").lower())
        if not unicodedata.combining(c)
    )
    norm = re.sub(r"[^a-z0-9]+", "-", norm).strip("-")
    return "-".join(norm.split("-")[:max_palabras])
