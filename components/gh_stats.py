"""Componente gh-stats: ficha de repositorio GitHub (stars, forks, lenguajes)."""

import html as _html

MAX_LANGS = 4

_COLORES_LANG = {
    "python": "#3572A5", "javascript": "#F1E05A", "typescript": "#3178C6",
    "go": "#00ADD8", "rust": "#DEA584", "shell": "#89E051", "bash": "#89E051",
    "java": "#B07219", "c": "#555555", "c++": "#F34B7D", "html": "#E34C26",
    "css": "#563D7C", "ruby": "#701516", "php": "#4F5D95", "swift": "#F05138",
    "kotlin": "#A97BFF", "dart": "#00B4AB", "lua": "#000080",
    "jupyter notebook": "#DA5B0B", "dockerfile": "#384D54", "yaml": "#CB171E",
}


def render(props, ctx, warnings=None):
    repo = props.get("repo") or props.get("nombre") or "usuario/repo"
    # Datos reales desde la API de GitHub (opt-in con "auto": true).
    if props.get("auto") or props.get("real"):
        try:
            import sys
            from pathlib import Path
            raiz = str(Path(__file__).resolve().parents[1])
            if raiz not in sys.path:
                sys.path.insert(0, raiz)
            from utils.github import props_desde_repo
            real = props_desde_repo(str(repo))
            if real:
                real.update({k: v for k, v in props.items()
                             if k not in ("auto", "real") and v})
                props = real
                repo = props.get("repo") or repo
            elif warnings is not None:
                warnings.append(f"gh-stats: no se pudo leer '{repo}' de la API "
                                "de GitHub (se usan los valores escritos)")
        except Exception as e:  # noqa: BLE001
            if warnings is not None:
                warnings.append(f"gh-stats: fallo consultando GitHub ({e})")
    desc = props.get("desc") or props.get("descripcion") or ""
    stars = props.get("stars") or props.get("estrellas") or "—"
    forks = props.get("forks") or "—"
    issues = props.get("issues") or props.get("temas") or "—"
    licencia = props.get("licencia") or props.get("license") or ""
    langs = props.get("lenguajes") or props.get("languages") or []
    if len(langs) > MAX_LANGS:
        if warnings is not None:
            warnings.append(f"gh-stats: {len(langs)} lenguajes > {MAX_LANGS}, se recortan")
        langs = langs[:MAX_LANGS]
    segs, leyenda = [], []
    for lg in langs:
        if isinstance(lg, str):
            lg = {"n": lg, "p": 0}
        nombre = str(lg.get("n") or lg.get("nombre") or "")
        try:
            pct = max(0, min(100, float(lg.get("p") or lg.get("pct") or 0)))
        except (TypeError, ValueError):
            pct = 0
        color = _COLORES_LANG.get(nombre.lower(), "#9CA3AF")
        segs.append(f'<span class="ghstats__seg" style="width:{pct}%;'
                    f'background:{color}"></span>')
        leyenda.append(
            f'<span class="ghstats__lang"><span class="ghstats__dot" '
            f'style="background:{color}"></span>{_html.escape(nombre)} '
            f'{pct:g}%</span>')
    barra = (f'<div class="ghstats__bar">{"".join(segs)}</div>'
             f'<div class="ghstats__langs">{" ".join(leyenda)}</div>' if segs else "")
    lic = (f'<span class="ghstats__lic">{_html.escape(str(licencia))}</span>'
           if licencia else "")
    return (
        '<div class="ghstats">'
        f'<div class="ghstats__repo">{_html.escape(str(repo))} {lic}</div>'
        + (f'<div class="ghstats__desc">{_html.escape(str(desc))}</div>' if desc else "")
        + f'<div class="ghstats__nums"><span>★ {_html.escape(str(stars))} stars</span>'
        f'<span>{_html.escape(str(forks))} forks</span>'
        f'<span>{_html.escape(str(issues))} issues</span></div>'
        + barra + '</div>'
    )
