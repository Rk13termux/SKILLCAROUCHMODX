"""Consulta la API pública de GitHub para datos reales de un repo.

Sin dependencias: usa `urllib` de la stdlib. Cachea por repo en el proceso
(el render paralelo puede pedir el mismo repo varias veces).

Uso:
    from utils.github import fetch_repo
    data = fetch_repo("psf/requests")   # None si falla o no hay red
"""

import json
import urllib.error
import urllib.request

_API = "https://api.github.com/repos/"
_TIMEOUT = 6
_CACHE = {}
_UA = "chmodx-carousel/1.0 (+https://chmodxcode.pro)"


def _get(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": _UA,
        "Accept": "application/vnd.github+json",
    })
    with urllib.request.urlopen(req, timeout=_TIMEOUT) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def fetch_repo(slug, max_langs=4):
    """{stars, forks, issues, licencia, desc, lenguajes:[{n,p}]} o None."""
    slug = (slug or "").strip().strip("/")
    if slug.count("/") != 1 or not all(slug.split("/")):
        return None
    if slug in _CACHE:
        return _CACHE[slug]
    try:
        info = _get(_API + slug)
        langs_raw = _get(_API + slug + "/languages")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError,
            ValueError, OSError):
        _CACHE[slug] = None
        return None
    total = sum(langs_raw.values()) or 1
    langs = sorted(({"n": k, "p": round(v * 100 / total)}
                    for k, v in langs_raw.items()),
                   key=lambda d: d["p"], reverse=True)[:max_langs]
    lic = (info.get("license") or {}).get("spdx_id") or ""
    if lic in ("NOASSERTION", "None"):
        lic = ""
    data = {
        "stars": info.get("stargazers_count", 0),
        "forks": info.get("forks_count", 0),
        "issues": info.get("open_issues_count", 0),
        "licencia": lic,
        "desc": (info.get("description") or "")[:120],
        "lenguajes": langs,
    }
    _CACHE[slug] = data
    return data


def _fmt(n):
    n = int(n)
    if n >= 1000:
        return f"{n / 1000:.1f}k".replace(".0k", "k")
    return str(n)


def props_desde_repo(slug):
    """Props listas para el componente gh-stats, o None."""
    d = fetch_repo(slug)
    if not d:
        return None
    return {
        "repo": slug,
        "desc": d["desc"],
        "stars": _fmt(d["stars"]),
        "forks": _fmt(d["forks"]),
        "issues": _fmt(d["issues"]),
        "licencia": d["licencia"],
        "lenguajes": d["lenguajes"],
    }
