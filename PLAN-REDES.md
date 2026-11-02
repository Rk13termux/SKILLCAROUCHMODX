# Plan — 3 versiones del carrusel por red (TikTok · Instagram · Facebook)

**Objetivo:** que un mismo tema produzca tres carruseles listos para publicar, cada
uno con su formato, su densidad de texto y su copy, **sin cambiar la lógica actual**.

**Regla dura:** lo que hoy funciona se queda igual. Sin `--redes`, el builder produce
exactamente la misma salida que hoy (mismos archivos, mismo HTML, mismos PNG).

## 0. Decisiones cerradas

| Decisión | Elección |
|---|---|
| Salida actual en la raíz | **Legacy intacta.** `renders/`, `preview/`, `stories/`, `caption.txt` y `copy-redes.md` se siguen escribiendo igual. Las 3 carpetas se **suman**. |
| Slides por red | **Recorte automático.** El perfil fija un máximo; si la fuente tiene más, el builder toma portada + contenido + cierre y **avisa qué slides quedaron afuera**. `--slides-<red>` lo fuerza. |


---

## 1. Estructura de carpetas (cómo queda)

```
$CTSLIDER/<slug>/
├── slide-01.html … slide-N.html     ← ÚNICA fuente de contenido (no se duplica)
├── story-fuente.html
├── caption.txt                       ← master (se mantiene, = Instagram)
├── copy-redes.md                     ← master comparativo (se mantiene)
├── renders/  preview/  stories/      ← salida legacy INTACTA (formato actual)
│
├── instagram/                        ← 4:5 · 1080×1350 · 8-10 slides
│   ├── renders/slide-NN.html
│   ├── preview/slide-NN.png
│   ├── stories/story-01.png
│   ├── caption.txt                   ← copy de IG (60-95 palabras, 9 hashtags)
│   ├── copy.md                        ← caption + primer comentario + UTM
│   └── perfil.json                    ← formato, slides, zona segura, hash fuente
│
├── tiktok/                           ← 9:16 · 1080×1920 · 6-8 slides
│   └── (misma estructura)
│
└── facebook/                         ← 4:5 · 1080×1350 · 5-6 slides
    └── (misma estructura)
```

Decisiones:

- **La fuente no se copia.** `slide-*.html` sigue siendo el único lugar donde se
  escribe el contenido. Las 3 carpetas son *salidas*, no fuentes.
- **La raíz sigue siendo válida.** Quien ya publica desde `preview/` no cambia nada.
- **`perfil.json` es la memoria de la versión**: guarda con qué perfil se generó y el
  hash de la fuente, para que `--incremental` sepa si hay que re-renderizar.

---

## 2. Perfiles por red (`redes.py`)

| | **TikTok** | **Instagram** | **Facebook** |
|---|---|---|---|
| Formato | `9:16` (1080×1920) | `4:5` (1080×1350) | `4:5` (1080×1350) |
| Slides | 6-8 | 8-10 | 5-6 |
| Cuerpo | 48px (+9%) | 44px (base) | 46px (+4%) |
| Palabras por slide | ≤25 | ≤45 | ≤45 |
| Copy (caption) | 30-50 palabras | 60-95 | 60-110 |
| Hashtags | 5 | 9 | 5 |
| CTA | seguir / serie | comentar palabra + guardar | link a landing |
| Zona segura | top 120 · bottom 250 · right 120 (UI de TikTok) | cuadrado central 1080×1080 (recorte de grilla) | margen 8% |
| Nota | Photo Mode, hasta 35 fotos; el gancho va en el slide 1 | Carrusel nativo | Multi-foto (no carrusel orgánico): se publican las imágenes en un post |

Por qué Facebook distinto: el carrusel como tal es formato publicitario; orgánico se
publica como **multi-foto**. Menos slides y CTA a link rinden mejor ahí. El plan lo
respeta en vez de fingir que es igual a Instagram.

---

## 3. Qué se toca en el código (mínimo)

| Archivo | Cambio |
|---|---|
| `redes.py` *(nuevo)* | `PERFILES`, `resolver_redes()`, `ajustes_por_red()` (formato + escala + límites) |
| `tech_carousel.py` | `--redes` y `--slides-<red>`; `final_dir` pasa de `input_dir/"renders"` a `base/"renders"` (4 sitios); bucle por red que reutiliza `generar_html()` sin cambios |
| `generar_copy_tech.py` | parte el bloque IG/TT/FB que ya calcula en `caption.txt` por red; el `copy-redes.md` global se mantiene |
| `tests/test_redes.py` *(nuevo)* | salida idéntica sin flag, perfiles, carpetas, presupuestos de copy |

**Lo que NO se toca:** `generar_html()`, auto-fit, `ajustar_titulo_portada()`,
keywords por líneas, arte/contraste, QA de ritmo y repetición, iconos, fondos.

El truco para no duplicar lógica: cada red es **una corrida del pipeline actual** con
un `fmt` y un `base` distintos. Nada más.

---

## 4. CLI

```bash
# como hoy (una salida en la raíz) — nada cambia
python3 tech_carousel.py --tema sql-injection --color "#06B6D4" --slides 10

# las tres versiones de una
python3 tech_carousel.py --tema sql-injection --color "#06B6D4" --slides 10 \
    --redes tiktok,instagram,facebook

# recortar slides por red (opcional)
python3 tech_carousel.py --tema sql-injection --redes todas \
    --slides-tiktok 6 --slides-facebook 5

# sólo el HTML de las tres, para iterar rápido
python3 tech_carousel.py --tema sql-injection --redes todas --solo-html
```

| Flag | Efecto |
|---|---|
| `--redes tiktok,instagram,facebook` / `todas` | genera las carpetas por red (la raíz se sigue generando igual) |
| `--slides-<red> N` | fuerza la cantidad de esa red; si no se pasa, el perfil recorta y avisa |
| `--solo-red <red>` | re-renderiza una sola (con `--incremental`) |
| `--check --redes todas` | valida los 3 perfiles sin renderizar |

Sin `--redes` **no se crea ninguna carpeta nueva**: garantía de compatibilidad.

---

## 5. Agentes nuevos

Los agentes viven en `~/.config/opencode/agents/`. Cada uno con un trabajo acotado y
salida verificable.

| Agente | Para qué | Entrada | Salida |
|---|---|---|---|
| **`carousel-logic`** | Busca dónde vive cada decisión del pipeline (formato, copy, QA, iconos, safe zones) y devuelve un mapa con archivo:línea. Se usa antes de tocar código. | Pregunta puntual ("¿dónde se decide el formato?") | Informe + grafo de dependencias |
| **`carousel-auditor`** | Corre `--check`, `pytest`, QA de ritmo/repetición, arte y contraste sobre las 3 versiones. | Carpeta del tema | Informe bloqueantes vs avisos |
| **`carousel-copy`** | Adapta el caption por red respetando presupuestos (30-50 / 60-95 / 60-110), dialecto neutro y hashtags exactos. | Tema + copy master | 3 captions + QA de palabras |
| **`carousel-analyst`** *(opcional, fase 4)* | Lee el CSV de métricas de cada red y propone qué formato/slide ajustar. | Export de IG/TT/FB | Recomendaciones priorizadas |

Flujo:

```
tema ──> carousel-logic ──> (mapa de lógica)
             │
             ▼
      builder --redes todas
             │
     ┌───────┼────────┐
     ▼       ▼        ▼
  tiktok  instagram facebook
     └───────┼────────┘
             ▼
      carousel-auditor  ──> ¿bloqueantes? ──> carousel-copy ──> publicar
```

---

## 6. Ramas (cómo queda el árbol git)

```
main
│
├── feat/redes-perfiles        ← redes.py + --redes (sin escribir carpetas todavía)
│      │
│      ├── feat/redes-carpetas ← base por red + perfil.json + incremental
│      │      │
│      │      ├── feat/redes-copy    ← caption.txt por red
│      │      │
│      │      └── feat/redes-agentes ← 3 agentes + docs
│      │
│      └── (merge a main al final de la fase 2)
```

| Rama | Alcance | Merge |
|---|---|---|
| `feat/redes-perfiles` | `redes.py`, flag, tests de perfiles. No escribe nada nuevo. | → `main` |
| `feat/redes-carpetas` | Carpetas `<slug>/<red>/`, `perfil.json`, incremental por red | → `main` |
| `feat/redes-copy` | `caption.txt`/`copy.md` por red + UTM por red | → `main` |
| `feat/redes-agentes` | Agentes `carousel-logic`, `carousel-auditor`, `carousel-copy` | → `main` |

Regla: **cada rama deja `main` verde** (169 tests + render de un tema real). Si una
rama rompe la salida legacy, no se mergea.

---

## 7. Fases y criterios de aceptación

| Fase | Qué entrega | Aceptación |
|---|---|---|
| **F1 · Perfiles** | `redes.py`, `--redes`, `--check` por perfil | Sin `--redes` el HTML generado es **byte a byte igual** al actual |
| **F2 · Carpetas** | `tema/<red>/{renders,preview,stories}` + `perfil.json` | 3 carpetas completas, `✓ Sin recortes` en las 3, `--incremental` reusa |
| **F3 · Copy** | `caption.txt` por red + `copy.md` + UTM por red | Presupuestos de palabras y hashtags exactos por red |
| **F4 · Agentes** | 3 `.md` + flujo documentado | `carousel-auditor` detecta un slide recortado a propósito |
| **F5 · Analítica** (opcional) | Ingesta de métricas y recomendaciones | Propone ≥1 acción concreta por red |

Estimación: F1 1 h · F2 2 h · F3 1 h · F4 1 h · F5 2 h.

---

## 8. Riesgos y cómo se cubren

| Riesgo | Mitigación |
|---|---|
| Duplicar PNG (3× disco) | `perfil.json` + `--incremental` por red; los PNG se pueden borrar y regenerar |
| Romper la salida actual | Test de regresión: hash del HTML legacy antes/después |
| Recorte de slides deja copy huérfano | El builder avisa qué slides quedaron fuera por red |
| TikTok tapa texto con su UI | Zona segura por perfil + revisión de arte extendida |
| Facebook no tiene carrusel orgánico | Documentado: se publica como multi-foto, con 5-6 imágenes |
| El copy se desincroniza entre redes | El master sigue en la raíz; las 3 copias se regeneran juntas |

---

## 9. Tests nuevos (`tests/test_redes.py`)

1. Sin `--redes`, los archivos generados son idénticos (hash).
2. `--redes todas` crea exactamente 3 carpetas con sus 3 subcarpetas.
3. Cada `perfil.json` declara el formato correcto (9:16 / 4:5 / 4:5).
4. `--slides-tiktok 6` genera 6 PNG y no toca las otras redes.
5. Los presupuestos de caption se respetan por red.
6. `--check --redes todas` no falla con un tema válido.

---

## 10. Estado

### F1 · Perfiles — hecho (rama `feat/redes-perfiles`)

| Entrega | Estado |
|---|---|
| `redes.py` con `PERFILES`, `resolver_redes()`, `seleccion()`, `planear()` | ✅ |
| CLI `--redes` + `--slides-tiktok/instagram/facebook` | ✅ |
| Validación temprana con error claro (`--redes myspace`) | ✅ |
| `--check --redes todas` imprime el plan sin renderizar | ✅ |
| `redes` aceptado en `--lote` | ✅ |
| `tests/test_redes.py` (13 casos) | ✅ 182 passed en total |

**Regresión verificada:** con el mismo comando y la misma fuente, el HTML generado
en esta rama es **idéntico byte a byte** al del commit anterior
(`diff -r` sobre los 10 `renders/*.html` → 0 líneas). Sin `--redes` no se escribe
ninguna carpeta nueva.

**Lo que F1 todavía NO hace (a propósito):** no escribe en `<tema>/<red>/`. El flag
valida el perfil y muestra el plan; la salida real es la de siempre.

### F2 · Carpetas — hecho (rama `feat/redes-perfiles`)

- `base = input_dir / <red>` cuando hay `--red-destino`: `renders/`, `preview/`,
  `stories/` y `caption.txt` se escriben en la carpeta de la red. La fuente
  (`slide-*.html`) se sigue leyendo del tema.
- **Recorte real:** `--recorte` remapea los slides fuente elegidos por `seleccion()`
  y **renumera** el badge (`1/8` en la versión de TikTok, no `3/10`).
- **`perfil.json`** por red: formato, slides, recorte, hash de la fuente, zona
  segura y presupuesto de copy.
- **Orquestador:** un subproceso por red con el mismo CLI (`--red-destino` y
  `--recorte` son internos). Cero lógica de render duplicada.
- QA de repetición/ritmo se corre una sola vez sobre la fuente (no por red).

**Regresión verificada:** sin `--redes`, el HTML sigue siendo **idéntico byte a byte**
al commit anterior (diff de los 10 `renders/*.html` → 0 líneas) y no se crea ninguna
carpeta nueva. `pytest`: 187 passed.

### F3 · Copy por red — hecho (rama `feat/redes-perfiles`)

- Cada red escribe su **`caption.txt`** con el texto de su plataforma (Instagram
  60-95 · TikTok 30-50 · Facebook 60-110) y **`copy.md`** con título, hashtags,
  primer comentario y el enlace con `utm_source=<red>`.
- `_primer_comentario()` ahora acepta `red=`, así el UTM del comentario fijado
  apunta a la red correcta (antes iba siempre a `instagram`).
- **Bug corregido:** la carpeta destino se llamaba `tiktok/`, así que
  `slug = carpeta.name` metía `#tiktok` en los hashtags y `utm_campaign=tiktok`.
  Ahora `generar_copy_redes(..., slug=tema_slug)` usa el slug real del tema.
- QA por red en el propio `copy.md` (palabras vs presupuesto, voseo, regionalismos,
  contenido responsable).
- `--copy-redes` sigue generando el `copy-redes.md` comparativo **solo en la raíz**;
  las carpetas de red ya traen su copy siempre.

**Verificación:** presupuestos 82 / 37 / 78 palabras (IG / TT / FB), hashtags
9 / 5 / 5, UTM distinto por red. `pytest`: 191 passed.

### F4 · Agentes — pendiente



