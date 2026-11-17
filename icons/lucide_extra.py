"""Overlay local de iconos — lo escribe `icon_smith.py agregar`.

Se mezcla SOBRE `lucide_sets.py`, así que los iconos que agregue el agente
NO se pierden al regenerar con `python3 -m icons.sync_lucide`.
"""

SETS = {
    "infra": {
        "folder":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z\" /></g>",
        "folder-tree":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M20 10a1 1 0 0 0 1-1V6a1 1 0 0 0-1-1h-2.5a1 1 0 0 1-.8-.4l-.9-1.2A1 1 0 0 0 15 3h-2a1 1 0 0 0-1 1v5a1 1 0 0 0 1 1Z\" /> <path d=\"M20 21a1 1 0 0 0 1-1v-3a1 1 0 0 0-1-1h-2.9a1 1 0 0 1-.88-.55l-.42-.85a1 1 0 0 0-.92-.6H13a1 1 0 0 0-1 1v5a1 1 0 0 0 1 1Z\" /> <path d=\"M3 5a2 2 0 0 0 2 2h3\" /> <path d=\"M3 3v13a2 2 0 0 0 2 2h3\" /></g>",
        "list-tree":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M8 5h13\" /> <path d=\"M13 12h8\" /> <path d=\"M13 19h8\" /> <path d=\"M3 10a2 2 0 0 0 2 2h3\" /> <path d=\"M3 5v12a2 2 0 0 0 2 2h3\" /></g>",
    },
}

ORDEN = {
    "infra": ['folder-tree', 'folder', 'list-tree'],
}
