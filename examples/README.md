# Ejemplos por vertical

Un ejemplo funcional por vertical. Cada carpeta contiene los `slide-*.html`
fuente (contrato HTML: `.numero`, `.slide`, `.contenido`, `.pie`,
`.componente[data-component][data-props]`) más el `story-fuente.html`.

Para regenerar el copy de un ejemplo (paso previo al render):

```bash
python3 generar_copy_tech.py --tema <slug> --slides <N> --vertical <v> --color "#RRGGBB" \
  [--display-tema "Título público"] [--short-tema "Tema corto"]
```

Para renderizar (Chromium headless, uno a la vez → `preview/*.png` + `caption.txt`):

```bash
python3 tech_carousel.py --tema <slug> --color "#RRGGBB" --slides <N> --vertical <v> \
  [--formato 9:16|4:5|3:4|1:1] [--marca TechEdu]
```

| Carpeta | Vertical | Slides | Comando exacto |
|---|---|---|---|
| `cybersec-sql-injection/` | cybersec | 8 | `python3 tech_carousel.py --tema sql-injection-api --color "#4F46E5" --slides 8 --vertical cybersec --short-tema "SQL injection" --display-tema "SQL injection en APIs REST"` |
| `prog-python-testing/` | prog | 7 | `python3 tech_carousel.py --tema python-testing --color "#10B981" --slides 7 --vertical prog --short-tema "Testing en Python" --display-tema "Testing en Python"` |
| `ai-prompts/` | ai | 7 | `python3 tech_carousel.py --tema prompt-ia --color "#F59E0B" --slides 7 --vertical ai --short-tema "Prompts IA" --display-tema "Prompts que funcionan"` |

Salida esperada en `/mnt/sdcard/CTSLIDER/<slug>/`:

```
slide-01..N.html   # fuente
renders/           # HTML final con componentes expandidos + CSS inline
preview/           # PNG 1080×1920 (9:16 por defecto)
stories/story-01.png
caption.txt        # copy de redes listo (con hashtags y CTA)
```

Para copiar un ejemplo a la carpeta de trabajo:

```bash
cp examples/cybersec-sql-injection/*.html /mnt/sdcard/CTSLIDER/sql-injection-api/
```
