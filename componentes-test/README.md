# Componentes — muestra visual

Referencia de los **32 componentes** del builder, renderizados con el diseño vigente.

| Archivo | Qué es |
|---|---|
| `componentes.png` | Grilla 8×4 con una miniatura por componente, etiquetada |
| `MANIFEST.json` | Props de muestra de cada componente (`["componente", {...}]`) |
| `regenerar.py` | Reconstruye todo: slides → render → grilla |

## Regenerar

```bash
cd ~/.config/opencode/skills/tech-carousel
python3 componentes-test/regenerar.py            # ~4 renders, deja componentes.png
python3 componentes-test/regenerar.py --solo-html # sólo arma los slides (debug)
```

Crea los temas `_catalogo-1..4` en `$CTSLIDER`, con **una portada fija** al inicio
(para que el builder no convierta el primer componente en hook) y los slides fijos
de resumen/cierre al final.

## Para agregar un componente

1. Sumá la entrada en `MANIFEST.json`.
2. Corré `regenerar.py`.
3. Si no aparece en la grilla, revisá que esté en `components/base.py`
   (`RENDERIZADORES`) y que tenga CSS en `theme/tokens.py`.
