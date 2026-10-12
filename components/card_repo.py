"""Card de repositorio (mock de proyecto / README)."""

import html as _html


def _install_lineas(cmd):
    lineas = []
    for ln in str(cmd).strip().splitlines():
        ln = ln.strip()
        if not ln:
            continue
        if ln.startswith("$"):
            cuerpo = _html.escape(ln)
            lineas.append(f'<div><span class="prompt">$</span> '
                          f"{cuerpo[1:].strip()}</div>")
        else:
            lineas.append(f"<div>{_html.escape(ln)}</div>")
    return "".join(lineas)


def render(props, ctx, warnings=None):
    repo = str(props.get("repo") or props.get("nombre") or "org/proyecto")
    desc = _html.escape(str(props.get("desc") or props.get("descripcion") or ""))
    tree = str(props.get("tree") or props.get("estructura") or "").strip()
    install = str(props.get("install") or props.get("instalacion") or "").strip()
    badges = props.get("badges") or []
    if isinstance(badges, str):
        badges = [badges]

    # repo "owner/name": owner tenue, nombre en acento
    if "/" in repo:
        owner, nombre = repo.split("/", 1)
        repo_html = (f'<span class="repo-card__owner">{_html.escape(owner)}/</span>'
                     f"<b>{_html.escape(nombre)}</b>")
        barra = f"~/projects/<span>{_html.escape(owner)}</span>/<b>{_html.escape(nombre)}</b>"
    else:
        repo_html = f"<b>{_html.escape(repo)}</b>"
        barra = f"~/projects/<b>{_html.escape(repo)}</b>"

    badges_html = ""
    if badges:
        chips = []
        for b in badges[:5]:
            if isinstance(b, dict):
                texto, clase = str(b.get("v") or b.get("text") or ""), (
                    "chip--ok" if b.get("ok") else "")
            else:
                texto, clase = str(b), ("chip--ok" if str(b).lower() in
                                        ("ok", "estable", "stable", "passing") else "")
            chips.append(f'<span class="chip {clase}">{_html.escape(texto)}</span>')
        badges_html = f'<div class="repo-card__badges">{"".join(chips)}</div>'

    tree_html = f'<div class="repo-card__tree">{_html.escape(tree)}</div>' if tree else ""
    install_html = ""
    if install:
        install_html = (f'<div class="repo-card__install">'
                        f"{_install_lineas(install)}</div>")

    return (
        '<div class="repo-card">'
        f'<div class="repo-card__bar"><span class="repo-card__path">{barra}</span></div>'
        '<div class="repo-card__body">'
        f'<div class="repo-card__nombre">{repo_html}</div>'
        f'<div class="repo-card__desc">{desc}</div>'
        f"{badges_html}{tree_html}{install_html}"
        "</div></div>"
    )
