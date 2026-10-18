---
name: tech-carousel
description: Use when the user asks to create professional Instagram carousel slides for tech education (cybersecurity, programming, AI, infra) with tech_carousel.py in this skill folder — requires HEX accent color and slide count. Writes copy + HTML + PNG into the CTSLIDER work folder (/sdcard/CTSLIDER, override with CTSLIDER_DIR). 23 components: terminal, cards, compare, repo, diagrams, code, editor, tree, http, diff, stats, layers, pipeline, tabla, faq, quote, quiz and more. 235 professional icons (Lucide + hand-drawn) picked semantically from the slide text; icon_smith.py and the icon-smith agent add icons per topic.
---

# Crear Carousel Tech (Ciberseguridad · Programación · IA)

Genera un carrusel de Instagram completo (copywriting + HTML + componentes gráficos + PNG renderizados) con `tech_carousel.py`, la librería `icons/` y los componentes `components/`.

Funciona con CUALQUIER tema técnico y CUALQUIER cantidad de slides (7 a 10 recomendados, mínimo 3).

**Identidad:** `CHMODX`. Marca configurable con `--marca`.

## Ideología (CHMODX · educativo · sin censura responsable)

- **Educativo primero.** Cada slide explica qué es, por qué importa y cómo aplicarlo (mínimo 1 aplicación práctica por bloque).
- **Técnico y preciso.** Terminología correcta, sin hype ni promesas vacías. Cero datos inventados: si no es verificable, no se publica.
- **Sin censura innecesaria.** Se abordan vulnerabilidades, ataques y trade-offs tal como existen.
- **Responsable por diseño.** NUNCA se incluyen payloads ejecutables listos para abuso, credenciales reales, víctimas ni pasos para dañar. Los ejemplos son teóricos/defensivos o de laboratorio propio. Difundir una vulnerabilidad explicando cómo defenderse es educación; entregar un arma no lo es.
- **Progresivo (scaffolding).** Hook → desarrollo incremental → cierre accionable.
- **Determinista.** Sin llamadas a LLM/API. Mismo entrada → mismo resultado.
- **Alto valor.** 1 idea útil y aplicable por slide.

Verticales: `cybersec` (blue/red team, appsec, cloudsec, zero trust) · `prog` (fundamentos, patrones, arquitectura, testing) · `ai` (LLMs, RAG, agentes, evals, seguridad IA) · `infra` (redes, Linux, contenedores, CI/CD, SRE).

## Brief inicial (obligatorio, siempre antes de empezar)

Nunca empieces un carrusel sin este brief. Pregunta con la herramienta de
preguntas (multi-selección donde aplique) y recién después ejecuta:

**P1 — Tipo de post** (uno; define `--preset` y el contexto de todo el copy):

| Tipo | `--preset` | Vertical | Set de componentes |
|---|---|---|---|
| Repo de GitHub | `repo` | prog | `card-repo, gh-stats, tree, code, terminal` |
| Enseñar comandos | `comandos` | infra | `terminal, tabla, code, checklist, quiz` |
| Código Python | `python` | prog | `editor, code, terminal, diff, quiz` |
| Mixto / otro | `mixto` | auto | auto (banco del vertical) |

**P2 — Tema + color + slides** (los 3 obligatorios de siempre; el color y los
slides nunca se deducen).

**P3 — Componentes** (multi-selección; default: el set del preset elegido;
`auto` = banco completo del vertical).

**P4 — Extras**: formato (default 9:16), `--repo` URL (obligatorio para preset
`repo`: va al primer comentario), `--landing` URL propia (opcional: cierra el
carrusel hacia tu dominio/landing en vez de "síguenos"), `--copy-redes`,
`--marca` (default CHMODX).

Sin `--preset`, el banco del vertical decide los componentes (modo `mixto`).
Con `--preset`, la auto-generación filtra el banco a la whitelist y el builder
avisa si un slide manual usa un componente fuera de la lista.

## Entrada del usuario (4 datos)

1. **Tema** — ej: "SQL injection en APIs REST".
2. **Color HEX** — OBLIGATORIO. `#RRGGBB` (o nombre de paleta: rojo/azul/verde/purpura/naranja/rosa/dorado).
3. **Cantidad de slides** — OBLIGATORIA. `--slides N`. Recomendado 7-10.
4. **Tema corto para títulos** (opcional) — ej: "SQL injection". Si falta, primeras 4 palabras del tema.

Opcional: formato (default **9:16** = 1080×1920), vertical (`--vertical auto` = default, o `cybersec|prog|ai|infra`), `--resalte` (default: el mismo `--color`), `--cta-palabra`, `--hashtags`, `--marca`, `--copy-redes`, `--offline`.

Si falta color, slides o tema, preguntá con AskUserQuestion antes de empezar. **Nunca** deduzcas el HEX ni la cantidad de slides por tu cuenta.

## CLI

```bash
python3 ~/.config/opencode/skills/tech-carousel/tech_carousel.py \
  --tema <slug-del-tema> \
  --color "#RRGGBB" \
  --slides 8 \
  --formato 9:16 \
  --vertical cybersec \
  --display-tema "<tema legible>" \
  --short-tema "<tema corto 3-4 palabras>"
```

| Flag | Requerido | Descripción |
|------|-----------|-------------|
| `--tema` | sí | Carpeta fuente en CTSLIDER |
| `--color` | **sí** | HEX `#RRGGBB` o nombre de paleta |
| `--slides` | **sí** | Cantidad de diapositivas (debe coincidir con `slide-*.html` reales) |
| `--formato` | no | `9:16` (default) · `3:4` · `4:5` · `1:1` |
| `--vertical` | no | `auto` (default: se deduce del slug) o fijo `cybersec\|prog\|ai\|infra` |
| `--iconos` | no | `auto` (default) o `--iconos <categoria>` |
| `--sin-placa` | no | Iconos en modo clásico (sin la placa duotono) |
| `--componentes` | no | `auto` (default) o lista fijada `terminal,card-compare` |
| `--preset` | no | `repo` · `comandos` · `python` · `mixto` (default: receta tipo de post) |
| `--marca` | no | Marca del pie (default `CHMODX`) |
| `--badge` | no | Texto del badge de portada |
| `--cta-palabra` | no | Palabra del CTA (default: determinista desde el slug) |
| `--cta-modo` | no | `seguir` (default: botón negro con borde de acento "SÍGUENOS Y NO TE PIERDAS LO QUE SIGUE" + copy de valor) o `comentar` (botón 'Comenta X') |
| `--repo` | no | URL del repo (va al primer comentario de copy-redes) |
| `--landing` | no | URL propia (ej `https://chmodxcode.pro`). Activa el **cierre con landing**: slide N-1 empuja a programar + mini-card del dominio, slide N muestra el dominio gigante como CTA primario (los comandos siguen presentes, en línea secundaria hacia el primer comentario), y caption/copy-redes/primer comentario arrancan con el enlace |
| `--landing2` / `--landing2-texto` | no | Segunda URL del cierre (ej canal de Telegram). Agrega un **botón secundario** (borde punteado) en el slide final y una línea extra en caption/copy/primer comentario |
| `--workers` | no | Chromium en paralelo (default: núcleos-1, máx 4). Baja un carrusel de ~1m/slide a ~15s/slide |
| `--solo-html` | no | Escribe los HTML + auto-fit **sin** renderizar PNG, story ni copy (iterar en segundos) |
| `--incremental` | no | Salta los slides cuyo HTML no cambió (hash en `preview/.hashes.json`) y reusa sus PNG |
| `--sin-autofit` | no | No ajusta el zoom automáticamente; sólo avisa los recortes |
| `--contact-sheet` | no | Genera `contact-sheet.png` (grilla con todo el carrusel, revisión de un vistazo) |
| `--pdf` | no | Exporta el carrusel completo a PDF (una página por slide) |
| `--reel` | no | Exporta un MP4 vertical con ffmpeg (si está instalado) |
| `--sin-guia` | no | No inyecta la card funnel del slide 2 |
| `--guia-titulo` / `--guia-sub` | no | Personalizan la card funnel del slide 2 |
| `--resalte` | no | Color de keywords (default: **el mismo `--color`**) |
| `--short-tema` / `--display-tema` | no | Tema corto (títulos) / legible (caption) |
| `--hashtags` | no | `a,b,c` |
| `--solo-story` | no | Re-render solo story |
| `--copy-redes` | no | Además de `caption.txt`, escribe `copy-redes.md` (IG/TikTok/FB/Story) |
| `--offline` | no | No enlaza Google Fonts: render con fuentes locales (para Chromium sin red) |
| `--no-auto` | no | No escribir copy si falta la carpeta: falla explicando qué hacer |

**1 comando = copy + HTML + PNG + verificación.** Si la carpeta fuente no existe, el mismo comando la crea con el copy de los `N` slides (y `story-fuente.html`) y sigue. Usá `--no-auto` cuando quieras controlar vos los slides fuente.

El builder imprime en la cabecera: `Color`, `Slides`, `Vertical`, `Íconos`, `Resalte`, `Badge`, `CTA`. Verificá esos valores antes de publicar.

## ¿Esta skill o `crear-carousel`?

| | `tech-carousel` (esta) | `crear-carousel` |
|---|---|---|
| Pasos | **1**: `tech_carousel.py` hace copy → HTML → render → verificación | **2**: `generar_carousel_ab.py` para los PNGs, después `crear-audio` para el audio |
| Temas | Técnico (cybersec, prog, IA, infra) | Psicología / desarrollo personal (AudioBlaze) |
| Componentes | terminal, code, diagrama, card-compare, card-repo, checklist, mitos, pasos, social, card-info | texto + iconos SVG por tema |
| Marca | `CHMODX` (`--marca`) | AudioBlaze |

Usá **`tech-carousel`** si el tema es técnico. Usá **`crear-carousel`** si es para AudioBlaze. No las mezcles: los estilos, paletas y estructuras son distintos.


## Estructura viral de 7-10 slides (requerida)

1. **Slide 1 (Portada/Hook):** título MÁXIMO 8 palabras (tensión técnica legítima, no engañosa) + subtítulo MÁXIMO 2 líneas + **1 componente gancho** (terminal con evidencia por default, desde `HOOK_COMPS` de cada vertical en `copywriting/`). La portada es el slide más importante: es lo que frena el scroll y decide si guardan el post. El builder conserva el componente tras el subtítulo (ver `generar_html()` rama `i == 1`).
2. **Slides 2..N-2 (Contenido de valor):** MÁXIMO 3 líneas de texto por slide (40-50 palabras), 1 idea clara. Usá `.clave` en 1-2 keywords. Concepto largo → dividiólo en 2 slides.
3. **Slide N-1 (Puente-recap):** el script arma "Antes del final: el resumen" con checklist de las 3 ideas clave extraídas del propio carrusel (títulos de inicio/medio/cierre, 7 palabras máx). Sin títulos suficientes, usa una frase puente del banco `PUENTES`. Con `--landing`, el título pasa a "Ver no es hacer: empieza a programar hoy" y se agrega una mini-card con el dominio (curso + Telegram). No generar copy manual.
4. **Slide N (CTA final):** el script inyecta "¿Listo para aplicarlo?", terminal con TODOS los comandos del carrusel, card gigante "COPIA LOS COMANDOS DEL PRIMER COMENTARIO", botón CTA y línea de cierre. `--cta-modo comentar` (default): botón "Comenta [PALABRA] y te paso la checklist completa". `--cta-modo seguir`: botón "SÍGUENOS Y NO TE PIERDAS LO QUE SIGUE" + "Guarda este carrusel: lo vas a necesitar · El próximo tema lo eligen los seguidores" (gatillos de pérdida + pertenencia). Con `--landing` se reemplaza ese bloque: título "De mirar a programar", terminal (máx 6 comandos), card gigante con el dominio + "Curso de Python completo y canal de Telegram" + botón "EMPIEZA EN [DOMINIO]" (sin flecha), y línea fina "Todos los comandos completos están en el primer comentario". NO generar copy manual.

Reglas de copy:
- Hooks: curiosidad técnica legítima ("Tu config por defecto no es segura"), nunca clickbait falso ("esto te va a asustar").
- Tono: autoridad didáctica, directa. Sin coaching motivacional ni conspirativismo.
- Datos: solo cifras verificables. Si no lo puedes verificar, descríbelo cualitativamente.
- Dialecto: tuteo neutro latino. Sin voseo, sin regionalismos, sin rituales.
- Dividió el tema en N-3 bloques (quedan 1 y N-1/N fijos).

## Componentes gráficos (nuevos, de alto valor)

Los componentes van declarados en el slide fuente dentro de `.contenido`. El builder los expande a HTML+CSS y falla si falta el wrapper `.slide` (ver "Regla de oro").

Sintaxis (data-props es JSON con comillas dobles, atributo con comillas simples):

```html
<div class="componente" data-component="terminal" data-props='{"lines":[
  {"t":"cmd","v":"nmap -sV 10.0.0.5"},{"t":"out","v":"22/tcp  open  ssh"},
  {"t":"ok","v":"3 puertos abiertos"}]}'>
</div>
```

Si `data-props` no está, el JSON se toma del texto interior del `<div class="componente">`.

| `data-component` | Uso | Props principales |
|---|---|---|
| `terminal` | Comandos CLI, walkthroughs, debugging | `lines: [{t:"cmd\|out\|err\|warn\|ok", v:"..."}]`, `titulo` |
| `card-info` | Conceptos, definiciones, notas | `variante: info\|tip\|warn\|danger`, `titulo`, `cuerpo`, `icono` |
| `card-compare` | A vs B, pros/contras, before/after | `titulo`, `cols: [{nombre, badge, items:[{ok:true,v}]}]` |
| `card-repo` | Repos, README, proyectos OSS | `repo`, `desc`, `tree`, `install`, `badges: []` |
| `diagram` | Topologías, flujos, attack path defensivo | `titulo`, `nodos: [{v, sub, tipo}]` (se encadenan con flechas) |
| `pasos` | Infografía de pasos/timeline | `titulo`, `pasos: [{t, d}]` |
| `code` | Snippets prácticos | `lenguaje`, `codigo`, `notas` |
| `checklist` | Takeaways / resumen accionable | `titulo`, `items: []` |
| `mitos` | Mito vs realidad | `mito`, `realidad` |
| `social` | Portadas/CTA valor | `titulo`, `texto`, `cta` |
| `tree` | Árbol de archivos o ramas git | `titulo`, `nodos: [{v, depth, tipo: dir\|file}]` o `tree: "texto"`, `modo: fs\|git`, `ramas: []` |
| `http` | Request/response de API | `metodo`, `ruta`, `codigo`, `nota_estado`, `request`, `response` |
| `browser` | Mock de ventana web | `url`, `titulo`, `vista` |
| `diff` | Antes vs después (código/config) | `titulo`, `antes`, `despues` |
| `stats` | Métricas / cifras impacto | `titulo`, `items: [{valor, etiqueta}]` |
| `tabla` | Tabla comparativa densa | `titulo`, `headers: []`, `filas: [[]]` |
| `layers` | Capas (OSI, Docker, pirámide) | `titulo`, `capas: [{v, sub, tipo}]` |
| `pipeline` | Etapas CI/CD o flujo deploy | `titulo`, `etapas: [{v, estado: ok\|run\|warn\|err\|idle}]` |
| `faq` | Pregunta + respuesta / objeciones | `titulo`, `pregunta`, `respuesta` o `items: [{q, a}]` |
| `quote` | Cita o principio editorial | `texto`, `autor` (default `CHMODX`), `rol` |
| `quiz` | Pregunta + opciones (engagement) | `pregunta`, `opciones: [{v, ok}]`, `pie` |
| `editor` | Snippet como ventana de IDE | `archivo`, `lenguaje`, `codigo`, `salida`, `pie` |
| `gh-stats` | Ficha de repo GitHub | `repo`, `desc`, `stars`, `forks`, `issues`, `licencia`, `lenguajes: [{n, p}]`. Con `"auto": true` trae los datos **reales** de la API de GitHub |
| `qr` | Código QR escaneable desde pantalla (cierra el funnel) | `url` (obligatorio), `titulo`, `pie`, `escanea`, `color` (default negro) |
| `stack-tec` | Fila de tecnologías/stack (alias `tecnologias`) | `titulo`, `items: [{v, sub, color}]` o `["Python", "Git"]`, `pie` |
| `error` | Consola con traceback real (errores típicos) | `titulo`, `archivo`, `texto` (traceback completo), `linea` (resumen), `pie` |
| `timeline-fases` | Ruta de aprendizaje por fases/semanas (alias `roadmap`) | `titulo`, `etapas: [{v, sub, estado: ok\|run\|error}]`, `pie` |
| `indice` | "Lo que verás" numerado (alias `toc`) | `titulo`, `items: ["...", ...]` o `[{v}]`, `pie` |

Reglas por componente (el builder valida y avisa):
- **`code`**: máx 8 líneas visibles por slide. Si es más largo, dividiólo en 2 slides. Tipografía mono Hask, fondo `#0F172A`, borde `#334155`.
- **`terminal`**: prompt `$` (o `#` para root), salida en `#9CA3AF`, éxito `#10B981`, error `#EF4444`, warning `#F59E0B`.
- **`card-compare`**: máx 4 items por columna, 2 columnas.
- **`diagram`**: máx 5 nodos por slide (legibilidad vertical). Caja con borde acento, flecha entre nodos.
- **`checklist`**: máx 4 items, check verde.
- **`tree`**: máx 10 líneas; `depth` = nivel de sangría; `tipo` se infiere por `/` final si falta. Modo `git`: `ramas: ["main*", ...]` con `*` en la actual.
- **`http`**: `request`/`response` máx 8 líneas c/u; el método tiñe el badge (GET verde, POST azul, PUT ámbar, DELETE rojo).
- **`diff`**: máx 8 líneas en total (4+4); panel ANTES rojo / DESPUÉS verde.
- **`stats`**: máx 4 tarjetas; valores solo verificables o cualitativos (nunca cifras inventadas).
- **`tabla`**: máx 4 filas.
- **`layers`**: máx 5 capas; `tipo: front|back|db|api` tiñe el borde.
- **`pipeline`**: máx 5 etapas; `estado: ok|run|warn|err|idle`.
- **`faq`**: máx 3 items (o 1 `pregunta`+`respuesta`).
- **`quiz`**: máx 4 opciones; 1 sola `ok: true`; el `pie` apunta al siguiente slide.
- **`editor`**: máx 10 líneas de código + 4 de salida; reutiliza el resaltado de `code`; barra de estado con archivo y lenguaje.
- **`gh-stats`**: máx 4 lenguajes (barra proporcional + leyenda); stars/forks/issues como texto documentado, nunca inventado. Con `"auto": true` los trae de la API de GitHub (fallback a los valores escritos si no hay red).
- **`qr`**: máx 1 por slide; el QR va sobre caja blanca (escaneable sobre fondo negro). Requiere `segno` (`pip install --user --break-system-packages segno`); sin él degrada a la URL en texto.
- **`stack-tec`**: máx 8 chips. `color` opcional; si falta se deduce por nombre de tecnología.
- **`error`**: máx 12 líneas. `Traceback`/`Error`/`Exception` se tiñen de rojo, `File`/contexto en ámbar.
- **`timeline-fases`**: máx 6 etapas. `estado` = `ok` (✓ acento) · `run` (▶ ámbar) · `error` (✕ rojo).
- **`indice`**: máx 7 items; numerados automáticamente.
- Todo componente respeta 1 idea principal por slide.

## Componentes por categoría de post (matriz)

El prompt controla los componentes por 3 vías: `--vertical` (elige el banco
`COBERTURA` en `copywriting/`), `--componentes` (fuerza el set) y `--no-auto`
+ HTML a mano (control total). Combinaciones recomendadas:

| Categoría de post | `--componentes` sugerido | Vertical |
|---|---|---|
| Comando / tutorial (Linux, nmap, docker) | `terminal,tree,checklist` | infra, cybersec |
| Comparativa X vs Y / antes-después | `card-compare,diff,tabla` | cualquiera |
| Arquitectura (RAG, OSI, CI/CD) | `diagram,layers,pipeline` | ai, infra |
| API / endpoint (REST, auth, SQLi) | `http,code,card-info` | cybersec, prog |
| Proyecto / repo OSS | `card-repo,tree,code` | prog |
| Estructura de proyecto / Git flow | `tree,terminal,pasos` | prog, infra |
| Métricas / incidente | `stats,pipeline,checklist` | infra |
| Engagement / mito | `mitos,quiz,faq,quote` | cualquiera |
| Definición / concepto | `card-info,faq,quote` | ai, prog |

Estructura de prompt recomendada por categoría (la portada siempre lleva
hook + subtítulo + componente gancho automático):

```
@tech-carousel — [categoría]: [tema]. Color [#HEX], [N] slides.
Forzar: --componentes [set de la matriz] (opcional).
```

## Sets de íconos (por tema + rol)

**235 glyphs** en 8 categorías. La librería combina **Lucide** (line-art 24×24, ISC,
normalizado al estilo de la casa) con el **trazo a mano** original, que gana si
comparten nombre. El color sale del acento del carrusel (gradiente `url(#c)`).

Precedencia de `detectar_categoria()` (primer match gana, orden crítico anti-colisión):

| Categoría | Keywords del slug/tema |
|---|---|
| `cybersec` | ciber, seguridad, vulner, inyecc, sql, xss, phishing, ransom, malware, exploit, pentest, zero-trust, auth, firewall, red-team, blue-team, cifrado, hashing, 2fa, xxe, csrf, log4shell, ddos, burp, owasp |
| `dev` | python, javascript, java, rust, go, git, commit, api, rest, test, refactor, patrón, arquitectura, diseño, algoritmo, base-de-datos, sql-code, docker-code, linter, ide |
| `ai` | ia, inteligencia, llm, gpt, prompt, rag, embedding, agente, modelo, token, fine-tuning, entrenar, inferencia, transformer, mcp, guardrails, alucina, vision |
| `infra` | red, redes, linux, servidor, servidor, kubernetes, contenedor, ci-cd, pipeline, nube, aws, deploy, sre, monitoreo, observabilidad, dns, tcp, ip, subred, vpn, ssh |
| `data` | dato, datos, dataframe, analitica, metrica, grafica, dashboard, etl |
| `common` | (fallback temático) |
| `educativo` | tutorial, guia, curso, paso, aprende |
| `tech` | default universal (si no matchea ninguno) |

Verificá la categoría detectada (la imprime el builder) o forzá con `--iconos <categoria>`.

### Icono semántico (el texto del slide decide)

Ya no es solo "vertical → set": cada slide busca en **su propio texto** (título,
cuerpo y props de los componentes) una **palabra clave** y usa el glyph que
corresponde — `docker`→contenedor, `phishing`→anzuelo, `fuga`→correo en riesgo,
`roadmap`→ruta, `ransomware`→candado, etc. Gana la clave que aparece **más
temprano** en el texto y se exige **límite de palabra** (así `pipeline` no cae en
`pip` ni `funciona` en `funciones`). Si no hay match, cae al **rol**:

| Rol | Glyph |
|---|---|
| Portada (1) | primer glyph del set |
| Contenido | rota por índice, sin repetir los ya usados |
| Puente (N-1) | `list-checks` / `target` / `flag` / `check` |
| Cierre (N) | `rocket` / `arrow-right` / `check` / `target` |

### Estilo: placa duotono + glow

Los iconos se pintan dentro de una **placa** (esquina redondeada, relleno de
acento, borde y halo) que ocupa el mismo `__icon_size__`, así que no altera el
layout ni el auto-fit. Modo clásico sin placa: `--sin-placa`.

### Crear iconos para un tema (`icon_smith.py` + agente `icon-smith`)

```bash
cd ~/.config/opencode/skills/tech-carousel
python3 icon_smith.py sugerir "Fugas de correo con Python" --slides 7
python3 icon_smith.py sugerir --tema <slug> --dir "$CTSLIDER_DIR"   # slides reales
python3 icon_smith.py buscar "kubernetes"        # qué matchea y qué falta
python3 icon_smith.py catalogo --grep shield     # 2159 iconos de Lucide
python3 icon_smith.py agregar cybersec shield-half --kw "media luna"
python3 icon_smith.py listar cybersec
```

`agregar` baja el SVG de Lucide, lo normaliza y lo escribe en el **overlay**
`icons/lucide_extra.py` (+ reglas en `icons/tema_extra.py`), que **no se pierde**
al regenerar la librería. Para re-sincronizar los sets curados de Lucide:

```bash
python3 -m icons.sync_lucide            # regenera icons/lucide_sets.py
python3 -m icons.registry --test        # valida TODOS los glyphs
```

El **agente `icon-smith`** (`.config/opencode/agents/icon-smith.md`) automatiza
ese ciclo: analiza el tema, agrega los iconos que faltan y verifica con el
self-test + la suite. Reglas duras: un solo `stroke-width` por elemento, sin
filtros SVG, `fill="none"`, y el color siempre por `url(#c)`.

## Pipeline (6 pasos)

### 1. Copywriting (AUTOMÁTICO si faltan archivos)

Se ejecuta solo dentro del paso 4 si no existen `slide-*.html` en la carpeta del tema. Para correrlo aparte (recomendado cuando querés revisar el copy antes de renderizar):

```bash
python3 ~/.config/opencode/skills/tech-carousel/generar_copy_tech.py \
  --tema <slug> --slides 8 --vertical cybersec \
  --color "#RRGGBB" \
  [--display-tema "<legible>"] [--short-tema "<corto>"]
```

Crea `slide-01..N.html` con la estructura viral + marcadores de componente cuando el tema lo amerita (comandos, comparativas, diagramas). Reglas:
- Slide 1: hook + subtítulo. Slide 2..N-2: contenido + `.clave` en 1-2 keywords. N-1 y N los maneja el builder.
- Componentes solo donde aportan: comandos → `terminal`, herramientas → `card-compare`, flujos → `diagram` o `pasos`, ejemplos → `code`.
- QA: sin voseo, sin regionalismos, sin datos inventados, sin payload ejecutable dañino.

### 2. Crear carpeta fuente + slides HTML (estructura exacta, probada)

Carpeta: `$CTSLIDER/<slug>/` con `$CTSLIDER = $CTSLIDER_DIR | /mnt/sdcard/CTSLIDER (Termux) | ~/CTSLIDER` (minúsculas, guiones).

```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  .titulo { font-weight: 700; }
  .cuerpo { font-weight: 400; }
  .dato { font-weight: 700; color: var(--acento); }
  .resaltar { font-weight: 700; }
  .cita { font-style: italic; }
  .clave { font-weight: 700; color: #06B6D4; }  /* = --color del carrusel */
</style>
</head>
<body>
  <div class="numero">1/8</div>
  <div class="slide">
    <div class="contenido">
      <div class="titulo">Título del slide</div>
      <div class="cuerpo">Contenido del slide.</div>
      <!-- componente opcional: ver tabla de componentes -->
    </div>
    <div class="pie">
      <span class="logo"></span>CHMODX · <TEMA>
    </div>
  </div>
</body>
</html>
```

Obligatorio: `<div class="numero">X/N</div>`, wrapper `<div class="slide">`, `<div class="contenido">`, `<div class="pie">`. `X/N` correcto = `--slides` correcto. **No pongas emoji/ícono**: el builder reemplaza por el ícono SVG de la categoría.

### 3. Story fuente (opcional)

`story-fuente.html` con `.titulo` y 1-2 `<span class="clave">` + `.cuerpo` como subtítulo. El builder arma la story pro: isotipo, título, subtítulo, **terminal con los 3 primeros comandos reales del carrusel** (extraídos de los slides) y **botón "VER POST COMPLETO EN EL PERFIL →"** (fondo negro, borde de acento). Sin `.pie` ni `.numero`. Re-render solo story: `--solo-story`.

### 4. Generar y renderizar

```bash
python3 ~/.config/opencode/skills/tech-carousel/tech_carousel.py \
  --tema <slug> --color "#RRGGBB" --slides 8 \
  --formato 9:16 --vertical cybersec \
  --display-tema "<legible>" --short-tema "<corto>"
```

Salidas en la carpeta del tema: `renders/` (HTML), `preview/` (PNG), `stories/`, `caption.txt`.
- Renderiza **en paralelo** (varios Chromium a la vez; `--workers` para fijarlo). Ajustá el conteo si la máquina se queda sin memoria.
- Mide títulos en Chromium (`Range.getClientRects()`) para la regla de keywords: 1 línea → 1 `.clave`, 2-3 líneas → 2. Repite hasta 3 pasadas.
- Tinte dinámico del isotipo con `CTSLIDER/logo.png` en el color HEX pedido.
- `--formato`: 9:16 → 1080×1920 · 3:4 → 1080×1440 · 4:5 → 1080×1350 · 1:1 → 1080×1080. El cuerpo del slide mide 44px (37 en 1:1) y el texto de los componentes nace de `__comp_base__` — 40px en 9:16/4:5/3:4 y 45px en 1:1 — inyectado en `.comp-wrap { font-size }`, porque ningún `.slide` fija `font-size` y sin eso los `em` de los componentes heredan los 16px del navegador (texto a mitad de tamaño). En formatos cortos el builder aligera además el shell en el dict `ajustes` de `_format_scaling()` (pad_top/pad_bottom/ícono/título), baja `__comp_zoom__` (0.80 en 4:5 y 3:4, 0.72 en 1:1) y en 1:1 oculta el chip `.ind-swipe`, que si no pisa el pie.
- **Auto-fit (default):** antes de renderizar mide el recorte de `.contenido` y, si un slide desborda, baja el zoom de su envoltorio `.ajuste` (de 1.0 hasta el piso 0.70) hasta que entra. Termina con `✓ Sin recortes` o `! slide-XX: sigue recortando Npx (piso alcanzado; acortá el copy)`. Con `--sin-autofit` sólo avisa. El wrapper `.ajuste` (dentro de `.contenido`) es lo que permite escalar sin tocar el diseño base.
- **Iteración rápida:** `--solo-html` escribe HTML + auto-fit sin PNG/story/copy; `--incremental` salta los slides cuyo HTML no cambió (hash) y reusa sus PNG.
- **Exports opcionales:** `--contact-sheet` (grilla `contact-sheet.png`), `--pdf` (carrusel en PDF), `--reel` (MP4 vertical con ffmpeg).

### 5. Verificar

- Cabecera del builder: `Color`, `Slides` y `Vertical` correctos, y el aviso de contraste del acento si aparece.
- Cada PNG: ícono nítido, portada con badge + barra de progreso, N-1 con puente, N con botón de CTA, 1 clave por línea de título en `--resalte`, sin texto cortado.
- Componentes: terminal/código legibles en el móvil, comparativas sin desborde, diagrama ≤5 nodos. Con `--contact-sheet`, revisá la grilla completa de un vistazo.
- **QA de repetición (automática):** al terminar, el builder compara el contenido de los slides fuente y avisa si dos slides no consecutivos comparten ≥85% del texto, o si un mismo componente aparece en la mitad o más de los slides. Son avisos, no bloquean.
- `caption.txt`: tema, palabra CTA, hashtags. Con `--landing`, verifica que arranque con el dominio (y el segundo enlace si usás `--landing2`).
- Reportá carpeta de salida, categoría de íconos y conteo final.

### 6. copy-redes.md

```bash
python3 ~/.config/opencode/skills/tech-carousel/generar_copy_tech.py --carpeta <slug> [--funnel]
```

Genera copy por plataforma (Instagram 60-95 palabras, TikTok 30-50, Facebook 60-110, Story ≤8 palabras en mayúsculas) con QA de presupuesto de palabras, dialecto neutro y hashtags exactos (IG 9, TT 5, FB 5).

Con `--landing` (y `--landing2`) agrega una sección **🔗 Enlaces con UTM** lista para pegar en bio/story/comentario: el mismo dominio con `?utm_source=instagram|tiktok|facebook&utm_medium=carrusel&utm_campaign=<slug>`, para medir de qué red llega el tráfico.

Incluye además un **📅 Plan de publicación sugerido** (días y franjas por red, republicación de story y repost de portada como reel) que podés ajustar según la analítica de tu cuenta.

## Brief interactivo (`brief.py`)

Alternativa a escribir el comando a mano: hace las 4 preguntas del brief (tipo → tema/color/slides → vertical → extras, incluida la landing y el repo) y arma/ejecuta el comando.

```bash
python3 ~/.config/opencode/skills/tech-carousel/brief.py            # interactivo
python3 ~/.config/opencode/skills/tech-carousel/brief.py --dry-run  # sólo imprime el comando
```

## Reglas de diseño (las aplica el builder)

- **Keywords por líneas:** 1 línea → EXACTAMENTE 1 `.clave`; 2-3 líneas → EXACTAMENTE 2. Medido en Chromium, nunca estimado. El matcher acepta `class='clave'` y `class="clave"` (`_RE_CLAVE`), no solo comillas dobles.
- **Color de keyword:** `--resalte`, y si no se pasa **usa el mismo `--color`** (`_colors.resuelve_resalte()`), para que todo el carrusel viva de un solo color. Un `--resalte` explícito siempre gana. El builder avisa si el contraste contra `#0B0B0D` no llega a 4.5:1 (nunca cambia el color solo).
- **Glow keyword:** `0 0 27px` con 32% de opacidad del `--resalte`.
- **Tamaño mínimo de texto:** cuerpo del slide `__body_size__` (44px) y componentes `__comp_base__` × `__comp_zoom__` ≥ 32px de diseño. Nunca achicar texto para que quepa: aligerá el shell (`ajustes` en `_format_scaling()`) o acortá el copy.
- **Píldora swipe:** padding 18px/32px, `min-height: __ind_h__px` (72 en 9:16, 56 en 4:5, 54 en 3:4, oculta en 1:1).
- **Tipografía:** display **Inter** (títulos/cuerpo) + mono **Hasklig → JetBrains Mono** (código/terminal). El `font-family` del mono siempre termina en `SFMono-Regular, Menlo, Consolas, monospace` para que funcione offline.
- **Fondo:** slides `#0B0B0D`, superficies `#141417`/`#1F2937`, bloques técnicos `#0F172A`, bordes `#26262B`/`#334155`.
- **Cielo estrellado:** cada slide (y la story) lleva una capa de 77 gradientes —viñeta de profundidad + 68 estrellas tenues + 8 brillantes— en `.slide::before`, **por debajo** del contenido (`z-index: 1`) y con coordenadas en `%`, así el mismo CSS sirve para 9:16, 3:4, 4:5 y 1:1. Determinista (`theme/stars.py`, semilla fija): mismo tema → mismas estrellas en todos los renders.
- **Accesibilidad:** contraste AA mínimo. Si `--resalte` contra `#0B0B0D` no llega a 4.5:1, el builder avisa.

## Errores comunes

| Síntoma | Causa / solución |
|---|---|
| `--slides N no coincide` | Hay N±x `slide-*.html`. Corregí la cantidad de archivos o el flag. |
| Ícono no se ve | XML inválido: cada elemento debe tener UN solo `stroke-width`. Validar con `python3 -m icons.registry --test`. |
| Set de íconos no esperado | El slug no matcheó keywords. Forzá `--iconos cybersec\|dev\|ai\|infra\|data\|common\|educativo\|tech`. |
| Componente no se expande | Falta `class="componente"` o `data-component`, o el JSON de `data-props` es inválido. |
| PNG en blanco | Se renderizó en loop. Usá el builder, no scripts propios. |
| Falta el pie | Falta `<div class="slide">` wrapper. |
| Chromium no existe | El builder busca en `PATH` y en `~/.cache/ms-playwright/chromium*`. Si no lo encuentra: `export CHROMIUM=/ruta/chromium`. |
| CTSLIDER no encontrado | `CTSLIDER_DIR=/ruta/a/CTSLIDER python3 ...` |
| Texto desbordado | Copy largo: acortá el `.cuerpo` o dividió el slide. |
| Texto de componente muy chico (≈16px) | `.comp-wrap` sin `font-size`: revisá `__comp_base__` en `theme/tokens.py` y que `_format_scaling()` lo setee (40 / 45 en 1:1). |
| `! slide-XX: Npx de contenido recortadas` | El lienzo es más corto que el contenido (casi siempre 4:5/3:4/1:1 con componente grande). Acortá copy, bajá `__comp_zoom__` de ese formato o aligerá su dict `ajustes` (`__pad_top__`, `__icon_size__`, `__title_margin__`) en `_format_scaling()`. |
| Color no reconocido | Hex `#RRGGBB` o nombre de paleta. |
| Keywords con otro color del esperado | El color de `.clave` lo decide `--resalte` (**default: el mismo `--color`**); el `#FFB800` del HTML fuente es sólo previsualización y el builder lo descarta. |
| Fondo sin estrellas / `__estrellas__` a la vista | Token sin reemplazar: pasá por `generar_html()`, nunca edites `renders/*.html` a mano. |
| Código no cabe | Más de 8 líneas visibles: dividió en 2 slides. |

## Regla de oro

Nunca edites los PNG ni los HTML de `renders/`. Corregí el **slide fuente** y volvé a ejecutar `tech_carousel.py`.

## Notas de producción

- **Entorno instalado (este equipo):** skill en `~/.config/opencode/skills/tech-carousel/` · carpeta de trabajo `/sdcard/CTSLIDER` · Pillow 12.3 (`pip3 --user`) · Chromium headless de Playwright (`chrome-headless-shell` aarch64 en `~/.cache/ms-playwright`, resuelto solo por `utils/render.py`) · `python3 -m pytest tests/` → 78 passed.
- **1 comando:** `tech_carousel.py` escribe el copy si falta, renderiza y verifica. `--copy-redes` agrega `copy-redes.md`; `--offline` evita Google Fonts; `--no-auto` exige slides hechos a mano.
- Copywriting también suelto con `generar_copy_tech.py` (paso 1 del pipeline).
- Ejemplos funcionales por vertical (fuentes + comando exacto) en `examples/`: `cybersec-sql-injection/`, `prog-python-testing/`, `ai-prompts/`.
- Íconos, badge, caption y hashtags se derivan del tema: solo necesitás tema + color HEX + slides.
- Marca default `CHMODX`; cambiála con `--marca` si el carrusel es para otro proyecto.
- Offline-friendly: fallbacks de tipografía y SVG sin filtros rasterizables en cualquier Chromium.
- Tests: `python3 -m pytest tests/` (78 casos: escalado por formato, proporción de font-size, keywords, props, color, CLI, fallback de GPU).
