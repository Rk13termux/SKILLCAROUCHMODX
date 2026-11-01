"""Tokens de layout + CSS compartido de componentes.

Todo el CSS de componente vive aquí (scoped bajo `.slide`) para que el
TEMPLATE del builder sólo tenga que inyectar `__componentes_css__`.
Los tamaños por formato los aporta el builder (scaling dict).
"""

# CSS base de componentes. Vars usadas:
#   --acento, --resalte, y tokens fijos de theme.colors
COMPONENTES_CSS = """
  /* ── Terminal / CLI ─────────────────────────────── */
  .terminal {
    background: var(--surf) padding-box, var(--borde-deg) border-box;
    border: 1.5px solid transparent;
    border-radius: 20px;
    overflow: hidden;
    text-align: left;
    box-shadow: var(--sombra), var(--sombra-edge);
    margin: 0 auto;
    width: 100%;
  }
  .terminal__bar {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 15px 20px;
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.05), transparent);
    border-bottom: 1px solid var(--linea);
  }
  .terminal__dot { width: 13px; height: 13px; border-radius: 50%; box-shadow: 0 0 10px currentColor; }
  .terminal__dot--r { background: #EF4444; color: #EF4444; }
  .terminal__dot--y { background: #F59E0B; color: #F59E0B; }
  .terminal__dot--g { background: #10B981; color: #10B981; }
  .terminal__titulo {
    margin-left: 10px;
    font-family: 'Hasklig', 'JetBrains Mono', 'SFMono-Regular', Menlo, Consolas, monospace;
    font-size: 0.74em;
    font-weight: 700;
    color: #8B93A1;
  }
  .terminal__live {
    margin-left: auto;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-family: 'Hasklig', 'JetBrains Mono', 'SFMono-Regular', Menlo, Consolas, monospace;
    font-size: 0.66em;
    font-weight: 800;
    letter-spacing: 2px;
    color: var(--acento);
    text-transform: uppercase;
  }
  .terminal__live::before {
    content: "";
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--acento);
    box-shadow: 0 0 12px var(--acento);
  }
  .terminal__body { padding: 20px 22px; background: var(--surf-2); }
  .terminal__line {
    font-family: 'Hasklig', 'JetBrains Mono', 'SFMono-Regular', Menlo, Consolas, monospace;
    font-size: 0.92em;
    line-height: 1.6;
    word-break: break-word;
    white-space: pre-wrap;
    color: #C9CFDA;
  }
  .terminal__line + .terminal__line { margin-top: 7px; }
  .terminal__line .prompt { color: var(--acento); font-weight: 800; }
  .terminal__line--cmd {
    color: #F8FAFC;
    font-weight: 600;
    background: rgba(255, 255, 255, 0.035);
    border-left: 3px solid var(--acento);
    border-radius: 0 8px 8px 0;
    padding: 5px 12px;
    margin-left: -12px;
  }
  .terminal__line--out { color: #8B93A1; }
  .terminal__line--ok { color: #34D399; font-weight: 600; }
  .terminal__line--err { color: #F87171; font-weight: 600; }
  .terminal__line--warn { color: #FBBF24; font-weight: 600; }
  .terminal__line .cmt { color: #5C6473; }

  /* ── Card informativa ───────────────────────────── */
  .card-info {
    border: 1.5px solid transparent;
    background: var(--surf) padding-box, var(--borde-deg) border-box;
    border-radius: 20px;
    padding: 26px 30px 28px 34px;
    text-align: left;
    position: relative;
    overflow: hidden;
    box-shadow: var(--sombra), var(--sombra-edge);
  }
  .card-info::before {
    content: "";
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 5px;
    background: linear-gradient(180deg,
      var(--card-borde, #3B82F6),
      color-mix(in srgb, var(--card-borde, #3B82F6) 25%, transparent) 78%,
      transparent);
  }
  .card-info__head {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 15px;
  }
  .card-info__ico {
    flex: 0 0 auto;
    font-size: 0.9em;
    width: 2em; height: 2em;
    border-radius: 0.5em;
    display: flex; align-items: center; justify-content: center;
    background: color-mix(in srgb, var(--card-borde, #3B82F6) 16%, transparent);
    border: 1px solid color-mix(in srgb, var(--card-borde, #3B82F6) 42%, transparent);
    box-shadow: 0 0 26px -6px color-mix(in srgb, var(--card-borde, #3B82F6) 60%, transparent);
    color: var(--card-borde, #3B82F6);
    font-weight: 800;
  }
  .card-info__ico img { width: 1.3em; height: 1.3em; display: block; }
  .card-info__titulo {
    font-weight: 800;
    font-size: 1.32em;
    line-height: 1.2;
    letter-spacing: -0.01em;
    color: #FFFFFF;
  }
  .card-info__cuerpo {
    font-size: 0.98em;
    line-height: 1.55;
    color: #C9CFDA;
    text-align: left;
  }

  /* ── Card comparativa ───────────────────────────── */
  .card-compare { text-align: left; }
  .card-compare__titulo {
    font-weight: 800;
    font-size: 1.1em;
    text-align: center;
    margin-bottom: 24px;
    color: #FFFFFF;
    letter-spacing: -0.01em;
  }
  .card-compare__grid {
    display: grid;
    grid-template-columns: repeat(var(--cols, 2), 1fr);
    gap: 16px;
  }
  .card-compare__col {
    background: var(--surf) padding-box, var(--borde-deg) border-box;
    border: 1.5px solid transparent;
    border-radius: 18px;
    padding: 20px 20px 18px;
    min-width: 0;
    position: relative;
    box-shadow: var(--sombra), var(--sombra-edge);
  }
  .card-compare__col--a { opacity: 0.9; }
  .card-compare__col--win {
    opacity: 1;
    box-shadow: var(--sombra), var(--sombra-edge), var(--glow);
  }
  .card-compare__col--ribbon::after {
    content: "MEJOR";
    position: absolute;
    top: -11px; right: 16px;
    font-family: 'Hasklig', 'JetBrains Mono', 'SFMono-Regular', Menlo, Consolas, monospace;
    font-size: 0.56em;
    font-weight: 800;
    letter-spacing: 2px;
    background: var(--acento);
    color: #0B0B10;
    padding: 4px 11px;
    border-radius: 999px;
    box-shadow: 0 0 20px var(--acento-rgba-40);
  }
  .card-compare__badge {
    display: inline-block;
    font-family: 'Hasklig', 'JetBrains Mono', 'SFMono-Regular', Menlo, Consolas, monospace;
    font-size: 0.62em;
    font-weight: 800;
    letter-spacing: 2px;
    padding: 5px 11px;
    border-radius: 999px;
    background: color-mix(in srgb, var(--acento) 16%, transparent);
    border: 1px solid color-mix(in srgb, var(--acento) 45%, transparent);
    color: var(--acento);
    margin-bottom: 12px;
  }
  .card-compare__col--b .card-compare__badge {
    background: rgba(255, 255, 255, 0.05);
    border-color: var(--linea);
    color: #8B93A1;
  }
  .card-compare__col--win .card-compare__badge {
    background: var(--acento);
    border-color: var(--acento);
    color: #0B0B10;
  }
  .card-compare__nombre {
    font-weight: 800;
    font-size: 1.14em;
    margin-bottom: 12px;
    color: #FFFFFF;
    letter-spacing: -0.01em;
    word-break: break-word;
  }
  .card-compare__item {
    display: flex;
    gap: 11px;
    align-items: flex-start;
    font-size: 0.92em;
    line-height: 1.4;
    color: #C9CFDA;
    padding: 9px 0;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
  }
  .card-compare__item:first-of-type { border-top: 0; padding-top: 2px; }
  .card-compare__mark {
    flex: 0 0 auto;
    font-weight: 800;
    width: 1.45em; height: 1.45em;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.78em;
  }
  .card-compare__mark--ok { color: #0B0B10; background: #34D399; box-shadow: 0 0 16px rgba(52, 211, 153, 0.35); }
  .card-compare__mark--no { color: #F87171; background: rgba(248, 113, 113, 0.18); }
  .card-compare__mark--mid { color: #FBBF24; background: rgba(251, 191, 36, 0.16); border: 1px solid rgba(251, 191, 36, 0.35); }

  /* ── Card repositorio ───────────────────────────── */
  .repo-card {
    background: #000000;
    border: 2px solid #26262B;
    border-radius: 20px;
    overflow: hidden;
    text-align: left;
    box-shadow: 0 14px 34px rgba(0, 0, 0, 0.4);
  }
  .repo-card__bar {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px 22px;
    background: #1F2937;
    border-bottom: 1px solid #26262B;
    font-family: 'Hasklig', 'JetBrains Mono', 'SFMono-Regular', Menlo, Consolas, monospace;
    font-size: 0.86em;
    color: #9CA3AF;
  }
  .repo-card__path b { color: #E5E7EB; font-weight: 700; }
  .repo-card__body { padding: 24px 26px; }
  .repo-card__nombre {
    font-weight: 800;
    font-size: 1.2em;
    color: var(--acento);
    margin-bottom: 8px;
    word-break: break-word;
  }
  .repo-card__desc { font-size: 0.96em; color: #E5E7EB; line-height: 1.45; margin-bottom: 16px; }
  .repo-card__badges { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 16px; }
  .chip {
    font-size: 0.78em;
    font-weight: 700;
    letter-spacing: 1px;
    padding: 7px 13px;
    border-radius: 60px;
    background: #1F2937;
    border: 1px solid #334155;
    color: #CBD5E1;
  }
  .chip--ok { background: rgba(16, 185, 129, 0.16); border-color: #10B981; color: #10B981; }
  .repo-card__tree, .repo-card__install {
    background: #000000;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 16px 18px;
    font-size: 0.88em;
    line-height: 1.6;
    color: #9CA3AF;
    white-space: pre-wrap;
    word-break: break-word;
    overflow: hidden;
  }
  .repo-card__install .prompt { color: #10B981; font-weight: 700; }

  /* ── Diagrama / flujo ───────────────────────────── */
  .diagram { text-align: center; }
  .diagram__titulo {
    font-weight: 700;
    font-size: 1.1em;
    margin-bottom: 4px;
    color: #FFFFFF;
  }
  .diagram__nodo {
    background: #000000;
    border: 2px solid var(--acento);
    border-radius: 16px;
    padding: 11px 20px;
    box-shadow: 0 10px 26px rgba(0, 0, 0, 0.38);
  }
  .diagram__nodo--alerta { border-color: #EF4444; }
  .diagram__nodo--ok { border-color: #10B981; }
  .diagram__nodo--info { border-color: #3B82F6; }
  .diagram__v {
    font-weight: 800;
    font-size: 1.04em;
    color: #FFFFFF;
    word-break: break-word;
  }
  .diagram__sub {
    font-size: 0.86em;
    color: #9CA3AF;
    margin-top: 2px;
    line-height: 1.35;
    word-break: break-word;
  }
  .diagram__flecha {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    color: var(--acento);
    font-weight: 800;
    font-size: 1.1em;
    padding: 0;
    text-shadow: 0 0 14px color-mix(in srgb, var(--acento) 40%, transparent);
  }
  .diagram__flecha .lbl {
    font-size: 0.74em;
    font-weight: 600;
    color: #9CA3AF;
    text-shadow: none;
    letter-spacing: 0.6px;
  }

  /* ── Pasos / infografía ─────────────────────────── */
  .pasos { text-align: left; }
  .pasos__titulo {
    font-weight: 700;
    font-size: 1.1em;
    text-align: center;
    margin-bottom: 24px;
    color: #FFFFFF;
  }
  .paso {
    display: flex;
    gap: 20px;
    align-items: flex-start;
    background: #000000;
    border: 1px solid #26262B;
    border-radius: 16px;
    padding: 18px 22px;
  }
  .paso + .paso { margin-top: 16px; }
  .paso__n {
    flex: 0 0 auto;
    width: 1.55em; height: 1.55em;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    background: var(--acento);
    color: #0B0B0D;
    font-weight: 800;
    font-size: 1.1em;
    box-shadow: 0 0 18px color-mix(in srgb, var(--acento) 34%, transparent);
  }
  .paso__t { font-weight: 700; font-size: 1em; color: #FFFFFF; margin-bottom: 4px; }
  .paso__d { font-size: 0.9em; color: #9CA3AF; line-height: 1.4; }

  /* ── Bloque de código ───────────────────────────── */
  .code {
    background: var(--surf) padding-box, var(--borde-deg) border-box;
    border: 1.5px solid transparent;
    border-radius: 20px;
    overflow: hidden;
    text-align: left;
    box-shadow: var(--sombra), var(--sombra-edge);
  }
  .code__head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 20px;
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.05), transparent);
    border-bottom: 1px solid var(--linea);
    font-family: 'Hasklig', 'JetBrains Mono', 'SFMono-Regular', Menlo, Consolas, monospace;
    font-size: 0.72em;
    letter-spacing: 2px;
    color: #8B93A1;
    text-transform: uppercase;
    font-weight: 700;
  }
  .code__head span:first-child {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    color: var(--acento);
  }
  .code__head span:first-child::before {
    content: "";
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--acento);
    box-shadow: 0 0 10px var(--acento);
  }
  .code__head span:last-child {
    font-size: 0.9em;
    letter-spacing: 1.2px;
    color: #6B7280;
    border: 1px solid var(--linea);
    border-radius: 999px;
    padding: 3px 11px;
  }
  .code__body { padding: 18px 0; background: var(--surf-2); }
  .code__line {
    display: flex;
    gap: 18px;
    padding: 3px 22px;
    font-family: 'Hasklig', 'JetBrains Mono', 'SFMono-Regular', Menlo, Consolas, monospace;
    font-size: 0.86em;
    line-height: 1.55;
    white-space: pre-wrap;
    word-break: break-word;
  }
  .code__ln {
    flex: 0 0 auto;
    color: #3F4654;
    user-select: none;
    text-align: right;
    min-width: 22px;
    font-weight: 700;
  }
  .code__src { color: #E2E8F0; }
  .code__note {
    padding: 14px 22px;
    font-size: 0.84em;
    color: #8B93A1;
    border-top: 1px solid var(--linea);
    background: rgba(255, 255, 255, 0.02);
    line-height: 1.45;
  }
  .tok-kw { color: #C084FC; }
  .tok-str { color: #86EFAC; }
  .tok-num { color: #FCD34D; }
  .tok-com { color: #64748B; font-style: italic; }
  .tok-fn { color: #7DD3FC; }

  /* ── Checklist ──────────────────────────────────── */
  .checklist { text-align: left; }
  .checklist__titulo {
    font-weight: 700;
    font-size: 1.1em;
    text-align: center;
    margin-bottom: 22px;
    color: #FFFFFF;
  }
  .checklist__item {
    display: flex;
    gap: 16px;
    align-items: flex-start;
    background: #000000;
    border: 1px solid #26262B;
    border-radius: 14px;
    padding: 16px 20px;
    font-size: 0.96em;
    line-height: 1.42;
    color: #E5E7EB;
  }
  .checklist__item + .checklist__item { margin-top: 14px; }
  .checklist__ico {
    flex: 0 0 auto;
    color: #10B981;
    font-weight: 800;
    font-size: 1.1em;
  }

  /* ── Mitos vs realidad ──────────────────────────── */
  .mitos { display: flex; flex-direction: column; gap: 20px; text-align: left; }
  .mitos__bloque {
    border-radius: 18px;
    padding: 24px 26px;
    border: 2px solid;
  }
  .mitos__bloque--mito { border-color: #EF4444; background: #000000; }
  .mitos__bloque--real { border-color: #10B981; background: #000000; }
  .mitos__label {
    font-size: 0.8em;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 10px;
  }
  .mitos__bloque--mito .mitos__label { color: #EF4444; }
  .mitos__bloque--real .mitos__label { color: #10B981; }
  .mitos__texto { font-size: 1em; line-height: 1.45; color: #FFFFFF; font-weight: 600; }
  .mitos__sub { font-size: 0.88em; color: #9CA3AF; margin-top: 8px; font-weight: 400; line-height: 1.4; }

  /* ── Social / valor ─────────────────────────────── */
  .social {
    background: linear-gradient(160deg, #000000, #000000);
    border: 2px solid color-mix(in srgb, var(--acento) 50%, #26262B);
    border-radius: 20px;
    padding: 30px 30px;
    text-align: center;
    box-shadow: 0 16px 38px rgba(0, 0, 0, 0.45);
  }
  .social__kicker {
    display: inline-block;
    font-size: 0.8em;
    font-weight: 800;
    letter-spacing: 2.4px;
    color: var(--acento);
    margin-bottom: 14px;
  }
  .social__titulo { font-weight: 800; font-size: 1.22em; color: #FFFFFF; line-height: 1.2; margin-bottom: 12px; }
  .social__texto { font-size: 0.96em; color: #E5E7EB; line-height: 1.5; margin-bottom: 20px; }
  .social__cta {
    display: inline-block;
    padding: 16px 32px;
    border-radius: 60px;
    background: var(--resalte);
    color: #0F0F10;
    font-weight: 800;
    font-size: 0.98em;
    box-shadow: 0 0 30px color-mix(in srgb, var(--resalte) 34%, transparent);
  }

  .comp-wrap {
    margin-top: __comp_margin__px;
    zoom: __comp_zoom__;
    font-size: __comp_base__px;
  }


  /* ── Árbol de directorios ───────────────────────── */
  .tree-dir { background: #000000; border: 2px solid #26262B; border-radius: 16px; padding: 18px 22px; text-align: left; }
  .tree-dir__titulo { font-weight: 700; font-size: 1.06em; margin-bottom: 12px; color: #FFFFFF; }
  .tree-dir__ul { list-style: none; padding-left: 0; margin: 0; }
  .tree-dir__li { display: flex; align-items: center; gap: 10px; color: #E5E7EB; font-size: 0.94em; line-height: 1.7; font-family: 'Hasklig', 'JetBrains Mono', 'SFMono-Regular', Menlo, Consolas, monospace; }
  .tree-dir__ico { display: inline-flex; flex: 0 0 auto; }
  .tree-dir__ico svg { width: 1.05em; height: 1.05em; display: block; }
  .tree-dir__li .prompt { color: #10B981; font-weight: 700; }

  /* ── API Block ─────────────────────────────────── */
  .api-block { background: #000000; border: 2px solid #26262B; border-radius: 16px; overflow: hidden; text-align: left; }
  .api-block__head { display: flex; align-items: center; gap: 12px; padding: 12px 18px; background: #000000; border-bottom: 1px solid #26262B; }
  .api-block__metodo { font-weight: 800; font-size: 0.82em; padding: 6px 10px; border-radius: 8px; background: #10B981; color: #000000; letter-spacing: 1px; }
  .api-block__metodo--post { background: #3B82F6; color: #FFFFFF; }
  .api-block__metodo--put { background: #F59E0B; color: #000000; }
  .api-block__metodo--del, .api-block__metodo--delete { background: #EF4444; color: #FFFFFF; }
  .api-block__url { font-family: 'Hasklig', 'JetBrains Mono', monospace; font-size: 0.86em; color: #E5E7EB; word-break: break-all; }
  .api-block__status { margin-left: auto; font-weight: 800; font-size: 0.8em; color: #10B981; }
  .api-block__body { padding: 14px 18px; font-family: 'Hasklig', 'JetBrains Mono', monospace; font-size: 0.84em; color: #9CA3AF; white-space: pre-wrap; }

  /* ── Browser ───────────────────────────────────── */
  .browser { background: #000000; border: 2px solid #26262B; border-radius: 16px; overflow: hidden; text-align: left; }
  .browser__bar { display: flex; align-items: center; gap: 10px; padding: 10px 14px; background: #000000; border-bottom: 1px solid #26262B; }
  .browser__dot { width: 10px; height: 10px; border-radius: 50%; background: #475569; }
  .browser__dot--r { background: #EF4444; }
  .browser__dot--y { background: #F59E0B; }
  .browser__dot--g { background: #10B981; }
  .browser__url { flex: 1; margin-left: 6px; font-size: 0.78em; color: #9CA3AF; background: #000000; border: 1px solid #26262B; border-radius: 8px; padding: 6px 10px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .browser__view { padding: 14px 16px; color: #E5E7EB; font-size: 0.9em; line-height: 1.5; white-space: pre-wrap; }

  /* ── Layers ────────────────────────────────────── */
  .layers { text-align: center; display: flex; flex-direction: column; gap: 10px; align-items: center; }
  .layers__titulo { font-weight: 700; font-size: 1.06em; color: #FFFFFF; }
  .layer { background: #000000; border: 2px solid var(--acento); border-radius: 12px; padding: 10px 18px; min-width: 70%; }
  .layer--front { border-color: #3B82F6; }
  .layer--back { border-color: #F59E0B; }
  .layer--db { border-color: #10B981; }
  .layer--api { border-color: var(--acento); }
  .layer__n { font-weight: 700; color: #FFFFFF; }
  .layer__s { font-size: 0.8em; color: #9CA3AF; }
  .layers__arr { color: var(--acento); font-weight: 800; }

  /* ── CI Pipeline ───────────────────────────────── */
  .pipeline { text-align: center; }
  .pipeline__titulo { font-weight: 700; font-size: 1.06em; color: #FFFFFF; margin-bottom: 16px; }
  .pipeline__row { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }
  .stage { background: #000000; border: 2px solid #26262B; border-radius: 12px; padding: 10px 16px; min-width: 120px; }
  .stage--ok { border-color: #10B981; }
  .stage--warn { border-color: #F59E0B; }
  .stage--err { border-color: #EF4444; }
  .stage--idle { border-color: #475569; }
  .stage__n { font-weight: 700; color: #FFFFFF; font-size: 0.92em; }
  .stage__st { font-size: 0.78em; color: #9CA3AF; }

  /* ── Stats ─────────────────────────────────────── */
  .stats { text-align: center; }
  .stats__titulo {
    font-family: 'Hasklig', 'JetBrains Mono', 'SFMono-Regular', Menlo, Consolas, monospace;
    font-weight: 700;
    font-size: 0.72em;
    letter-spacing: 2.4px;
    text-transform: uppercase;
    color: #8B93A1;
    margin-bottom: 18px;
  }
  .stats__grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 14px; }
  .stat {
    background: var(--surf) padding-box, var(--borde-deg) border-box;
    border: 1.5px solid transparent;
    border-radius: 18px;
    padding: 24px 14px 20px;
    position: relative;
    overflow: hidden;
    box-shadow: var(--sombra), var(--sombra-edge);
  }
  .stat::before {
    content: "";
    position: absolute;
    left: 0; right: 0; top: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, var(--acento), transparent);
  }
  .stat__val {
    font-weight: 900;
    font-size: 2.3em;
    line-height: 1;
    letter-spacing: -0.02em;
    background: linear-gradient(160deg, #FFFFFF 8%, var(--acento-brillo) 52%, var(--acento));
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 0 20px var(--acento-rgba-30));
  }
  .stat__lbl {
    font-size: 0.8em;
    color: #8B93A1;
    margin-top: 11px;
    line-height: 1.35;
    font-weight: 500;
  }

  /* ── Quote ─────────────────────────────────────── */
  .quote { background: #000000; border-left: 4px solid var(--acento); border: 2px solid #26262B; border-radius: 14px; padding: 18px 22px; text-align: left; }
  .quote__text { font-size: 1em; color: #E5E7EB; line-height: 1.6; font-style: italic; }
  .quote__autor { margin-top: 10px; font-weight: 700; color: #FFFFFF; }
  .quote__rol { font-size: 0.86em; color: #9CA3AF; }

  /* ── Comparison Table ───────────────────────────── */
  .ctable { background: #000000; border: 2px solid #26262B; border-radius: 16px; overflow: hidden; text-align: left; }
  .ctable__titulo { font-weight: 700; font-size: 1.06em; color: #FFFFFF; padding: 12px 16px; border-bottom: 1px solid #26262B; }
  .ctable__tbl { width: 100%; border-collapse: collapse; font-size: 0.9em; }
  .ctable__tbl th { background: #000000; color: #9CA3AF; text-align: left; padding: 10px 14px; border-bottom: 1px solid #26262B; font-weight: 700; }
  .ctable__tbl td { color: #E5E7EB; padding: 10px 14px; border-bottom: 1px solid #1F2937; }
  .ctable__tbl tr:last-child td { border-bottom: 0; }

  /* ── FAQ ────────────────────────────────────────── */
  .faq { background: #000000; border: 2px solid #26262B; border-radius: 16px; padding: 16px 18px; text-align: left; }
  .faq__titulo { font-weight: 700; font-size: 1.06em; color: #FFFFFF; margin-bottom: 10px; }
  .faq__item { border-top: 1px solid #1F2937; padding: 12px 0; }
  .faq__item:first-of-type { border-top: 0; }
  .faq__q { font-weight: 700; color: #FFFFFF; margin-bottom: 4px; }
  .faq__a { font-size: 0.9em; color: #9CA3AF; line-height: 1.45; }
  .faq__badge, .quiz__badge { display: inline-flex; align-items: center; justify-content: center; width: 1.5em; height: 1.5em; border-radius: 50%; border: 2px solid var(--acento); color: var(--acento); font-weight: 800; font-size: 0.85em; margin-right: 8px; vertical-align: baseline; }

  /* ── Diff antes/después ─────────────────────────── */
  .diff { background: #000000; border: 2px solid #26262B; border-radius: 16px; overflow: hidden; text-align: left; }
  .diff__titulo { font-weight: 700; font-size: 1.06em; color: #FFFFFF; padding: 12px 16px; border-bottom: 1px solid #26262B; }
  .diff__cols { display: grid; grid-template-columns: 1fr 1fr; gap: 0; }
  .diff__col { padding: 12px 14px; font-family: 'Hasklig', 'JetBrains Mono', 'SFMono-Regular', Menlo, Consolas, monospace; font-size: 0.82em; line-height: 1.55; }
  .diff__col--antes { background: rgba(239,68,68,0.07); border-right: 1px solid #26262B; }
  .diff__col--despues { background: rgba(16,185,129,0.07); }
  .diff__lbl { font-weight: 800; font-size: 0.86em; letter-spacing: 1px; margin-bottom: 8px; color: #9CA3AF; }
  .diff__line { white-space: pre-wrap; word-break: break-word; color: #E5E7EB; }
  .diff__line--del { color: #FCA5A5; }
  .diff__line--add { color: #6EE7B7; }
  .diff__mk { font-weight: 800; margin-right: 6px; }

  /* ── Quiz ───────────────────────────────────────── */
  .quiz { background: #000000; border: 2px solid var(--acento); border-radius: 16px; padding: 18px 20px; text-align: left; }  .quiz__q { font-weight: 800; font-size: 1.02em; color: #FFFFFF; margin-bottom: 14px; line-height: 1.4; }
  .quiz__op { display: flex; gap: 10px; align-items: baseline; background: #000000; border: 1px solid #26262B; border-radius: 12px; padding: 10px 14px; margin-bottom: 8px; color: #E5E7EB; font-size: 0.92em; }
  .quiz__op--ok { border-color: #10B981; }
  .quiz__mk { font-weight: 800; color: var(--acento); }
  .quiz__op--ok .quiz__mk { color: #10B981; }
  .quiz__pie { margin-top: 10px; font-size: 0.84em; color: #9CA3AF; }

  /* ── Editor de código (mock IDE) ────────────────── */
  .editor {
    background: var(--surf) padding-box, var(--borde-deg) border-box;
    border: 1.5px solid transparent;
    border-radius: 20px;
    overflow: hidden;
    text-align: left;
    box-shadow: var(--sombra), var(--sombra-edge);
  }
  .editor__bar {
    display: flex;
    align-items: flex-end;
    gap: 10px;
    padding: 12px 18px 0;
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.05), transparent);
    border-bottom: 1px solid var(--linea);
  }
  .editor__dot { width: 13px; height: 13px; border-radius: 50%; margin-bottom: 14px; box-shadow: 0 0 10px currentColor; }
  .editor__dot--r { background: #EF4444; color: #EF4444; }
  .editor__dot--y { background: #F59E0B; color: #F59E0B; }
  .editor__dot--g { background: #10B981; color: #10B981; }
  .editor__tab {
    margin-left: 8px;
    font-family: 'Hasklig', 'JetBrains Mono', 'SFMono-Regular', Menlo, Consolas, monospace;
    font-size: 0.82em;
    font-weight: 600;
    color: #F8FAFC;
    background: var(--s1);
    border: 1px solid var(--linea);
    border-bottom: 0;
    padding: 9px 16px;
    border-radius: 10px 10px 0 0;
    margin-bottom: -1px;
  }
  .editor__lang {
    margin-left: auto;
    margin-bottom: 10px;
    font-weight: 800;
    font-size: 0.66em;
    color: #0B0B10;
    background: var(--acento);
    padding: 5px 12px;
    border-radius: 999px;
    box-shadow: 0 0 20px -4px var(--acento-rgba-40);
  }
  .editor__body { padding: 18px 0; counter-reset: ln; background: var(--surf-2); }
  .editor__line { display: flex; font-family: 'Hasklig', 'JetBrains Mono', 'SFMono-Regular', Menlo, Consolas, monospace; font-size: 0.9em; line-height: 1.6; white-space: pre-wrap; word-break: break-word; }
  .editor__ln { flex: 0 0 52px; text-align: right; padding-right: 16px; color: #3F4654; user-select: none; font-weight: 700; }
  .editor__src { color: #E5E7EB; padding-right: 18px; }
  .editor .tok-kw { color: #C792EA; font-weight: 700; }
  .editor .tok-str { color: #C3E88D; }
  .editor .tok-num { color: #F78C6C; }
  .editor .tok-fn { color: #82AAFF; }
  .editor .tok-com { color: #64748B; font-style: italic; }
  .editor__out { border-top: 1px solid var(--linea); background: rgba(0, 0, 0, 0.35); }
  .editor__outbar { padding: 10px 20px; font-family: 'Hasklig', 'JetBrains Mono', 'SFMono-Regular', Menlo, Consolas, monospace; font-size: 0.72em; color: #8B93A1; border-bottom: 1px solid var(--linea); letter-spacing: 1.2px; text-transform: uppercase; }
  .editor__outbar .prompt { color: var(--acento); font-weight: 800; }
  .editor__outline { padding: 4px 20px; font-family: 'Hasklig', 'JetBrains Mono', 'SFMono-Regular', Menlo, Consolas, monospace; font-size: 0.84em; color: #8B93A1; white-space: pre-wrap; }
  .editor__outline:first-of-type { padding-top: 12px; }
  .editor__outline:last-child { padding-bottom: 12px; }
  .editor__status {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 11px 20px;
    background: linear-gradient(90deg, var(--acento), var(--acento-brillo));
    color: #0B0B10;
    font-family: 'Hasklig', 'JetBrains Mono', 'SFMono-Regular', Menlo, Consolas, monospace;
    font-size: 0.74em;
    font-weight: 800;
    letter-spacing: 0.4px;
  }

  /* ── GitHub stats ───────────────────────────────── */
  .ghstats { background: #000000; border: 2px solid #26262B; border-radius: 16px; padding: 18px 22px; text-align: left; }
  .ghstats__repo { font-weight: 800; font-size: 1.04em; color: #FFFFFF; margin-bottom: 6px; }
  .ghstats__lic { font-size: 0.72em; font-weight: 800; color: #0F0F10; background: #9CA3AF; padding: 4px 10px; border-radius: 8px; margin-left: 8px; vertical-align: middle; }
  .ghstats__desc { font-size: 0.9em; color: #9CA3AF; line-height: 1.45; margin-bottom: 12px; }
  .ghstats__nums { display: flex; gap: 18px; font-size: 0.9em; font-weight: 700; color: #E5E7EB; margin-bottom: 12px; }
  .ghstats__bar { display: flex; height: 12px; border-radius: 6px; overflow: hidden; background: #1F2937; margin-bottom: 10px; }
  .ghstats__seg { display: block; height: 100%; }
  .ghstats__langs { display: flex; gap: 14px; flex-wrap: wrap; font-size: 0.82em; color: #9CA3AF; }
  .ghstats__dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 6px; }

  /* ── QR (escaneable desde pantalla) ────────────── */
  .qr { background: #000000; border: 2px solid #26262B; border-radius: 18px; padding: 18px 22px; text-align: center; }
  .qr__titulo { font-weight: 800; font-size: 1.02em; color: #FFFFFF; margin-bottom: 12px; }
  .qr__caja { display: inline-block; background: #FFFFFF; padding: 16px 16px 12px; border-radius: 16px; }
  .qr__caja svg { width: 320px; height: 320px; display: block; }
  .qr__escanea { margin-top: 8px; font-weight: 800; font-size: .8em; letter-spacing: 3px; color: #0F0F10; text-transform: uppercase; }
  .qr__pie { margin-top: 12px; font-size: .88em; color: #9CA3AF; }
  .qr__vacio { padding: 26px; color: #9CA3AF; font-size: .9em; word-break: break-all; }
  .qr--vacio { padding: 26px; color: #EF4444; }

  /* ── Stack (tecnologías) ───────────────────────── */
  .stack { background: #000000; border: 2px solid #26262B; border-radius: 18px; padding: 18px 22px; }
  .stack__titulo { font-weight: 800; font-size: 1.02em; color: #FFFFFF; margin-bottom: 14px; }
  .stack__fila { display: flex; flex-wrap: wrap; gap: 12px; }
  .stack__chip { display: inline-flex; align-items: center; gap: 9px; background: #141417; border: 1px solid #2C2C33; border-radius: 999px; padding: 9px 16px; font-size: .92em; color: #F3F4F6; }
  .stack__chip b { font-weight: 700; }
  .stack__sub { color: #9CA3AF; font-size: .86em; }
  .stack__dot { width: 12px; height: 12px; border-radius: 50%; flex: 0 0 auto; }
  .stack__pie { margin-top: 14px; font-size: .86em; color: #9CA3AF; }

  /* ── Error (consola con traceback) ─────────────── */
  .err { background: #0B0B0D; border: 2px solid #26262B; border-radius: 16px; overflow: hidden; text-align: left; }
  .err__bar { display: flex; align-items: center; gap: 8px; background: #16161A; padding: 10px 14px; border-bottom: 1px solid #26262B; }
  .err__dot { width: 12px; height: 12px; border-radius: 50%; display: inline-block; }
  .err__dot--r { background: #FF5F57; } .err__dot--y { background: #FEBC2E; } .err__dot--g { background: #28C840; }
  .err__file { margin-left: 10px; font-size: .82em; color: #9CA3AF; font-family: 'Hasklig', 'JetBrains Mono', 'SFMono-Regular', Menlo, Consolas, monospace; }
  .err__titulo { padding: 12px 16px 0; font-weight: 800; font-size: .96em; color: #FFFFFF; }
  .err__body { padding: 12px 16px; font-family: 'Hasklig', 'JetBrains Mono', 'SFMono-Regular', Menlo, Consolas, monospace; font-size: .8em; line-height: 1.5; }
  .err__line { white-space: pre-wrap; word-break: break-word; }
  .err__line--err-head { color: #F87171; font-weight: 700; }
  .err__line--err { color: #F87171; font-weight: 700; }
  .err__line--err-ctx { color: #FBBF24; }
  .err__line--err-out { color: #D1D5DB; }
  .err__resumen { margin: 0 16px 12px; padding: 10px 14px; background: rgba(255,255,255,.06); border-left: 4px solid var(--acento); border-radius: 8px; font-size: .86em; color: #F3F4F6; }
  .err__pie { padding: 0 16px 14px; font-size: .8em; color: #9CA3AF; }

  /* ── Timeline (ruta de aprendizaje) ────────────── */
  .tl { background: #000000; border: 2px solid #26262B; border-radius: 18px; padding: 18px 22px; text-align: left; }
  .tl__titulo { font-weight: 800; font-size: 1.02em; color: #FFFFFF; margin-bottom: 14px; }
  .tl__item { display: flex; align-items: flex-start; gap: 14px; padding: 9px 0; border-bottom: 1px solid #1C1C21; }
  .tl__item:last-of-type { border-bottom: 0; }
  .tl__mark { flex: 0 0 auto; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: .9em; border: 2px solid #2C2C33; color: #9CA3AF; }
  .tl__mark--ok { border-color: var(--acento); color: var(--acento); }
  .tl__mark--run { border-color: #FBBF24; color: #FBBF24; }
  .tl__mark--error { border-color: #F87171; color: #F87171; }
  .tl__txt { display: flex; flex-direction: column; gap: 3px; padding-top: 2px; }
  .tl__txt b { font-size: .96em; color: #F3F4F6; }
  .tl__sub { font-size: .85em; color: #9CA3AF; }
  .tl__pie { margin-top: 12px; font-size: .86em; color: #9CA3AF; }

  /* ── Índice del post ───────────────────────────── */
  .idx { background: #000000; border: 2px solid #26262B; border-radius: 18px; padding: 18px 22px; text-align: left; }
  .idx__titulo { font-weight: 800; font-size: 1.02em; color: #FFFFFF; margin-bottom: 12px; }
  .idx__item { display: flex; align-items: center; gap: 14px; padding: 8px 0; }
  .idx__n { flex: 0 0 auto; width: 34px; height: 34px; border-radius: 10px; background: rgba(255,255,255,.08); color: var(--acento); font-weight: 800; display: flex; align-items: center; justify-content: center; }
  .idx__v { font-size: .98em; color: #F3F4F6; font-weight: 600; }
  .idx__pie { margin-top: 12px; font-size: .86em; color: #9CA3AF; }

  /* ══════════════════════════════════════════════════════════════
     ELEVATION · sistema de superficies (Wave 0)
     Va al final del CSS: gana por orden sobre el molde viejo.
     Ningún componente vuelve a ser #000000 puro.
     ══════════════════════════════════════════════════════════════ */

  /* 1 · Superficie elevada */
  .terminal, .code, .editor, .card-info, .repo-card, .api-block, .browser,
  .ctable, .faq, .diff, .ghstats, .qr, .stack, .err, .tl, .idx, .tree-dir,
  .stat, .paso, .card-compare__col, .social, .quote, .mitos__bloque,
  .diagram__nodo, .tl__item {
    background: var(--surf);
    box-shadow: var(--sombra), var(--sombra-edge);
  }

  /* 2 · Borde de luz: el acento cae desde arriba-izquierda */
  .terminal, .code, .editor, .card-info, .repo-card, .api-block, .browser,
  .ctable, .faq, .diff, .ghstats, .stack, .err, .tl, .idx, .tree-dir,
  .stat, .paso, .card-compare__col, .social, .quiz,
  .diagram__nodo, .tl__item {
    border: 1.5px solid transparent;
    background: var(--surf) padding-box, var(--borde-deg) border-box;
    box-shadow: var(--sombra), var(--sombra-edge);
  }

  /* 3 · Paneles anidados: un escalón más oscuro */
  .terminal__body, .code__body, .api-block__body,
  .repo-card__tree, .repo-card__install, .editor__out {
    background: var(--surf-2);
  }

  /* 4 · Rótulos (eyebrow): mono, tracking ancho, versalitas */
  .terminal__titulo, .code__head, .editor__lang {
    letter-spacing: 1.6px;
    text-transform: uppercase;
  }

  /* ══════════════════════════════════════════════════════════════
     WAVE 2 · los 22 componentes restantes
     Mismo contrato y mismo layout: sólo superficie, jerarquía y color.
     ══════════════════════════════════════════════════════════════ */

  /* ── Checklist ──────────────────────────────────── */
  .checklist {
    background: var(--surf) padding-box, var(--borde-deg) border-box;
    border: 1.5px solid transparent;
    border-radius: var(--radio-md);
    padding: 22px 24px;
    text-align: left;
    box-shadow: var(--sombra), var(--sombra-edge);
  }
  .checklist__titulo {
    font-family: var(--mono);
    font-size: 0.72em;
    font-weight: 700;
    letter-spacing: 2.2px;
    text-transform: uppercase;
    color: #8B93A1;
    margin-bottom: 14px;
  }
  .checklist__item {
    display: flex;
    gap: 12px;
    align-items: flex-start;
    font-size: 0.96em;
    line-height: 1.45;
    color: #E4E8EF;
    padding: 9px 0;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
  }
  .checklist__item:first-of-type { border-top: 0; padding-top: 0; }
  .checklist__ico {
    flex: 0 0 auto;
    width: 1.55em; height: 1.55em;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    background: #34D399;
    color: #0B0B10;
    font-weight: 800;
    font-size: 0.76em;
    box-shadow: 0 0 16px rgba(52, 211, 153, 0.35);
  }

  /* ── Pasos / infografía ─────────────────────────── */
  .pasos { text-align: left; }
  .pasos__titulo {
    font-family: var(--mono);
    font-size: 0.72em;
    font-weight: 700;
    letter-spacing: 2.2px;
    text-transform: uppercase;
    text-align: center;
    margin-bottom: 22px;
    color: #8B93A1;
  }
  .paso {
    position: relative;
    border-radius: var(--radio-md);
  }
  .paso__n {
    width: 1.7em; height: 1.7em;
    border-radius: 0.5em;
    background: linear-gradient(160deg, var(--acento-brillo), var(--acento));
    box-shadow: 0 0 22px -6px var(--acento-rgba-40);
    font-weight: 900;
  }
  .paso__t { font-weight: 800; font-size: 1.05em; letter-spacing: -0.01em; }
  .paso__d { font-size: 0.9em; color: #9AA2B1; line-height: 1.45; }
  .paso:not(:last-of-type)::after {
    content: "";
    position: absolute;
    left: calc(22px + 0.85em);
    top: calc(100% + 2px);
    height: 12px;
    width: 2px;
    background: linear-gradient(180deg, var(--acento-rgba-40), transparent);
  }

  /* ── Diagrama / flujo ───────────────────────────── */
  .diagram { text-align: center; counter-reset: nodo; }
  .diagram__titulo {
    font-family: var(--mono);
    font-size: 0.72em;
    font-weight: 700;
    letter-spacing: 2.2px;
    text-transform: uppercase;
    margin-bottom: 8px;
    color: #8B93A1;
  }
  .diagram__nodo {
    position: relative;
    border: 1.5px solid transparent;
    background: var(--surf) padding-box, var(--borde-deg) border-box;
    border-radius: var(--radio-md);
    padding: 13px 22px;
    box-shadow: var(--sombra), var(--sombra-edge);
  }
  .diagram__nodo::before {
    counter-increment: nodo;
    content: counter(nodo);
    position: absolute;
    left: 14px; top: -11px;
    width: 22px; height: 22px;
    border-radius: 50%;
    background: var(--acento);
    color: #0B0B10;
    font-family: var(--mono);
    font-size: 0.6em;
    font-weight: 900;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 0 14px var(--acento-rgba-40);
  }
  .diagram__nodo--alerta {
    --borde-deg: linear-gradient(145deg, rgba(248, 113, 113, 0.9),
      rgba(248, 113, 113, 0.14) 50%, #24242E);
  }
  .diagram__nodo--ok {
    --borde-deg: linear-gradient(145deg, rgba(52, 211, 153, 0.9),
      rgba(52, 211, 153, 0.14) 50%, #24242E);
  }
  .diagram__nodo--info {
    --borde-deg: linear-gradient(145deg, rgba(96, 165, 250, 0.9),
      rgba(96, 165, 250, 0.14) 50%, #24242E);
  }
  .diagram__v { font-weight: 800; font-size: 1.06em; color: #FFFFFF; }
  .diagram__sub { font-size: 0.84em; color: #8B93A1; margin-top: 3px; line-height: 1.35; }
  .diagram__flecha {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    height: 36px;
    position: relative;
    text-shadow: none;
  }
  .diagram__conector {
    position: relative;
    width: 2px;
    height: 24px;
    background: linear-gradient(180deg,
      color-mix(in srgb, var(--acento) 25%, transparent), var(--acento));
  }
  .diagram__conector::after {
    content: "";
    position: absolute;
    left: 50%; bottom: -6px;
    transform: translateX(-50%);
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 7px solid var(--acento);
  }
  .diagram__flecha .lbl {
    font-family: var(--mono);
    font-size: 0.7em;
    font-weight: 600;
    color: #8B93A1;
    letter-spacing: 0.6px;
    text-shadow: none;
  }

  /* ── Árbol de directorios ───────────────────────── */
  .tree-dir {
    border-radius: var(--radio-md);
    padding: 20px 22px;
  }
  .tree-dir__titulo {
    font-family: var(--mono);
    font-size: 0.72em;
    font-weight: 700;
    letter-spacing: 2.2px;
    text-transform: uppercase;
    margin-bottom: 14px;
    color: #8B93A1;
  }
  .tree-dir__li { color: #D5DAE3; font-size: 0.92em; line-height: 1.75; }
  .tree-dir__li .prompt { color: var(--acento); font-weight: 800; }

  /* ── API Block ─────────────────────────────────── */
  .api-block { border-radius: var(--radio-md); }
  .api-block__head {
    gap: 12px;
    padding: 14px 18px;
    background: rgba(255, 255, 255, 0.03);
    border-bottom: 1px solid var(--linea);
  }
  .api-block__metodo {
    font-family: var(--mono);
    font-weight: 800;
    font-size: 0.72em;
    letter-spacing: 1.4px;
    padding: 6px 12px;
    border-radius: 999px;
    background: #34D399;
    color: #0B0B10;
    box-shadow: 0 0 18px -4px rgba(52, 211, 153, 0.55);
  }
  .api-block__metodo--post { background: #60A5FA; color: #0B0B10; box-shadow: 0 0 18px -4px rgba(96, 165, 250, 0.55); }
  .api-block__metodo--put { background: #FBBF24; color: #0B0B10; box-shadow: 0 0 18px -4px rgba(251, 191, 36, 0.55); }
  .api-block__metodo--del, .api-block__metodo--delete { background: #F87171; color: #0B0B10; box-shadow: 0 0 18px -4px rgba(248, 113, 113, 0.55); }
  .api-block__url { font-family: var(--mono); font-size: 0.82em; color: #E4E8EF; }
  .api-block__status {
    margin-left: auto;
    font-family: var(--mono);
    font-weight: 800;
    font-size: 0.72em;
    color: #34D399;
    background: rgba(52, 211, 153, 0.12);
    border: 1px solid rgba(52, 211, 153, 0.35);
    padding: 4px 10px;
    border-radius: 999px;
  }
  .api-block__body {
    padding: 14px 18px;
    font-family: var(--mono);
    font-size: 0.8em;
    color: #9AA2B1;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
  }
  .api-block__body b { color: var(--acento); font-weight: 700; }

  /* ── Browser ───────────────────────────────────── */
  .browser { border-radius: var(--radio-md); }
  .browser__bar {
    gap: 10px;
    padding: 12px 14px;
    background: rgba(255, 255, 255, 0.04);
    border-bottom: 1px solid var(--linea);
  }
  .browser__url {
    font-family: var(--mono);
    font-size: 0.72em;
    color: #9AA2B1;
    background: var(--s3);
    border: 1px solid var(--linea);
    border-radius: 999px;
    padding: 6px 12px;
  }
  .browser__view {
    padding: 16px 18px;
    color: #E4E8EF;
    font-size: 0.88em;
    line-height: 1.55;
    white-space: pre-wrap;
  }
  .browser__view b { display: block; color: #FFFFFF; margin-bottom: 6px; }

  /* ── Diff antes/después ─────────────────────────── */
  .diff { border-radius: var(--radio-md); }
  .diff__titulo {
    font-family: var(--mono);
    font-size: 0.72em;
    font-weight: 700;
    letter-spacing: 2.2px;
    text-transform: uppercase;
    color: #8B93A1;
    padding: 14px 18px;
    border-bottom: 1px solid var(--linea);
  }
  .diff__col { padding: 14px 16px; font-family: var(--mono); font-size: 0.78em; line-height: 1.6; }
  .diff__col--antes { background: rgba(248, 113, 113, 0.07); border-right: 1px solid var(--linea); }
  .diff__col--despues { background: rgba(52, 211, 153, 0.07); }
  .diff__lbl { font-family: var(--mono); font-weight: 800; font-size: 0.8em; letter-spacing: 1.6px; margin-bottom: 10px; }
  .diff__col--antes .diff__lbl { color: #F87171; }
  .diff__col--despues .diff__lbl { color: #34D399; }
  .diff__line { color: #D5DAE3; }
  .diff__line--del { color: #FCA5A5; }
  .diff__line--add { color: #6EE7B7; }
  .diff__mk { font-weight: 800; margin-right: 8px; opacity: 0.85; }

  /* ── Comparison Table ───────────────────────────── */
  .ctable { border-radius: var(--radio-md); }
  .ctable__titulo {
    font-family: var(--mono);
    font-size: 0.72em;
    font-weight: 700;
    letter-spacing: 2.2px;
    text-transform: uppercase;
    color: #8B93A1;
    padding: 14px 18px;
    border-bottom: 1px solid var(--linea);
  }
  .ctable__tbl { font-size: 0.86em; }
  .ctable__tbl th {
    background: var(--s3);
    color: #C9CFDA;
    padding: 11px 16px;
    border-bottom: 1px solid var(--linea);
    font-weight: 700;
    font-size: 0.92em;
  }
  .ctable__tbl td { color: #E4E8EF; padding: 11px 16px; border-bottom: 1px solid rgba(255, 255, 255, 0.05); }
  .ctable__tbl td:first-child { color: var(--acento); font-weight: 700; }
  .ctable__tbl tr:last-child td { border-bottom: 0; }

  /* ── Layers ────────────────────────────────────── */
  .layers__titulo {
    font-family: var(--mono);
    font-size: 0.72em;
    font-weight: 700;
    letter-spacing: 2.2px;
    text-transform: uppercase;
    color: #8B93A1;
    margin-bottom: 6px;
  }
  .layer {
    border: 1.5px solid transparent;
    background: var(--surf) padding-box, var(--borde-deg) border-box;
    border-radius: var(--radio-sm);
    padding: 13px 20px;
    min-width: 76%;
    box-shadow: var(--sombra), var(--sombra-edge);
  }
  .layer__n { font-weight: 800; color: #FFFFFF; font-size: 1.02em; }
  .layer__s { font-size: 0.82em; color: #8B93A1; margin-top: 2px; }
  .layer--front { --borde-deg: linear-gradient(145deg, rgba(96, 165, 250, 0.9), rgba(96, 165, 250, 0.12) 50%, #24242E); }
  .layer--back { --borde-deg: linear-gradient(145deg, rgba(251, 191, 36, 0.9), rgba(251, 191, 36, 0.12) 50%, #24242E); }
  .layer--db { --borde-deg: linear-gradient(145deg, rgba(52, 211, 153, 0.9), rgba(52, 211, 153, 0.12) 50%, #24242E); }
  .layer--api { --borde-deg: linear-gradient(145deg, color-mix(in srgb, var(--acento) 90%, transparent), color-mix(in srgb, var(--acento) 14%, #24242E) 50%, #24242E); }
  .layers__arr { color: var(--acento); font-weight: 800; font-size: 0.8em; opacity: 0.8; }

  /* ── CI Pipeline ───────────────────────────────── */
  .pipeline__titulo {
    font-family: var(--mono);
    font-size: 0.72em;
    font-weight: 700;
    letter-spacing: 2.2px;
    text-transform: uppercase;
    color: #8B93A1;
    margin-bottom: 18px;
  }
  .stage {
    position: relative;
    border: 1.5px solid transparent;
    background: var(--surf) padding-box, var(--borde-deg) border-box;
    border-radius: var(--radio-sm);
    padding: 16px 18px 13px;
    min-width: 128px;
    box-shadow: var(--sombra);
  }
  .stage::before {
    content: "";
    position: absolute;
    left: 16px; right: 16px; top: 0;
    height: 3px;
    border-radius: 0 0 3px 3px;
    background: #475569;
  }
  .stage--ok { --borde-deg: linear-gradient(145deg, rgba(52, 211, 153, 0.9), rgba(52, 211, 153, 0.12) 50%, #24242E); }
  .stage--ok::before { background: #34D399; box-shadow: 0 0 14px rgba(52, 211, 153, 0.6); }
  .stage--warn { --borde-deg: linear-gradient(145deg, rgba(251, 191, 36, 0.9), rgba(251, 191, 36, 0.12) 50%, #24242E); }
  .stage--warn::before { background: #FBBF24; box-shadow: 0 0 14px rgba(251, 191, 36, 0.6); }
  .stage--err { --borde-deg: linear-gradient(145deg, rgba(248, 113, 113, 0.9), rgba(248, 113, 113, 0.12) 50%, #24242E); }
  .stage--err::before { background: #F87171; box-shadow: 0 0 14px rgba(248, 113, 113, 0.6); }
  .stage__n { font-weight: 700; color: #FFFFFF; font-size: 0.9em; }
  .stage__st { font-size: 0.74em; color: #8B93A1; margin-top: 3px; }

  /* ── FAQ ───────────────────────────────────────── */
  .faq { border-radius: var(--radio-md); padding: 20px 22px; }
  .faq__titulo {
    font-family: var(--mono);
    font-size: 0.72em;
    font-weight: 700;
    letter-spacing: 2.2px;
    text-transform: uppercase;
    color: #8B93A1;
    margin-bottom: 12px;
  }
  .faq__item { border-top: 1px solid rgba(255, 255, 255, 0.06); padding: 14px 0; }
  .faq__item:first-of-type { border-top: 0; padding-top: 0; }
  .faq__q { font-weight: 800; color: #FFFFFF; margin-bottom: 6px; font-size: 1.02em; }
  .faq__a { font-size: 0.9em; color: #9AA2B1; line-height: 1.5; }
  .faq__badge, .quiz__badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 1.45em; height: 1.45em;
    border-radius: 50%;
    background: color-mix(in srgb, var(--acento) 18%, transparent);
    border: 1px solid color-mix(in srgb, var(--acento) 45%, transparent);
    color: var(--acento);
    font-weight: 800;
    font-size: 0.78em;
    margin-right: 10px;
    vertical-align: baseline;
  }

  /* ── Quiz ──────────────────────────────────────── */
  .quiz { border-radius: var(--radio-md); padding: 22px; box-shadow: var(--sombra), var(--sombra-edge), var(--glow); }
  .quiz__q { font-weight: 800; font-size: 1.08em; color: #FFFFFF; margin-bottom: 16px; line-height: 1.4; }
  .quiz__op {
    display: flex;
    gap: 12px;
    align-items: center;
    background: var(--s3);
    border: 1px solid var(--linea);
    border-radius: var(--radio-sm);
    padding: 12px 16px;
    margin-bottom: 9px;
    color: #E4E8EF;
    font-size: 0.94em;
  }
  .quiz__op--ok { border-color: #34D399; background: rgba(52, 211, 153, 0.1); box-shadow: 0 0 24px -10px rgba(52, 211, 153, 0.7); }
  .quiz__mk {
    flex: 0 0 auto;
    width: 1.55em; height: 1.55em;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.06);
    color: var(--acento);
    display: flex; align-items: center; justify-content: center;
    font-weight: 800;
    font-size: 0.8em;
  }
  .quiz__op--ok .quiz__mk { background: #34D399; color: #0B0B10; }
  .quiz__pie { margin-top: 12px; font-family: var(--mono); font-size: 0.78em; color: #8B93A1; }

  /* ── Quote ─────────────────────────────────────── */
  .quote {
    position: relative;
    overflow: hidden;
    border-radius: var(--radio-md);
    padding: 34px 26px 24px 30px;
  }
  .quote::after {
    content: "";
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 4px;
    background: linear-gradient(180deg, var(--acento), transparent);
  }
  .quote__text { position: relative; font-size: 1.06em; color: #E9ECF2; line-height: 1.6; font-style: italic; }
  .quote__autor { display: flex; align-items: center; margin-top: 16px; font-weight: 800; color: #FFFFFF; font-size: 0.94em; }
  .quote__ava {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 2em; height: 2em;
    border-radius: 50%;
    background: linear-gradient(160deg, var(--acento-brillo), var(--acento));
    color: #0B0B10;
    font-weight: 900;
    font-size: 0.85em;
    margin-right: 12px;
    box-shadow: 0 0 20px -6px var(--acento-rgba-40);
  }
  .quote__rol { font-size: 0.82em; color: #8B93A1; margin-top: 2px; }

  /* ── Mitos vs realidad ─────────────────────────── */
  .mitos__bloque { border: 1.5px solid transparent; padding: 22px 24px; }
  .mitos__bloque--mito {
    background:
      linear-gradient(180deg, rgba(248, 113, 113, 0.1), rgba(248, 113, 113, 0.02)) padding-box,
      linear-gradient(145deg, rgba(248, 113, 113, 0.85), rgba(248, 113, 113, 0.1) 55%, #24242E) border-box;
  }
  .mitos__bloque--real {
    background:
      linear-gradient(180deg, rgba(52, 211, 153, 0.1), rgba(52, 211, 153, 0.02)) padding-box,
      linear-gradient(145deg, rgba(52, 211, 153, 0.85), rgba(52, 211, 153, 0.1) 55%, #24242E) border-box;
  }
  .mitos__label {
    display: inline-block;
    font-family: var(--mono);
    font-size: 0.68em;
    font-weight: 800;
    letter-spacing: 2.4px;
    padding: 4px 11px;
    border-radius: 999px;
    margin-bottom: 12px;
  }
  .mitos__bloque--mito .mitos__label { color: #F87171; background: rgba(248, 113, 113, 0.14); }
  .mitos__bloque--real .mitos__label { color: #34D399; background: rgba(52, 211, 153, 0.14); }
  .mitos__texto { font-size: 1.02em; line-height: 1.45; color: #FFFFFF; font-weight: 600; }
  .mitos__sub { font-size: 0.88em; color: #9AA2B1; margin-top: 8px; font-weight: 400; line-height: 1.45; }

  /* ── Card de repositorio ───────────────────────── */
  .repo-card { border-radius: var(--radio-md); }
  .repo-card__bar {
    padding: 14px 20px;
    background: rgba(255, 255, 255, 0.04);
    border-bottom: 1px solid var(--linea);
    font-family: var(--mono);
    font-size: 0.78em;
    color: #8B93A1;
  }
  .repo-card__body { padding: 22px 24px; }
  .repo-card__nombre { font-weight: 800; font-size: 1.22em; letter-spacing: -0.01em; color: var(--acento); }
  .repo-card__desc { font-size: 0.94em; color: #C9CFDA; line-height: 1.5; margin-bottom: 16px; }
  .chip {
    font-family: var(--mono);
    font-size: 0.68em;
    font-weight: 700;
    letter-spacing: 1px;
    padding: 5px 11px;
    border-radius: 999px;
    background: var(--s3);
    border: 1px solid var(--linea);
    color: #C9CFDA;
  }
  .chip--ok { background: rgba(52, 211, 153, 0.14); border-color: rgba(52, 211, 153, 0.45); color: #34D399; }
  .repo-card__tree, .repo-card__install {
    background: rgba(0, 0, 0, 0.35);
    border: 1px solid var(--linea);
    border-radius: var(--radio-sm);
    padding: 14px 16px;
    font-family: var(--mono);
    font-size: 0.82em;
    line-height: 1.65;
    color: #9AA2B1;
    white-space: pre-wrap;
  }
  .repo-card__install .prompt { color: var(--acento); font-weight: 800; }

  /* ── GitHub stats ──────────────────────────────── */
  .ghstats { border-radius: var(--radio-md); padding: 20px 22px; }
  .ghstats__repo { font-weight: 800; font-size: 1.08em; color: #FFFFFF; }
  .ghstats__lic {
    font-family: var(--mono);
    font-size: 0.64em;
    font-weight: 800;
    color: var(--acento);
    background: color-mix(in srgb, var(--acento) 14%, transparent);
    border: 1px solid color-mix(in srgb, var(--acento) 40%, transparent);
    padding: 4px 10px;
    border-radius: 999px;
  }
  .ghstats__desc { font-size: 0.88em; color: #9AA2B1; line-height: 1.5; margin-bottom: 14px; }
  .ghstats__nums { font-size: 0.88em; font-weight: 700; color: #E4E8EF; margin: 14px 0; font-variant-numeric: tabular-nums; }
  .ghstats__bar { height: 10px; border-radius: 999px; background: rgba(255, 255, 255, 0.06); margin-bottom: 10px; }
  .ghstats__langs { font-size: 0.78em; color: #9AA2B1; }
  .ghstats__dot { width: 9px; height: 9px; }

  /* ── Stack (tecnologías) ───────────────────────── */
  .stack { border-radius: var(--radio-md); padding: 20px 22px; }
  .stack__titulo {
    font-family: var(--mono);
    font-size: 0.72em;
    font-weight: 700;
    letter-spacing: 2.2px;
    text-transform: uppercase;
    color: #8B93A1;
    margin-bottom: 14px;
  }
  .stack__chip {
    background: var(--s3);
    border: 1px solid var(--linea);
    border-radius: 999px;
    padding: 9px 16px;
    font-size: 0.9em;
    color: #F3F4F6;
  }
  .stack__sub { color: #8B93A1; font-size: 0.84em; }
  .stack__dot { width: 11px; height: 11px; }
  .stack__pie { font-size: 0.82em; color: #8B93A1; }

  /* ── Error (traceback) ─────────────────────────── */
  .err { border-radius: var(--radio-md); }
  .err__bar { padding: 12px 16px; background: rgba(255, 255, 255, 0.04); border-bottom: 1px solid var(--linea); }
  .err__file { font-family: var(--mono); font-size: 0.78em; color: #8B93A1; }
  .err__titulo { padding: 14px 18px 0; font-weight: 800; font-size: 0.98em; color: #FFFFFF; }
  .err__body { padding: 14px 18px; font-family: var(--mono); font-size: 0.78em; line-height: 1.55; }
  .err__line--err, .err__line--err-head {
    color: #F87171;
    font-weight: 700;
    background: rgba(248, 113, 113, 0.08);
    border-radius: 4px;
  }
  .err__resumen {
    margin: 0 18px 14px;
    padding: 10px 14px;
    background: rgba(255, 255, 255, 0.05);
    border-left: 3px solid var(--acento);
    border-radius: 0 8px 8px 0;
    font-size: 0.84em;
    color: #F3F4F6;
  }
  .err__pie { padding: 0 18px 16px; font-size: 0.78em; color: #8B93A1; }

  /* ── Timeline de fases ─────────────────────────── */
  .tl { border-radius: var(--radio-md); padding: 20px 22px; }
  .tl__titulo {
    font-family: var(--mono);
    font-size: 0.72em;
    font-weight: 700;
    letter-spacing: 2.2px;
    text-transform: uppercase;
    color: #8B93A1;
    margin-bottom: 14px;
  }
  .tl__item { padding: 10px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.06); }
  .tl__mark {
    width: 32px; height: 32px;
    border-radius: 10px;
    border: 1.5px solid var(--linea);
    color: #8B93A1;
  }
  .tl__mark--ok { border-color: color-mix(in srgb, var(--acento) 60%, transparent); color: var(--acento); background: color-mix(in srgb, var(--acento) 12%, transparent); }
  .tl__mark--run { border-color: rgba(251, 191, 36, 0.55); color: #FBBF24; background: rgba(251, 191, 36, 0.12); }
  .tl__mark--error { border-color: rgba(248, 113, 113, 0.55); color: #F87171; background: rgba(248, 113, 113, 0.12); }
  .tl__txt b { font-size: 0.96em; color: #F3F4F6; }
  .tl__sub { font-size: 0.84em; color: #8B93A1; }
  .tl__pie { font-size: 0.82em; color: #8B93A1; }

  /* ── Índice del post ───────────────────────────── */
  .idx { border-radius: var(--radio-md); padding: 20px 22px; }
  .idx__titulo {
    font-family: var(--mono);
    font-size: 0.72em;
    font-weight: 700;
    letter-spacing: 2.2px;
    text-transform: uppercase;
    color: #8B93A1;
    margin-bottom: 12px;
  }
  .idx__item { padding: 9px 0; gap: 14px; }
  .idx__n {
    width: 34px; height: 34px;
    border-radius: 10px;
    background: linear-gradient(160deg, var(--acento-brillo), var(--acento));
    color: #0B0B10;
    font-weight: 900;
    box-shadow: 0 0 18px -6px var(--acento-rgba-40);
  }
  .idx__v { font-size: 0.96em; color: #E9ECF2; font-weight: 600; }
  .idx__pie { font-size: 0.82em; color: #8B93A1; }

  /* ── QR ────────────────────────────────────────── */
  .qr { border-radius: var(--radio-md); padding: 20px 22px; }
  .qr__titulo { font-weight: 800; font-size: 1.02em; color: #FFFFFF; margin-bottom: 14px; }
  .qr__caja {
    background: #FFFFFF;
    padding: 18px 18px 14px;
    border-radius: var(--radio-md);
    box-shadow:
      0 0 0 4px color-mix(in srgb, var(--acento) 32%, transparent),
      0 0 48px -10px var(--acento-rgba-40);
  }
  .qr__escanea { color: #0B0B10; font-family: var(--mono); }
  .qr__pie { font-size: 0.86em; color: #9AA2B1; }

  /* ── Social / valor ────────────────────────────── */
  .social {
    background:
      linear-gradient(160deg, color-mix(in srgb, var(--acento) 13%, #0B0B10), #0B0B10 62%) padding-box,
      var(--borde-deg) border-box;
    border: 1.5px solid transparent;
    border-radius: var(--radio-lg);
    padding: 32px;
    box-shadow: var(--sombra), var(--sombra-edge), var(--glow);
  }
  .social__kicker {
    font-family: var(--mono);
    letter-spacing: 2.6px;
    font-size: 0.72em;
    text-transform: uppercase;
  }
  .social__titulo { font-weight: 900; font-size: 1.35em; letter-spacing: -0.015em; line-height: 1.2; }
  .social__texto { font-size: 0.96em; color: #C9CFDA; line-height: 1.55; }
  .social__cta {
    background: linear-gradient(135deg, var(--resalte), var(--resalte-brillo));
    color: #0B0B10;
    box-shadow: 0 0 34px -8px var(--resalte-brillo);
    letter-spacing: 0.4px;
  }

  /* ══════════════════════════════════════════════════════════════
     WAVE 4 · componentes nuevos
     ══════════════════════════════════════════════════════════════ */

  /* ── dato-hero: la cifra que frena el scroll ───── */
  .hero-dato {
    position: relative;
    overflow: hidden;
    text-align: center;
    padding: 34px 28px 30px;
    border: 1.5px solid transparent;
    background: var(--surf) padding-box, var(--borde-deg) border-box;
    border-radius: var(--radio-lg);
    box-shadow: var(--sombra), var(--sombra-edge), var(--glow);
  }
  .hero-dato::before {
    content: "";
    position: absolute;
    left: 16%; right: 16%; top: 0;
    height: 3px;
    border-radius: 0 0 3px 3px;
    background: linear-gradient(90deg, transparent, var(--acento), transparent);
  }
  .hero-dato__eyebrow {
    font-family: var(--mono);
    font-size: 0.66em;
    font-weight: 700;
    letter-spacing: 2.6px;
    text-transform: uppercase;
    color: #8B93A1;
    margin-bottom: 12px;
  }
  .hero-dato__val {
    font-weight: 900;
    font-size: 3.3em;
    line-height: 0.95;
    letter-spacing: -0.03em;
    background: linear-gradient(160deg, #FFFFFF 6%, var(--acento-brillo) 48%, var(--acento));
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 0 30px var(--acento-rgba-30));
  }
  .hero-dato__lbl { margin-top: 14px; font-weight: 800; font-size: 1.06em; color: #FFFFFF; line-height: 1.3; }
  .hero-dato__sub { margin-top: 8px; font-size: 0.9em; color: #9AA2B1; line-height: 1.5; }
  .hero-dato__src {
    margin-top: 18px;
    font-family: var(--mono);
    font-size: 0.64em;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #6B7280;
  }

  /* ── split: dos paneles enfrentados ────────────── */
  .split { text-align: left; }
  .split__titulo {
    font-weight: 800;
    font-size: 1.08em;
    text-align: center;
    margin-bottom: 22px;
    color: #FFFFFF;
    letter-spacing: -0.01em;
  }
  .split__grid {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: 12px;
    align-items: stretch;
  }
  .split__lado {
    border: 1.5px solid transparent;
    border-radius: var(--radio-md);
    padding: 20px 18px;
    box-shadow: var(--sombra);
    min-width: 0;
  }
  .split__lado--a {
    background:
      linear-gradient(180deg, rgba(248, 113, 113, 0.06), rgba(248, 113, 113, 0.01)) padding-box,
      linear-gradient(145deg, rgba(248, 113, 113, 0.8),
        rgba(248, 113, 113, 0.1) 55%, #24242E) border-box;
  }
  .split__lado--b {
    background:
      linear-gradient(180deg, rgba(52, 211, 153, 0.06), rgba(52, 211, 153, 0.01)) padding-box,
      linear-gradient(145deg, rgba(52, 211, 153, 0.8),
        rgba(52, 211, 153, 0.1) 55%, #24242E) border-box;
  }
  .split__vs {
    align-self: center;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 3em; height: 3em;
    border-radius: 50%;
    background: var(--s2);
    border: 1px solid color-mix(in srgb, var(--acento) 45%, transparent);
    color: var(--acento);
    font-family: var(--mono);
    font-size: 0.8em;
    font-weight: 800;
    letter-spacing: 1px;
    box-shadow: 0 0 26px -8px var(--acento-rgba-40);
  }
  .split__tag {
    font-family: var(--mono);
    font-size: 0.62em;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 10px;
  }
  .split__lado--a .split__tag { color: #F87171; }
  .split__lado--b .split__tag { color: #34D399; }
  .split__t { font-weight: 800; font-size: 1.04em; color: #FFFFFF; margin-bottom: 8px; line-height: 1.25; }
  .split__c { font-size: 0.9em; color: #C9CFDA; line-height: 1.45; }
  .split__items { margin-top: 10px; }
  .split__item { display: flex; gap: 9px; align-items: flex-start; font-size: 0.88em; color: #C9CFDA; line-height: 1.4; padding: 5px 0; }
  .split__dot { flex: 0 0 auto; width: 6px; height: 6px; border-radius: 50%; margin-top: 0.5em; background: currentColor; opacity: 0.6; }

  /* ── progreso: barra de avance con hitos ───────── */
  .prog {
    border: 1.5px solid transparent;
    background: var(--surf) padding-box, var(--borde-deg) border-box;
    border-radius: var(--radio-md);
    padding: 22px 24px;
    text-align: left;
    box-shadow: var(--sombra), var(--sombra-edge);
  }
  .prog__titulo {
    font-family: var(--mono);
    font-size: 0.72em;
    font-weight: 700;
    letter-spacing: 2.2px;
    text-transform: uppercase;
    color: #8B93A1;
    margin-bottom: 16px;
  }
  .prog__head { display: flex; align-items: center; gap: 14px; }
  .prog__track {
    flex: 1;
    height: 14px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.07);
    overflow: hidden;
    box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.6);
  }
  .prog__fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, var(--acento), var(--acento-brillo));
    box-shadow: 0 0 20px -2px var(--acento-rgba-40);
  }
  .prog__pct {
    font-family: var(--mono);
    font-weight: 900;
    font-size: 1.45em;
    letter-spacing: -0.02em;
    color: #FFFFFF;
    min-width: 2.6em;
    text-align: right;
  }
  .prog__etiqueta { margin-top: 12px; font-size: 0.9em; color: #9AA2B1; line-height: 1.45; }
  .prog__hitos { display: flex; flex-wrap: wrap; gap: 10px 18px; margin-top: 16px; }
  .prog__hito { flex: 1 1 44%; display: inline-flex; align-items: center; gap: 8px; font-size: 0.84em; color: #C9CFDA; line-height: 1.35; }
  .prog__dot { width: 9px; height: 9px; border-radius: 50%; background: #475569; }
  .prog__hito--ok { color: #E4E8EF; }
  .prog__hito--ok .prog__dot { background: #34D399; box-shadow: 0 0 12px rgba(52, 211, 153, 0.6); }
  .prog__hito--run .prog__dot { background: #FBBF24; box-shadow: 0 0 12px rgba(251, 191, 36, 0.6); }
  .prog__hito--error .prog__dot { background: #F87171; box-shadow: 0 0 12px rgba(248, 113, 113, 0.6); }

  /* ── fix: el error y la solución ───────────────── */
  .fix {
    border: 1.5px solid transparent;
    background: var(--surf) padding-box, var(--borde-deg) border-box;
    border-radius: var(--radio-md);
    overflow: hidden;
    text-align: left;
    box-shadow: var(--sombra), var(--sombra-edge);
  }
  .fix__titulo {
    font-family: var(--mono);
    font-size: 0.72em;
    font-weight: 700;
    letter-spacing: 2.2px;
    text-transform: uppercase;
    color: #8B93A1;
    padding: 14px 18px;
    border-bottom: 1px solid var(--linea);
  }
  .fix__row { display: grid; grid-template-columns: 1fr auto 1fr; align-items: stretch; }
  .fix__col { min-width: 0; display: flex; flex-direction: column; }
  .fix__panel {
    flex: 1;
    font-family: var(--mono);
    font-size: 0.74em;
    line-height: 1.6;
    padding: 10px 14px 14px;
  }
  .fix__panel--malo { background: rgba(248, 113, 113, 0.08); }
  .fix__panel--bueno { background: rgba(52, 211, 153, 0.08); }
  .fix__line { white-space: pre-wrap; word-break: break-word; }
  .fix__panel--malo .fix__line { color: #FCA5A5; }
  .fix__panel--bueno .fix__line { color: #6EE7B7; }
  .fix__lbl {
    font-family: var(--mono);
    font-size: 0.66em;
    font-weight: 800;
    letter-spacing: 1.8px;
    padding: 12px 14px 8px;
  }
  .fix__lbl--malo { color: #F87171; }
  .fix__lbl--bueno { color: #34D399; }
  .fix__arrow {
    align-self: center;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 2em; height: 2em;
    margin: 0 6px;
    border-radius: 50%;
    background: var(--acento);
    color: #0B0B10;
    font-size: 0.78em;
    font-weight: 900;
    box-shadow: 0 0 22px -6px var(--acento-rgba-40);
  }
  .fix__nota { font-size: 0.82em; color: #8B93A1; padding: 12px 18px 14px; border-top: 1px solid var(--linea); }

"""
