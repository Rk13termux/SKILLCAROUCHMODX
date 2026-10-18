"""Overlay local de iconos — lo escribe `icon_smith.py agregar`.

Se mezcla SOBRE `lucide_sets.py`, así que los iconos que agregue el agente
NO se pierden al regenerar con `python3 -m icons.sync_lucide`.

Formato:
    SETS[<categoria>][<nombre>] = cuerpo SVG (estilo de la casa)
    ORDEN[<categoria>] = [nombres...]   # orden de rol sugerido
"""

SETS = {}
ORDEN = {}
