# Plan de rediseño visual de componentes — tech-carousel

**Objetivo:** que cada slide se vea como una pieza diseñada (no como una caja con borde),
y que el ritmo del carrusel sostenga la retención slide a slide.

**Alcance:** los 28 componentes + `theme/tokens.py` + `theme/colors.py`.
**No cambia:** contrato `data-component` / `data-props` (todo retrocompatible).

---

## 1. Diagnóstico (evidencia sobre renders reales)

Revisado sobre `/sdcard/CTSLIDER/python-termux/preview/slide-01/03/05.png`:

| # | Problema | Evidencia |
|---|---|---|
| 1 | **Componente y fondo son el mismo negro** → cero separación | `background: #000000` en cada componente vs `.slide { background: #000000 }`. El bloque solo se distingue por su borde de 2px. |
| 2 | **Un solo molde para los 28** | Todos: rectángulo + `border: 2px solid` + `#000000`. No hay jerarquía entre dato hero y nota secundaria. |
| 3 | **Sombras invisibles** | `box-shadow: 0 14px 34px rgba(0,0,0,.45)` sobre negro = 0 impacto visual. |
| 4 | **El acento no vende** | El color solo pinta bordes y títulos; las superficies no se tiñen. El carrusel pierde identidad cromática. |
| 5 | **La librería de 235 iconos no se usa dentro de componentes** | `card-info__ico` muestra un carácter (`i`, `✓`, `!`, `✕`) de `VARIANTES`. |
| 6 | **Conectores del diagrama son un glifo** | `diagram__flecha` = `↓` con `text-shadow`. No es un conector real. |
| 7 | **Gradiente muerto** | `.social { background: linear-gradient(160deg, #000000, #000000) }`. |
| 8 | **CSS huérfano** | `.alert` y `.timeline` (líneas 443-469 de `tokens.py`) no los usa ningún renderizador: son componentes fantasma. |
| 9 | **Jerarquía tipográfica plana** | Título de componente 1.16em vs cuerpo 0.98em: 18% de diferencia, se lee todo igual. |
| 10 | **Ritmo idéntico slide a slide** | icono → título → cuerpo → caja, siempre. Sin "premio visual" nuevo cada 2 slides, la retención cae. |

---

## 2. Sistema visual propuesto: **CHMODX Elevation**

### 2.1 Tokens nuevos (en `theme/colors.py`)

```python
SUPERFICIES = {
    "s1": "#0B0B10",   # superficie de componente
    "s2": "#121219",   # sub-panel / gutter / bloque anidado
    "s3": "#1A1A23",   # chip, badge, barra
    "line": "#24242E", # borde base
}
RADIOS = {"sm": 12, "md": 18, "lg": 24}
```

### 2.2 Variables CSS inyectadas por slide (`acento_vars`)

```css
--s1: #0B0B10; --s2: #121219; --s3: #1A1A23; --line: #24242E;
--line-acc: color-mix(in srgb, var(--acento) 55%, #24242E);
--edge: inset 0 1px 0 rgba(255,255,255,.06);
--shadow: 0 30px 60px -28px #000,
          0 10px 30px -18px color-mix(in srgb, var(--acento) 35%, transparent);
--glow: 0 0 44px -10px color-mix(in srgb, var(--acento) 45%, transparent);
--surf: linear-gradient(180deg,
          color-mix(in srgb, var(--acento) 7%, var(--s1)), var(--s1));
--rad-sm: 12px; --rad-md: 18px; --rad-lg: 24px;
```

### 2.3 Las 3 reglas que cambian todo

**R1 — Borde degradado (mayor impacto por línea de código).**
El borde deja de ser color plano y pasa a ser luz cayendo desde arriba-izquierda:

```css
.comp-base {
  border: 1.5px solid transparent;
  border-radius: var(--rad-md);
  background:
    var(--surf) padding-box,
    linear-gradient(145deg,
      color-mix(in srgb, var(--acento) 70%, transparent) 0%,
      color-mix(in srgb, var(--acento) 12%, #24242E) 45%,
      #24242E 100%) border-box;
  box-shadow: var(--shadow), var(--edge);
}
```

**R2 — Superficie con elevación real.**
Ningún componente vuelve a usar `#000000` como fondo. Piso: `var(--s1)`.
Los bloques anidados (gutter, panel interno, install) usan `var(--s2)`.

**R3 — Jerarquía tipográfica de 4 niveles.**

| Rol | Tamaño | Peso | Extra |
|---|---|---|---|
| hero (cifra grande) | 2.6em | 900 | gradiente de acento en el texto |
| título | 1.35em | 800 | `letter-spacing: -.01em` |
| cuerpo | 1em | 400 | `line-height 1.5` |
| label/eyebrow | 0.72em | 700 | mono, `uppercase`, `letter-spacing 2px`, acento |

---

## 3. Intervención por componente

### Wave 1 — los 6 que definen portada y cierre (80% del impacto)

| Componente | Qué cambia |
|---|---|
| `terminal` | Barra con dot "live" pulsante, prompt `$` en círculo de acento, output atenuado a `#8B93A1`, línea de comando con fondo `--s3` y borde izquierdo de acento, chip "copiar" en la barra. |
| `code` | Gutter con números sobre `--s2`, línea activa resaltada, header con `dot` del lenguaje + contador en pill, tipografía 0.92em, `code__note` como footer con borde superior degradado. |
| `editor` | Tabs reales (archivo activo con fondo `--s1`), barra de estado con dot verde y lenguaje mono, salida en panel `--s2` con label "OUTPUT". |
| `card-info` | **Icono SVG del registry** (no carácter) en placa duotono, eyebrow con variante (`INFO/TIP/WARN/DANGER`), barra lateral de acento convertida en degradado vertical. |
| `stats` | Tarjeta individual `--s2`, número hero 2.4em con `background-clip: text` en gradiente, label uppercase mono. Es el componente que más frena el scroll. |
| `card-compare` | Columna ganadora con ribbon "MEJOR" y borde acento; perdedora a 72% de opacidad. Badge VS como círculo central entre columnas. |

### Wave 2 — el resto (22)

`diagram`: conectores SVG con degradado + nodos numerados + glow en el nodo final.
`pasos`: número en placa cuadrada con degradado, rail vertical que conecta los pasos.
`tree`: guías continuas, íconos por tipo (ya existen), rama activa en acento con glow.
`http`: badge de método con glow, bloque request/response en `--s2` con label mono.
`browser`: barra con URL en pill `--s3`, sombra del marco, vista con padding real.
`diff`: gutter `−/+`, paneles rojo/verde translúcidos (no solo borde), label con ícono.
`tabla`: header sticky visual en `--s2`, filas alternadas, primera columna en acento.
`layers`: stack con profundidad (cada capa con sombra creciente) + separadores con chevron.
`pipeline`: rail horizontal conectando etapas, estado por color + dot animado en `run`.
`faq`: pregunta con `?` en placa, respuesta indentada con barra lateral.
`quiz`: opciones como botones `A/B/C/D`, la correcta con glow y check.
`quote`: comilla gigante como watermark, autor con avatar de inicial en círculo.
`checklist`: check en círculo relleno, ítems con separador sutil.
`mitos`: panel mito en rojo translúcido con label + ícono ✕, realidad en verde.
`card-repo`: barra tipo ventana, chips con dot, install con prompt en acento.
`gh-stats`: números grandes, barra de lenguajes con segmentos redondeados y glow.
`stack-tec`: chips con dot de color + borde degradado.
`error`: traceback con gutter de líneas, línea del error en rojo con fondo translúcido.
`timeline-fases`: rail con estado (✓/▶/✕) en placas de color.
`indice`: números en placa, ítem activo con barra de acento.
`qr`: tarjeta blanca con padding, marco de acento alrededor, pill "ESCANEA".
`social`: gradiente real (acento 10% → transparente), CTA con glow.

### Wave 3 — ritmo y composición (retención)

1. **Regla de familias alternas:** el builder avisa si dos slides consecutivos usan la misma familia (código / card / datos / flujo).
2. **Un hero por slide:** si hay `stats`, `quote` o `social`, el resto del slide baja a cuerpo (nada compite con la cifra).
3. **Tratamiento especial portada y cierre:** ya existe; se refuerza con superficie elevada y el componente en "modo showcase" (más padding, más glow).
4. **Variación de fondo por rol** ya existe (`--fondo`); se alinea la intensidad del componente con el rol (portada = glow, contenido = plano).

### Wave 4 — nuevos componentes (opcional, post-rediseño)

- `dato-hero`: cifra gigante + contexto de una línea (scroll-stopper puro).
- `split`: comparación visual partida con etiquetas.
- `progreso`: barra de avance + hitos.
- `fix`: error → solución en dos paneles con flecha.

---

## 4. Limpieza y guardarraíles

- **Eliminar** `.alert` y `.timeline` de `tokens.py` (CSS huérfano) o implementarlos de verdad.
- **Arreglar** el gradiente muerto de `.social`.
- **Mantener** auto-fit: las superficies no cambian el layout, solo padding/borde; el zoom sigue funcionando.
- **Contraste:** todo texto sobre `--s1` debe quedar ≥4.5:1 (validar con `avisar_contraste`).
- **Verificación:** `python3 -m pytest tests/` (78) + `--check` + render de los 3 carruseles de `examples/` + `contact-sheet.png` antes/después.

---

## 5. Orden de ejecución y criterio de aceptación

| Wave | Contenido | Esfuerzo | Aceptación |
|---|---|---|---|
| 0 | Tokens + R1/R2/R3 en `tokens.py` | 30-45 min | Los 28 componentes cambian de golpe sin tocar Python |
| 1 | 6 componentes clave | 1.5-2 h | Portada y cierre se ven "premium" en el contact-sheet |
| 2 | 22 restantes | 3-4 h | Ningún componente queda con el molde viejo |
| 3 | Ritmo + reglas del builder | 1 h | 2 slides consecutivos nunca comparten familia |
| 4 | Componentes nuevos | 2-3 h | `dato-hero` usable en carruseles de métricas |

**Criterio global:** en un contact-sheet de 8 slides, cada slide debe mostrar al menos
3 elementos visualmente diferenciados (superficie, acento, tipografía) y ninguno debe
tener el mismo peso visual que el anterior.

---

## 6. Estado de ejecución

### Hecho — Wave 0 (sistema)

- `tech_carousel.py`: vars `--s1/--s2/--s3/--linea`, `--surf`, `--surf-2`,
  `--borde-deg`, `--sombra`, `--sombra-edge`, `--glow`, radios.
- `theme/tokens.py`: bloque **ELEVATION** al final del CSS. Superficie + borde de luz
  en 24 selectores; paneles anidados un escalón más oscuros.
- `theme/fondos.py`: circuitos del fondo bajados de `0.45/0.70` a `0.26/0.42` de
  alpha (dejaban de competir con el contenido).
- `tech_carousel.py`: `--disable-dev-shm-usage` en Chromium (evita el crash
  `futex facility returned an unexpected error code` en contenedores).

### Hecho — Wave 1 (6 componentes)

| Componente | Cambio |
|---|---|
| `terminal` | Superficie + borde de luz, barra con eyebrow mono, prompt `$` en acento, línea de comando con fondo y barra izquierda de acento, salida atenuada, estados con peso. |
| `code` | Header con dot de acento + pill de líneas, gutter oscuro con números en negrita, cuerpo `--surf-2`, note como footer. |
| `editor` | Tab real (borde + fondo), pill de lenguaje con glow, salida en panel oscuro con label mono, status bar en degradado. |
| `card-info` | **Icono SVG del registry** (shield-alert / lightbulb / triangle-alert / info) en placa duotono, barra lateral en degradado, título 1.32em. |
| `stats` | Cifra 2.3em con gradiente en el texto + drop-shadow, tarjeta con hairline de acento arriba, label uppercase. |
| `card-compare` | Columna ganadora detectada por `ok:true` (clase `--win` + glow + ribbon "MEJOR"), perdedora al 90%, badges pill, marcas en círculo. |

**Verificación:** `pytest` 169 passed · `--check` OK · render 10 slides sin recortes ·
arte `✓ contraste mín 7.0:1`.

### Hecho — Wave 2 (22 componentes restantes)

Todos pasaron a superficie elevada + borde de luz + jerarquía mono:

`checklist` · `pasos` (rail entre pasos) · `diagram` (conectores SVG reales +
nodos numerados + variantes de color por tipo) · `tree` · `http` (badge de método
con glow, status pill) · `browser` · `diff` · `tabla` · `layers` (variantes de
borde por tipo) · `pipeline` (hairline de estado por etapa) · `faq` · `quiz`
(opciones tipo botón, correcta con glow) · `quote` (avatar con inicial) · `mitos`
(paneles tintados) · `repo` · `gh-stats` · `stack` · `error` (línea del error
resaltada) · `timeline` (placas de estado) · `índice` · `qr` · `social`.

**Bugs reales corregidos en el camino**

| Bug | Arreglo |
|---|---|
| El QR se dibujaba a ~30px dentro de una caja de 300px | `segno.svg_inline(..., omitsize=True)` + caja a 320px: ahora escala y es escaneable |
| `data-props` con apóstrofos (`&#39;`) se imprimía literal | `html.unescape()` antes de `json.loads()` en `components/base.py` |
| La flecha del diagrama era el glifo `↓` con `text-shadow` | Conector SVG real (`.diagram__conector`) + etiqueta opcional |
| `.social` tenía `linear-gradient(160deg, #000000, #000000)` | Gradiente real con tinte del acento + glow |
| `.quote` declaraba `border-left: 4px` y lo pisaba con `border: 2px` | Barra lateral por `::after` |

**Verificación:** `pytest` 169 passed · 3 carruseles QA (`_qa-a`, `_qa-b`, `_qa-c`,
28 componentes) sin recortes · contraste mínimo 7.0:1.

### Hecho — Wave 3 (ritmo y composición)

- **Píldora de swipe** (`.ind-swipe`): superficie con borde de luz, texto mono y la
  flecha dentro de un círculo de acento.
- **Card funnel** (`.guia-card`, slide 2): superficie elevada, tag en mono, barra
  lateral en degradado. Dejó de ser un bloque translúcido plano.
- **Showcase en portada**: el componente gancho del slide 1 va con `comp-wrap--showcase`
  (glow + borde más luminoso, mismo layout y mismo auto-fit).
- **QA de ritmo** (`qa_ritmo`): avisa de familias visuales repetidas en slides
  consecutivos, de slides con más de 2 componentes y de 2 bloques hero en el mismo
  slide. Es guía, no bloqueo.
- **Nodos del diagrama**: el número va sobre el borde superior, dentro de la tarjeta
  (antes se salía del margen en el recap N-1).

### Hecho — Wave 4 (componentes nuevos + limpieza)

**4 componentes nuevos (32 en total):**

| Componente | Alias | Uso |
|---|---|---|
| `dato-hero` | `hero`, `dato`, `cifra` | Una cifra gigante con gradiente + etiqueta + sub + fuente. El freno de scroll |
| `split` | `vs-panel`, `dos-paneles` | Dos paneles enfrentados con VS central (sin código) |
| `progreso` | `progress`, `avance` | Barra de avance 0-100 con hitos de estado |
| `fix` | `error-fix`, `solucion` | El error a la izquierda, el fix a la derecha |

- `components/nuevos.py` (renderizadores) + registro en `components/base.py` (+ 12 alias).
- CSS nuevo en `theme/tokens.py` (bloque WAVE 4).
- `dato-hero` entra como bloque *hero* en el QA de ritmo; `fix` en la familia `código`.

**Limpieza**

- Borrado el CSS huérfano: `.alert`, `.timeline`, `.network`, `.flow` (nunca tuvieron
  renderizador; llegaron a documentarse como componentes que no existían).
- `componentes-test/` reconstruido: los 27 PNG eran **el mismo archivo** (placeholder de
  8.7 KB). Ahora hay `componentes.png` (grilla 8×4 con los 32), `MANIFEST.json`,
  `regenerar.py` y `SLIDERS.md` generado desde el manifiesto.

**Verificación:** `pytest` 169 passed · catálogo renderizado sin recortes · contraste 7.0:1.

### Notas de deuda técnica

- El CSS quedó en tres capas (`base → ELEVATION → WAVE 2/4`). Las reglas viejas de los
  22 componentes siguen ahí y las nuevas las pisan por orden. Funciona y está testeado,
  pero consolidar cada bloque en uno solo es una tarea aparte (implica unificar
  propiedad por propiedad, no borrar a ciegas).
- `qa_ritmo` y `qa_repeticion` son avisos: no bloquean el render.




