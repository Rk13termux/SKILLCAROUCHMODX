"""Iconos Lucide normalizados al estilo de la casa (generado).

Fuente: lucide-static 1.59.0 · licencia ISC · https://lucide.dev
NO editar a mano: regenerar con `python3 -m icons.sync_lucide`.
"""

VERSION = "1.59.0"

SETS = {
    "cybersec": {
        "shield-alert":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z\" /> <path d=\"M12 8v4\" /> <path d=\"M12 16h.01\" /></g>",
        "lock-keyhole":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><circle cx=\"12\" cy=\"16\" r=\"1\" /> <rect x=\"3\" y=\"10\" width=\"18\" height=\"12\" rx=\"2\" /> <path d=\"M7 10V7a5 5 0 0 1 10 0v3\" /></g>",
        "fingerprint":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M12 10a2 2 0 0 0-2 2c0 1.02-.1 2.51-.26 4\" /> <path d=\"M14 13.12c0 2.38 0 6.38-1 8.88\" /> <path d=\"M17.29 21.02c.12-.6.43-2.3.5-3.02\" /> <path d=\"M2 12a10 10 0 0 1 18-6\" /> <path d=\"M2 16h.01\" /> <path d=\"M21.8 16c.2-2 .131-5.354 0-6\" /> <path d=\"M5 19.5C5.5 18 6 15 6 12a6 6 0 0 1 .34-2\" /> <path d=\"M8.65 22c.21-.66.45-1.32.57-2\" /> <path d=\"M9 6.8a6 6 0 0 1 9 5.2v2\" /></g>",
        "scan-face":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M3 7V5a2 2 0 0 1 2-2h2\" /> <path d=\"M17 3h2a2 2 0 0 1 2 2v2\" /> <path d=\"M21 17v2a2 2 0 0 1-2 2h-2\" /> <path d=\"M7 21H5a2 2 0 0 1-2-2v-2\" /> <path d=\"M8 14s1.5 2 4 2 4-2 4-2\" /> <path d=\"M9 9h.01\" /> <path d=\"M15 9h.01\" /></g>",
        "crosshair":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><circle cx=\"12\" cy=\"12\" r=\"10\" /> <line x1=\"22\" x2=\"18\" y1=\"12\" y2=\"12\" /> <line x1=\"6\" x2=\"2\" y1=\"12\" y2=\"12\" /> <line x1=\"12\" x2=\"12\" y1=\"6\" y2=\"2\" /> <line x1=\"12\" x2=\"12\" y1=\"22\" y2=\"18\" /></g>",
        "siren":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M7 18v-6a5 5 0 1 1 10 0v6\" /> <path d=\"M5 21a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-1a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2z\" /> <path d=\"M21 12h1\" /> <path d=\"M18.5 4.5 18 5\" /> <path d=\"M2 12h1\" /> <path d=\"M12 2v1\" /> <path d=\"m4.929 4.929.707.707\" /> <path d=\"M12 12v6\" /></g>",
        "triangle-alert":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3\" /> <path d=\"M12 9v4\" /> <path d=\"M12 17h.01\" /></g>",
        "user-x":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2\" /> <circle cx=\"9\" cy=\"7\" r=\"4\" /> <line x1=\"17\" x2=\"22\" y1=\"8\" y2=\"13\" /> <line x1=\"22\" x2=\"17\" y1=\"8\" y2=\"13\" /></g>",
        "badge-check":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z\" /> <path d=\"m16 9-5.5 5.5L8 12\" /></g>",
        "shield-off":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"m2 2 20 20\" /> <path d=\"M5 5a1 1 0 0 0-1 1v7c0 5 3.5 7.5 7.67 8.94a1 1 0 0 0 .67.01c2.35-.82 4.48-1.97 5.9-3.71\" /> <path d=\"M9.309 3.652A12.252 12.252 0 0 0 11.24 2.28a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1v7a9.784 9.784 0 0 1-.08 1.264\" /></g>",
        "key-round":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M2.586 17.414A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586l.814-.814a6.5 6.5 0 1 0-4-4z\" /> <circle cx=\"16.5\" cy=\"7.5\" r=\".5\" fill=\"url(#c)\" /></g>",
        "bug-off":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M12 20v-8\" /> <path d=\"M12.656 7H14a4 4 0 0 1 4 4v1.344\" /> <path d=\"M14.12 3.88 16 2\" /> <path d=\"M17.123 17.123A6 6 0 0 1 6 14v-3a4 4 0 0 1 1.72-3.287\" /> <path d=\"m2 2 20 20\" /> <path d=\"M21 5a4 4 0 0 1-3.55 3.97\" /> <path d=\"M22 13h-3.344\" /> <path d=\"M3 21a4 4 0 0 1 3.81-4\" /> <path d=\"M3 5a4 4 0 0 0 3.55 3.97\" /> <path d=\"M6 13H2\" /> <path d=\"m8 2 1.88 1.88\" /> <path d=\"M9.712 4.06A3 3 0 0 1 15 6v1.13\" /></g>",
        "door-closed":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16\" /> <path d=\"M2 21h20\" /> <path d=\"M9 12h.01\" /></g>",
        "mail-warning":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M22 10.5V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v12c0 1.1.9 2 2 2h12.5\" /> <path d=\"m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7\" /> <path d=\"M20 14v4\" /> <path d=\"M20 22v.01\" /></g>",
        "link-2-off":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M9 17H7A5 5 0 0 1 7 7\" /> <path d=\"M15 7h2a5 5 0 0 1 4 8\" /> <line x1=\"8\" x2=\"12\" y1=\"12\" y2=\"12\" /> <line x1=\"2\" x2=\"22\" y1=\"2\" y2=\"22\" /></g>",
        "biohazard":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><circle cx=\"12\" cy=\"11.9\" r=\"2\" /> <path d=\"M6.7 3.4c-.9 2.5 0 5.2 2.2 6.7C6.5 9 3.7 9.6 2 11.6\" /> <path d=\"m8.9 10.1 1.4.8\" /> <path d=\"M17.3 3.4c.9 2.5 0 5.2-2.2 6.7 2.4-1.2 5.2-.6 6.9 1.5\" /> <path d=\"m15.1 10.1-1.4.8\" /> <path d=\"M16.7 20.8c-2.6-.4-4.6-2.6-4.7-5.3-.2 2.6-2.1 4.8-4.7 5.2\" /> <path d=\"M12 13.9v1.6\" /> <path d=\"M13.5 5.4c-1-.2-2-.2-3 0\" /> <path d=\"M17 16.4c.7-.7 1.2-1.6 1.5-2.5\" /> <path d=\"M5.5 13.9c.3.9.8 1.8 1.5 2.5\" /></g>",
        "skull":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"m12.5 17-.5-1-.5 1h1z\" /> <path d=\"M15 22a1 1 0 0 0 1-1v-1a2 2 0 0 0 1.56-3.25 8 8 0 1 0-11.12 0A2 2 0 0 0 8 20v1a1 1 0 0 0 1 1z\" /> <circle cx=\"15\" cy=\"12\" r=\"1\" /> <circle cx=\"9\" cy=\"12\" r=\"1\" /></g>",
        "scan-line":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M3 7V5a2 2 0 0 1 2-2h2\" /> <path d=\"M17 3h2a2 2 0 0 1 2 2v2\" /> <path d=\"M21 17v2a2 2 0 0 1-2 2h-2\" /> <path d=\"M7 21H5a2 2 0 0 1-2-2v-2\" /> <path d=\"M7 12h10\" /></g>",
        "shield-plus":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z\" /> <path d=\"M9 12h6\" /> <path d=\"M12 9v6\" /></g>",
        "file-lock":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M4 9.8V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.706.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2h-3\" /> <path d=\"M14 2v5a1 1 0 0 0 1 1h5\" /> <path d=\"M9 17v-2a2 2 0 0 0-4 0v2\" /> <rect width=\"8\" height=\"5\" x=\"3\" y=\"17\" rx=\"1\" /></g>",
        "user-check":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"m16 11 2 2 4-4\" /> <path d=\"M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2\" /> <circle cx=\"9\" cy=\"7\" r=\"4\" /></g>",
        "alert-octagon":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M12 16h.01\" /> <path d=\"M12 8v4\" /> <path d=\"M15.312 2a2 2 0 0 1 1.414.586l4.688 4.688A2 2 0 0 1 22 8.688v6.624a2 2 0 0 1-.586 1.414l-4.688 4.688a2 2 0 0 1-1.414.586H8.688a2 2 0 0 1-1.414-.586l-4.688-4.688A2 2 0 0 1 2 15.312V8.688a2 2 0 0 1 .586-1.414l4.688-4.688A2 2 0 0 1 8.688 2z\" /></g>",
        "shield-ban":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z\" /> <path d=\"m4.243 5.21 14.39 12.472\" /></g>",
        "venetian-mask":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M18 11c-1.5 0-2.5.5-3 2\" /> <path d=\"M4 6a2 2 0 0 0-2 2v4a5 5 0 0 0 5 5 8 8 0 0 1 5 2 8 8 0 0 1 5-2 5 5 0 0 0 5-5V8a2 2 0 0 0-2-2h-3a8 8 0 0 0-5 2 8 8 0 0 0-5-2z\" /> <path d=\"M6 11c1.5 0 2.5.5 3 2\" /></g>",
        "footprints":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M4 16v-2.38C4 11.5 2.97 10.5 3 8c.03-2.72 1.49-6 4.5-6C9.37 2 10 3.8 10 5.5c0 3.11-2 5.66-2 8.68V16a2 2 0 1 1-4 0Z\" /> <path d=\"M20 20v-2.38c0-2.12 1.03-3.12 1-5.62-.03-2.72-1.49-6-4.5-6C14.63 6 14 7.8 14 9.5c0 3.11 2 5.66 2 8.68V20a2 2 0 1 0 4 0Z\" /> <path d=\"M16 17h4\" /> <path d=\"M4 13h4\" /></g>",
        "key-square":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M12.4 2.7a2.5 2.5 0 0 1 3.4 0l5.5 5.5a2.5 2.5 0 0 1 0 3.4l-3.7 3.7a2.5 2.5 0 0 1-3.4 0L8.7 9.8a2.5 2.5 0 0 1 0-3.4z\" /> <path d=\"m14 7 3 3\" /> <path d=\"m9.4 10.6-6.814 6.814A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586l.814-.814\" /></g>",
        "shield-question":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z\" /> <path d=\"M9.1 9a3 3 0 0 1 5.82 1c0 2-3 3-3 3\" /> <path d=\"M12 17h.01\" /></g>",
        "file-warning":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z\" /> <path d=\"M12 9v4\" /> <path d=\"M12 17h.01\" /></g>",
    },
    "dev": {
        "terminal":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M12 19h8\" /> <path d=\"m4 17 6-6-6-6\" /></g>",
        "git-branch":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M15 6a9 9 0 0 0-9 9V3\" /> <circle cx=\"18\" cy=\"6\" r=\"3\" /> <circle cx=\"6\" cy=\"18\" r=\"3\" /></g>",
        "code-xml":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"m18 16 4-4-4-4\" /> <path d=\"m6 8-4 4 4 4\" /> <path d=\"m14.5 4-5 16\" /></g>",
        "braces":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M8 3H7a2 2 0 0 0-2 2v5a2 2 0 0 1-2 2 2 2 0 0 1 2 2v5c0 1.1.9 2 2 2h1\" /> <path d=\"M16 21h1a2 2 0 0 0 2-2v-5c0-1.1.9-2 2-2a2 2 0 0 1-2-2V5a2 2 0 0 0-2-2h-1\" /></g>",
        "package":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M11 21.73a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73z\" /> <path d=\"M12 22V12\" /> <polyline points=\"3.29 7 12 12 20.71 7\" /> <path d=\"m7.5 4.27 9 5.15\" /></g>",
        "workflow":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><rect width=\"8\" height=\"8\" x=\"3\" y=\"3\" rx=\"2\" /> <path d=\"M7 11v4a2 2 0 0 0 2 2h4\" /> <rect width=\"8\" height=\"8\" x=\"13\" y=\"13\" rx=\"2\" /></g>",
        "test-tube":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M14.5 2v17.5c0 1.4-1.1 2.5-2.5 2.5c-1.4 0-2.5-1.1-2.5-2.5V2\" /> <path d=\"M8.5 2h7\" /> <path d=\"M14.5 16h-5\" /></g>",
        "binary":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><rect x=\"14\" y=\"14\" width=\"4\" height=\"6\" rx=\"2\" /> <rect x=\"6\" y=\"4\" width=\"4\" height=\"6\" rx=\"2\" /> <path d=\"M6 20h4\" /> <path d=\"M14 10h4\" /> <path d=\"M6 14h2v6\" /> <path d=\"M14 4h2v6\" /></g>",
        "regex":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M17 3v10\" /> <path d=\"m12.67 5.5 8.66 5\" /> <path d=\"m12.67 10.5 8.66-5\" /> <path d=\"M9 17a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v2a2 2 0 0 0 2 2h2a2 2 0 0 0 2-2v-2z\" /></g>",
        "component":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M15.536 11.293a1 1 0 0 0 0 1.414l2.376 2.377a1 1 0 0 0 1.414 0l2.377-2.377a1 1 0 0 0 0-1.414l-2.377-2.377a1 1 0 0 0-1.414 0z\" /> <path d=\"M2.297 11.293a1 1 0 0 0 0 1.414l2.377 2.377a1 1 0 0 0 1.414 0l2.377-2.377a1 1 0 0 0 0-1.414L6.088 8.916a1 1 0 0 0-1.414 0z\" /> <path d=\"M8.916 17.912a1 1 0 0 0 0 1.415l2.377 2.376a1 1 0 0 0 1.414 0l2.377-2.376a1 1 0 0 0 0-1.415l-2.377-2.376a1 1 0 0 0-1.414 0z\" /> <path d=\"M8.916 4.674a1 1 0 0 0 0 1.414l2.377 2.376a1 1 0 0 0 1.414 0l2.377-2.376a1 1 0 0 0 0-1.414l-2.377-2.377a1 1 0 0 0-1.414 0z\" /></g>",
        "database":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><ellipse cx=\"12\" cy=\"5\" rx=\"9\" ry=\"3\" /> <path d=\"M3 5V19A9 3 0 0 0 21 19V5\" /> <path d=\"M3 12A9 3 0 0 0 21 12\" /></g>",
        "cpu":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M12 20v2\" /> <path d=\"M12 2v2\" /> <path d=\"M17 20v2\" /> <path d=\"M17 2v2\" /> <path d=\"M2 12h2\" /> <path d=\"M2 17h2\" /> <path d=\"M2 7h2\" /> <path d=\"M20 12h2\" /> <path d=\"M20 17h2\" /> <path d=\"M20 7h2\" /> <path d=\"M7 20v2\" /> <path d=\"M7 2v2\" /> <rect x=\"4\" y=\"4\" width=\"16\" height=\"16\" rx=\"2\" /> <rect x=\"8\" y=\"8\" width=\"8\" height=\"8\" rx=\"1\" /></g>",
        "refresh-cw":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8\" /> <path d=\"M21 3v5h-5\" /> <path d=\"M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16\" /> <path d=\"M8 16H3v5\" /></g>",
        "square-function":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><rect width=\"18\" height=\"18\" x=\"3\" y=\"3\" rx=\"2\" ry=\"2\" /> <path d=\"M9 17c2 0 2.8-1 2.8-2.8V10c0-2 1-3.3 3.2-3\" /> <path d=\"M9 11.2h5.7\" /></g>",
        "file-code":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z\" /> <path d=\"M14 2v5a1 1 0 0 0 1 1h5\" /> <path d=\"M10 12.5 8 15l2 2.5\" /> <path d=\"m14 12.5 2 2.5-2 2.5\" /></g>",
        "boxes":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M2.97 12.92A2 2 0 0 0 2 14.63v3.24a2 2 0 0 0 .97 1.71l3 1.8a2 2 0 0 0 2.06 0L12 19v-5.5l-5-3-4.03 2.42Z\" /> <path d=\"m7 16.5-4.74-2.85\" /> <path d=\"m7 16.5 5-3\" /> <path d=\"M7 16.5v5.17\" /> <path d=\"M12 13.5V19l3.97 2.38a2 2 0 0 0 2.06 0l3-1.8a2 2 0 0 0 .97-1.71v-3.24a2 2 0 0 0-.97-1.71L17 10.5l-5 3Z\" /> <path d=\"m17 16.5-5-3\" /> <path d=\"m17 16.5 4.74-2.85\" /> <path d=\"M17 16.5v5.17\" /> <path d=\"M7.97 4.42A2 2 0 0 0 7 6.13v4.37l5 3 5-3V6.13a2 2 0 0 0-.97-1.71l-3-1.8a2 2 0 0 0-2.06 0l-3 1.8Z\" /> <path d=\"M12 8 7.26 5.15\" /> <path d=\"m12 8 4.74-2.85\" /> <path d=\"M12 13.5V8\" /></g>",
        "flask-conical":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M14 2v6a2 2 0 0 0 .245.96l5.51 10.08A2 2 0 0 1 18 22H6a2 2 0 0 1-1.755-2.96l5.51-10.08A2 2 0 0 0 10 8V2\" /> <path d=\"M6.453 15h11.094\" /> <path d=\"M8.5 2h7\" /></g>",
        "wrench":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.106-3.105c.32-.322.863-.22.983.218a6 6 0 0 1-8.259 7.057l-7.91 7.91a1 1 0 0 1-2.999-3l7.91-7.91a6 6 0 0 1 7.057-8.259c.438.12.54.662.219.984z\" /></g>",
        "cog":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M11 10.27 7 3.34\" /> <path d=\"m11 13.73-4 6.93\" /> <path d=\"M12 22v-2\" /> <path d=\"M12 2v2\" /> <path d=\"M14 12h8\" /> <path d=\"m17 20.66-1-1.73\" /> <path d=\"m17 3.34-1 1.73\" /> <path d=\"M2 12h2\" /> <path d=\"m20.66 17-1.73-1\" /> <path d=\"m20.66 7-1.73 1\" /> <path d=\"m3.34 17 1.73-1\" /> <path d=\"m3.34 7 1.73 1\" /> <circle cx=\"12\" cy=\"12\" r=\"2\" /> <circle cx=\"12\" cy=\"12\" r=\"8\" /></g>",
        "variable":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M8 21s-4-3-4-9 4-9 4-9\" /> <path d=\"M16 3s4 3 4 9-4 9-4 9\" /> <line x1=\"15\" x2=\"9\" y1=\"9\" y2=\"15\" /> <line x1=\"9\" x2=\"15\" y1=\"9\" y2=\"15\" /></g>",
        "git-merge":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><circle cx=\"18\" cy=\"18\" r=\"3\" /> <circle cx=\"6\" cy=\"6\" r=\"3\" /> <path d=\"M6 21V9a9 9 0 0 0 9 9\" /></g>",
        "git-pull-request":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><circle cx=\"18\" cy=\"18\" r=\"3\" /> <circle cx=\"6\" cy=\"6\" r=\"3\" /> <path d=\"M13 6h3a2 2 0 0 1 2 2v7\" /> <line x1=\"6\" x2=\"6\" y1=\"9\" y2=\"21\" /></g>",
        "git-fork":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><circle cx=\"12\" cy=\"18\" r=\"3\" /> <circle cx=\"6\" cy=\"6\" r=\"3\" /> <circle cx=\"18\" cy=\"6\" r=\"3\" /> <path d=\"M18 9v2c0 .6-.4 1-1 1H7c-.6 0-1-.4-1-1V9\" /> <path d=\"M12 12v3\" /></g>",
        "repeat":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"m17 2 4 4-4 4\" /> <path d=\"M3 11v-1a4 4 0 0 1 4-4h14\" /> <path d=\"m7 22-4-4 4-4\" /> <path d=\"M21 13v1a4 4 0 0 1-4 4H3\" /></g>",
        "play":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M5 5a2 2 0 0 1 3.008-1.728l11.997 6.998a2 2 0 0 1 .003 3.458l-12 7A2 2 0 0 1 5 19z\" /></g>",
        "power":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M12 2v10\" /> <path d=\"M18.4 6.6a9 9 0 1 1-12.77.04\" /></g>",
        "blocks":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M10 22V7a1 1 0 0 0-1-1H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-5a1 1 0 0 0-1-1H2\" /> <rect x=\"14\" y=\"2\" width=\"8\" height=\"8\" rx=\"1\" /></g>",
        "puzzle":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M15.39 4.39a1 1 0 0 0 1.68-.474 2.5 2.5 0 1 1 3.014 3.015 1 1 0 0 0-.474 1.68l1.683 1.682a2.414 2.414 0 0 1 0 3.414L19.61 15.39a1 1 0 0 1-1.68-.474 2.5 2.5 0 1 0-3.014 3.015 1 1 0 0 1 .474 1.68l-1.683 1.682a2.414 2.414 0 0 1-3.414 0L8.61 19.61a1 1 0 0 0-1.68.474 2.5 2.5 0 1 1-3.014-3.015 1 1 0 0 0 .474-1.68l-1.683-1.682a2.414 2.414 0 0 1 0-3.414L4.39 8.61a1 1 0 0 1 1.68.474 2.5 2.5 0 1 0 3.014-3.015 1 1 0 0 1-.474-1.68l1.683-1.682a2.414 2.414 0 0 1 3.414 0z\" /></g>",
        "keyboard":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M10 8h.01\" /> <path d=\"M12 12h.01\" /> <path d=\"M14 8h.01\" /> <path d=\"M16 12h.01\" /> <path d=\"M18 8h.01\" /> <path d=\"M6 8h.01\" /> <path d=\"M7 16h10\" /> <path d=\"M8 12h.01\" /> <rect width=\"20\" height=\"16\" x=\"2\" y=\"4\" rx=\"2\" /></g>",
        "monitor-cog":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M12 17v4\" /> <path d=\"m14.305 7.53.923-.382\" /> <path d=\"m15.228 4.852-.923-.383\" /> <path d=\"m16.852 3.228-.383-.924\" /> <path d=\"m16.852 8.772-.383.923\" /> <path d=\"m19.148 3.228.383-.924\" /> <path d=\"m19.53 9.696-.382-.924\" /> <path d=\"m20.772 4.852.924-.383\" /> <path d=\"m20.772 7.148.924.383\" /> <path d=\"M22 13v2a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h7\" /> <path d=\"M8 21h8\" /> <circle cx=\"18\" cy=\"6\" r=\"3\" /></g>",
        "table":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M12 3v18\" /> <rect width=\"18\" height=\"18\" x=\"3\" y=\"3\" rx=\"2\" /> <path d=\"M3 9h18\" /> <path d=\"M3 15h18\" /></g>",
        "grid-3x3":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><rect width=\"18\" height=\"18\" x=\"3\" y=\"3\" rx=\"2\" /> <path d=\"M3 9h18\" /> <path d=\"M3 15h18\" /> <path d=\"M9 3v18\" /> <path d=\"M15 3v18\" /></g>",
        "layers":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83z\" /> <path d=\"M2 12a1 1 0 0 0 .58.91l8.6 3.91a2 2 0 0 0 1.65 0l8.58-3.9A1 1 0 0 0 22 12\" /> <path d=\"M2 17a1 1 0 0 0 .58.91l8.6 3.91a2 2 0 0 0 1.65 0l8.58-3.9A1 1 0 0 0 22 17\" /></g>",
        "file-terminal":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z\" /> <path d=\"M14 2v5a1 1 0 0 0 1 1h5\" /> <path d=\"m8 16 2-2-2-2\" /> <path d=\"M12 18h4\" /></g>",
        "list-checks":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M13 5h8\" /> <path d=\"M13 12h8\" /> <path d=\"M13 19h8\" /> <path d=\"m3 17 2 2 4-4\" /> <path d=\"m3 7 2 2 4-4\" /></g>",
        "mouse-pointer-click":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M14 4.1 12 6\" /> <path d=\"m5.1 8-2.9-.8\" /> <path d=\"m6 12-1.9 2\" /> <path d=\"M7.2 2.2 8 5.1\" /> <path d=\"M9.037 9.69a.498.498 0 0 1 .653-.653l11 4.5a.5.5 0 0 1-.074.949l-4.349 1.041a1 1 0 0 0-.74.739l-1.04 4.35a.5.5 0 0 1-.95.074z\" /></g>",
    },
    "ai": {
        "brain-circuit":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z\" /> <path d=\"M9 13a4.5 4.5 0 0 0 3-4\" /> <path d=\"M6.003 5.125A3 3 0 0 0 6.401 6.5\" /> <path d=\"M3.477 10.896a4 4 0 0 1 .585-.396\" /> <path d=\"M6 18a4 4 0 0 1-1.967-.516\" /> <path d=\"M12 13h4\" /> <path d=\"M12 18h6a2 2 0 0 1 2 2v1\" /> <path d=\"M12 8h8\" /> <path d=\"M16 8V5a2 2 0 0 1 2-2\" /> <circle cx=\"16\" cy=\"13\" r=\".5\" /> <circle cx=\"18\" cy=\"3\" r=\".5\" /> <circle cx=\"20\" cy=\"21\" r=\".5\" /> <circle cx=\"20\" cy=\"8\" r=\".5\" /></g>",
        "sparkles":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M11.017 2.814a1 1 0 0 1 1.966 0l1.051 5.558a2 2 0 0 0 1.594 1.594l5.558 1.051a1 1 0 0 1 0 1.966l-5.558 1.051a2 2 0 0 0-1.594 1.594l-1.051 5.558a1 1 0 0 1-1.966 0l-1.051-5.558a2 2 0 0 0-1.594-1.594l-5.558-1.051a1 1 0 0 1 0-1.966l5.558-1.051a2 2 0 0 0 1.594-1.594z\" /> <path d=\"M20 2v4\" /> <path d=\"M22 4h-4\" /> <circle cx=\"4\" cy=\"20\" r=\"2\" /></g>",
        "bot":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M12 8V4H8\" /> <rect width=\"16\" height=\"12\" x=\"4\" y=\"8\" rx=\"2\" /> <path d=\"M2 14h2\" /> <path d=\"M20 14h2\" /> <path d=\"M15 13v2\" /> <path d=\"M9 13v2\" /></g>",
        "network":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><rect x=\"16\" y=\"16\" width=\"6\" height=\"6\" rx=\"1\" /> <rect x=\"2\" y=\"16\" width=\"6\" height=\"6\" rx=\"1\" /> <rect x=\"9\" y=\"2\" width=\"6\" height=\"6\" rx=\"1\" /> <path d=\"M5 16v-3a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3\" /> <path d=\"M12 12V8\" /></g>",
        "wand-sparkles":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"m21.64 3.64-1.28-1.28a1.21 1.21 0 0 0-1.72 0L2.36 18.64a1.21 1.21 0 0 0 0 1.72l1.28 1.28a1.2 1.2 0 0 0 1.72 0L21.64 5.36a1.2 1.2 0 0 0 0-1.72\" /> <path d=\"m14 7 3 3\" /> <path d=\"M5 6v4\" /> <path d=\"M19 14v4\" /> <path d=\"M10 2v2\" /> <path d=\"M7 8H3\" /> <path d=\"M21 16h-4\" /> <path d=\"M11 3H9\" /></g>",
        "brain-cog":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"m10.852 14.772-.383.923\" /> <path d=\"m10.852 9.228-.383-.923\" /> <path d=\"m13.148 14.772.382.924\" /> <path d=\"m13.531 8.305-.383.923\" /> <path d=\"m14.772 10.852.923-.383\" /> <path d=\"m14.772 13.148.923.383\" /> <path d=\"M17.598 6.5A3 3 0 1 0 12 5a3 3 0 0 0-5.63-1.446 3 3 0 0 0-.368 1.571 4 4 0 0 0-2.525 5.771\" /> <path d=\"M17.998 5.125a4 4 0 0 1 2.525 5.771\" /> <path d=\"M19.505 10.294a4 4 0 0 1-1.5 7.706\" /> <path d=\"M4.032 17.483A4 4 0 0 0 11.464 20c.18-.311.892-.311 1.072 0a4 4 0 0 0 7.432-2.516\" /> <path d=\"M4.5 10.291A4 4 0 0 0 6 18\" /> <path d=\"M6.002 5.125a3 3 0 0 0 .4 1.375\" /> <path d=\"m9.228 10.852-.923-.383\" /> <path d=\"m9.228 13.148-.923.383\" /> <circle cx=\"12\" cy=\"12\" r=\"3\" /></g>",
        "atom":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><circle cx=\"12\" cy=\"12\" r=\"1\" /> <path d=\"M20.2 20.2c2.04-2.03.02-7.36-4.5-11.9-4.54-4.52-9.87-6.54-11.9-4.5-2.04 2.03-.02 7.36 4.5 11.9 4.54 4.52 9.87 6.54 11.9 4.5Z\" /> <path d=\"M15.7 15.7c4.52-4.54 6.54-9.87 4.5-11.9-2.03-2.04-7.36-.02-11.9 4.5-4.52 4.54-6.54 9.87-4.5 11.9 2.03 2.04 7.36.02 11.9-4.5Z\" /></g>",
        "orbit":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M20.341 6.484A10 10 0 0 1 10.266 21.85\" /> <path d=\"M3.659 17.516A10 10 0 0 1 13.74 2.152\" /> <circle cx=\"12\" cy=\"12\" r=\"3\" /> <circle cx=\"19\" cy=\"5\" r=\"2\" /> <circle cx=\"5\" cy=\"19\" r=\"2\" /></g>",
        "cpu":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M12 20v2\" /> <path d=\"M12 2v2\" /> <path d=\"M17 20v2\" /> <path d=\"M17 2v2\" /> <path d=\"M2 12h2\" /> <path d=\"M2 17h2\" /> <path d=\"M2 7h2\" /> <path d=\"M20 12h2\" /> <path d=\"M20 17h2\" /> <path d=\"M20 7h2\" /> <path d=\"M7 20v2\" /> <path d=\"M7 2v2\" /> <rect x=\"4\" y=\"4\" width=\"16\" height=\"16\" rx=\"2\" /> <rect x=\"8\" y=\"8\" width=\"8\" height=\"8\" rx=\"1\" /></g>",
        "microchip":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M10 12h4\" /> <path d=\"M10 17h4\" /> <path d=\"M10 7h4\" /> <path d=\"M18 12h2\" /> <path d=\"M18 18h2\" /> <path d=\"M18 6h2\" /> <path d=\"M4 12h2\" /> <path d=\"M4 18h2\" /> <path d=\"M4 6h2\" /> <rect x=\"6\" y=\"2\" width=\"12\" height=\"20\" rx=\"2\" /></g>",
        "scan-eye":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M3 7V5a2 2 0 0 1 2-2h2\" /> <path d=\"M17 3h2a2 2 0 0 1 2 2v2\" /> <path d=\"M21 17v2a2 2 0 0 1-2 2h-2\" /> <path d=\"M7 21H5a2 2 0 0 1-2-2v-2\" /> <circle cx=\"12\" cy=\"12\" r=\"1\" /> <path d=\"M18.944 12.33a1 1 0 0 0 0-.66 7.5 7.5 0 0 0-13.888 0 1 1 0 0 0 0 .66 7.5 7.5 0 0 0 13.888 0\" /></g>",
        "message-square-code":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M22 17a2 2 0 0 1-2 2H6.828a2 2 0 0 0-1.414.586l-2.202 2.202A.71.71 0 0 1 2 21.286V5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2z\" /> <path d=\"m10 8-3 3 3 3\" /> <path d=\"m14 14 3-3-3-3\" /></g>",
        "audio-waveform":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M2 13a2 2 0 0 0 2-2V7a2 2 0 0 1 4 0v13a2 2 0 0 0 4 0V4a2 2 0 0 1 4 0v13a2 2 0 0 0 4 0v-4a2 2 0 0 1 2-2\" /></g>",
        "image":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><rect width=\"18\" height=\"18\" x=\"3\" y=\"3\" rx=\"2\" ry=\"2\" /> <circle cx=\"9\" cy=\"9\" r=\"2\" /> <path d=\"m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21\" /></g>",
        "scan-text":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M3 7V5a2 2 0 0 1 2-2h2\" /> <path d=\"M17 3h2a2 2 0 0 1 2 2v2\" /> <path d=\"M21 17v2a2 2 0 0 1-2 2h-2\" /> <path d=\"M7 21H5a2 2 0 0 1-2-2v-2\" /> <path d=\"M7 8h8\" /> <path d=\"M7 12h10\" /> <path d=\"M7 16h6\" /></g>",
        "telescope":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"m10.065 12.493-6.18 1.318a.934.934 0 0 1-1.108-.702l-.537-2.15a1.07 1.07 0 0 1 .691-1.265l13.504-4.44\" /> <path d=\"m13.56 11.747 4.332-.924\" /> <path d=\"m16 21-3.105-6.21\" /> <path d=\"M16.485 5.94a2 2 0 0 1 1.455-2.425l1.09-.272a1 1 0 0 1 1.212.727l1.515 6.06a1 1 0 0 1-.727 1.213l-1.09.272a2 2 0 0 1-2.425-1.455z\" /> <path d=\"m6.158 8.633 1.114 4.456\" /> <path d=\"m8 21 3.105-6.21\" /> <circle cx=\"12\" cy=\"13\" r=\"2\" /></g>",
        "satellite":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"m13.5 6.5-3.148-3.148a1.205 1.205 0 0 0-1.704 0L6.352 5.648a1.205 1.205 0 0 0 0 1.704L9.5 10.5\" /> <path d=\"M16.5 7.5 19 5\" /> <path d=\"m17.5 10.5 3.148 3.148a1.205 1.205 0 0 1 0 1.704l-2.296 2.296a1.205 1.205 0 0 1-1.704 0L13.5 14.5\" /> <path d=\"M9 21a6 6 0 0 0-6-6\" /> <path d=\"M9.352 10.648a1.205 1.205 0 0 0 0 1.704l2.296 2.296a1.205 1.205 0 0 0 1.704 0l4.296-4.296a1.205 1.205 0 0 0 0-1.704l-2.296-2.296a1.205 1.205 0 0 0-1.704 0z\" /></g>",
        "antenna":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M2 12 7 2\" /> <path d=\"m7 12 5-10\" /> <path d=\"m12 12 5-10\" /> <path d=\"m17 12 5-10\" /> <path d=\"M4.5 7h15\" /> <path d=\"M12 16v6\" /></g>",
        "radio":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M16.247 7.761a6 6 0 0 1 0 8.478\" /> <path d=\"M19.075 4.933a10 10 0 0 1 0 14.134\" /> <path d=\"M4.925 19.067a10 10 0 0 1 0-14.134\" /> <path d=\"M7.753 16.239a6 6 0 0 1 0-8.478\" /> <circle cx=\"12\" cy=\"12\" r=\"2\" /></g>",
        "waves":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M2 12q2.5 2 5 0t5 0 5 0 5 0\" /> <path d=\"M2 19q2.5 2 5 0t5 0 5 0 5 0\" /> <path d=\"M2 5q2.5 2 5 0t5 0 5 0 5 0\" /></g>",
        "waypoints":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"m10.586 5.414-5.172 5.172\" /> <path d=\"m18.586 13.414-5.172 5.172\" /> <path d=\"M6 12h12\" /> <circle cx=\"12\" cy=\"20\" r=\"2\" /> <circle cx=\"12\" cy=\"4\" r=\"2\" /> <circle cx=\"20\" cy=\"12\" r=\"2\" /> <circle cx=\"4\" cy=\"12\" r=\"2\" /></g>",
        "spline":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><circle cx=\"19\" cy=\"5\" r=\"2\" /> <circle cx=\"5\" cy=\"19\" r=\"2\" /> <path d=\"M5 17A12 12 0 0 1 17 5\" /></g>",
        "activity":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.25.25 0 0 1-.48 0L9.24 2.18a.25.25 0 0 0-.48 0l-2.35 8.36A2 2 0 0 1 4.49 12H2\" /></g>",
        "gauge":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"m12 14 4-4\" /> <path d=\"M3.34 19a10 10 0 1 1 17.32 0\" /></g>",
        "sigma":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M18 7V5a1 1 0 0 0-1-1H6.5a.5.5 0 0 0-.4.8l4.5 6a2 2 0 0 1 0 2.4l-4.5 6a.5.5 0 0 0 .4.8H17a1 1 0 0 0 1-1v-2\" /></g>",
        "infinity":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M6 16c5 0 7-8 12-8a4 4 0 0 1 0 8c-5 0-7-8-12-8a4 4 0 1 0 0 8\" /></g>",
        "combine":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M14 3a1 1 0 0 1 1 1v5a1 1 0 0 1-1 1\" /> <path d=\"M19 3a1 1 0 0 1 1 1v5a1 1 0 0 1-1 1\" /> <path d=\"m7 15 3 3\" /> <path d=\"m7 21 3-3H5a2 2 0 0 1-2-2v-2\" /> <rect x=\"14\" y=\"14\" width=\"7\" height=\"7\" rx=\"1\" /> <rect x=\"3\" y=\"3\" width=\"7\" height=\"7\" rx=\"1\" /></g>",
        "merge":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"m8 6 4-4 4 4\" /> <path d=\"M12 2v10.3a4 4 0 0 1-1.172 2.872L4 22\" /> <path d=\"m20 22-5-5\" /></g>",
        "focus":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><circle cx=\"12\" cy=\"12\" r=\"3\" /> <path d=\"M3 7V5a2 2 0 0 1 2-2h2\" /> <path d=\"M17 3h2a2 2 0 0 1 2 2v2\" /> <path d=\"M21 17v2a2 2 0 0 1-2 2h-2\" /> <path d=\"M7 21H5a2 2 0 0 1-2-2v-2\" /></g>",
        "bot-message-square":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M12 6V2H8\" /> <path d=\"M15 11v2\" /> <path d=\"M2 12h2\" /> <path d=\"M20 12h2\" /> <path d=\"M20 16a2 2 0 0 1-2 2H8.828a2 2 0 0 0-1.414.586l-2.202 2.202A.71.71 0 0 1 4 20.286V8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2z\" /> <path d=\"M9 11v2\" /></g>",
        "scan-search":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M3 7V5a2 2 0 0 1 2-2h2\" /> <path d=\"M17 3h2a2 2 0 0 1 2 2v2\" /> <path d=\"M21 17v2a2 2 0 0 1-2 2h-2\" /> <path d=\"M7 21H5a2 2 0 0 1-2-2v-2\" /> <circle cx=\"12\" cy=\"12\" r=\"3\" /> <path d=\"m16 16-1.9-1.9\" /></g>",
        "search":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"m21 21-4.34-4.34\" /> <circle cx=\"11\" cy=\"11\" r=\"8\" /></g>",
    },
    "infra": {
        "server":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><rect width=\"20\" height=\"8\" x=\"2\" y=\"2\" rx=\"2\" ry=\"2\" /> <rect width=\"20\" height=\"8\" x=\"2\" y=\"14\" rx=\"2\" ry=\"2\" /> <line x1=\"6\" x2=\"6.01\" y1=\"6\" y2=\"6\" /> <line x1=\"6\" x2=\"6.01\" y1=\"18\" y2=\"18\" /></g>",
        "network":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><rect x=\"16\" y=\"16\" width=\"6\" height=\"6\" rx=\"1\" /> <rect x=\"2\" y=\"16\" width=\"6\" height=\"6\" rx=\"1\" /> <rect x=\"9\" y=\"2\" width=\"6\" height=\"6\" rx=\"1\" /> <path d=\"M5 16v-3a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3\" /> <path d=\"M12 12V8\" /></g>",
        "cloud":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z\" /></g>",
        "globe":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><circle cx=\"12\" cy=\"12\" r=\"10\" /> <path d=\"M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20\" /> <path d=\"M2 12h20\" /></g>",
        "router":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><rect width=\"20\" height=\"8\" x=\"2\" y=\"14\" rx=\"2\" /> <path d=\"M6.01 18H6\" /> <path d=\"M10.01 18H10\" /> <path d=\"M15 10v4\" /> <path d=\"M17.84 7.17a4 4 0 0 0-5.66 0\" /> <path d=\"M20.66 4.34a8 8 0 0 0-11.31 0\" /></g>",
        "radio-tower":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M4.9 16.1C1 12.2 1 5.8 4.9 1.9\" /> <path d=\"M7.8 4.7a6.14 6.14 0 0 0-.8 7.5\" /> <circle cx=\"12\" cy=\"9\" r=\"2\" /> <path d=\"M16.2 4.8c2 2 2.26 5.11.8 7.47\" /> <path d=\"M19.1 1.9a9.96 9.96 0 0 1 0 14.1\" /> <path d=\"M9.5 18h5\" /> <path d=\"m8 22 4-11 4 11\" /></g>",
        "signal":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M2 20h.01\" /> <path d=\"M7 20v-4\" /> <path d=\"M12 20v-8\" /> <path d=\"M17 20V8\" /> <path d=\"M22 4v16\" /></g>",
        "wifi":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M12 20h.01\" /> <path d=\"M2 8.82a15 15 0 0 1 20 0\" /> <path d=\"M5 12.859a10 10 0 0 1 14 0\" /> <path d=\"M8.5 16.429a5 5 0 0 1 7 0\" /></g>",
        "ethernet-port":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M10 8v1\" /> <path d=\"M14 8v1\" /> <path d=\"M18 8v1\" /> <path d=\"M19 17a2 2 0 00-1.765 1.059l-.47.882A2 2 0 0115 20H9a2 2 0 01-1.765-1.059l-.47-.882A2 2 0 005 17H4a2 2 0 01-2-2V6a2 2 0 012-2h16a2 2 0 012 2v9a2 2 0 01-2 2z\" /> <path d=\"M6 8v1\" /></g>",
        "cable":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M17 19a1 1 0 0 1-1-1v-2a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2a1 1 0 0 1-1 1z\" /> <path d=\"M17 21v-2\" /> <path d=\"M19 14V6.5a1 1 0 0 0-7 0v11a1 1 0 0 1-7 0V10\" /> <path d=\"M21 21v-2\" /> <path d=\"M3 5V3\" /> <path d=\"M4 10a2 2 0 0 1-2-2V6a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2a2 2 0 0 1-2 2z\" /> <path d=\"M7 5V3\" /></g>",
        "plug-zap":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M6.3 20.3a2.4 2.4 0 0 0 3.4 0L12 18l-6-6-2.3 2.3a2.4 2.4 0 0 0 0 3.4Z\" /> <path d=\"m2 22 3-3\" /> <path d=\"M7.5 13.5 10 11\" /> <path d=\"M10.5 16.5 13 14\" /> <path d=\"m18 3-4 4h6l-4 4\" /></g>",
        "cpu":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M12 20v2\" /> <path d=\"M12 2v2\" /> <path d=\"M17 20v2\" /> <path d=\"M17 2v2\" /> <path d=\"M2 12h2\" /> <path d=\"M2 17h2\" /> <path d=\"M2 7h2\" /> <path d=\"M20 12h2\" /> <path d=\"M20 17h2\" /> <path d=\"M20 7h2\" /> <path d=\"M7 20v2\" /> <path d=\"M7 2v2\" /> <rect x=\"4\" y=\"4\" width=\"16\" height=\"16\" rx=\"2\" /> <rect x=\"8\" y=\"8\" width=\"8\" height=\"8\" rx=\"1\" /></g>",
        "memory-stick":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M12 12v-2\" /> <path d=\"M12 18v-2\" /> <path d=\"M16 12v-2\" /> <path d=\"M16 18v-2\" /> <path d=\"M2 11h1.5\" /> <path d=\"M20 18v-2\" /> <path d=\"M20.5 11H22\" /> <path d=\"M4 18v-2\" /> <path d=\"M8 12v-2\" /> <path d=\"M8 18v-2\" /> <rect x=\"2\" y=\"6\" width=\"20\" height=\"10\" rx=\"2\" /></g>",
        "microchip":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M10 12h4\" /> <path d=\"M10 17h4\" /> <path d=\"M10 7h4\" /> <path d=\"M18 12h2\" /> <path d=\"M18 18h2\" /> <path d=\"M18 6h2\" /> <path d=\"M4 12h2\" /> <path d=\"M4 18h2\" /> <path d=\"M4 6h2\" /> <rect x=\"6\" y=\"2\" width=\"12\" height=\"20\" rx=\"2\" /></g>",
        "monitor":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><rect width=\"20\" height=\"14\" x=\"2\" y=\"3\" rx=\"2\" /> <line x1=\"8\" x2=\"16\" y1=\"21\" y2=\"21\" /> <line x1=\"12\" x2=\"12\" y1=\"17\" y2=\"21\" /></g>",
        "gauge":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"m12 14 4-4\" /> <path d=\"M3.34 19a10 10 0 1 1 17.32 0\" /></g>",
        "activity":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.25.25 0 0 1-.48 0L9.24 2.18a.25.25 0 0 0-.48 0l-2.35 8.36A2 2 0 0 1 4.49 12H2\" /></g>",
        "trending-up":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M16 7h6v6\" /> <path d=\"m22 7-8.5 8.5-5-5L2 17\" /></g>",
        "container":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M22 7.7c0-.6-.4-1.2-.8-1.5l-6.3-3.9a1.72 1.72 0 0 0-1.7 0l-10.3 6c-.5.2-.9.8-.9 1.4v6.6c0 .5.4 1.2.8 1.5l6.3 3.9a1.72 1.72 0 0 0 1.7 0l10.3-6c.5-.3.9-1 .9-1.5Z\" /> <path d=\"M10 21.9V14L2.1 9.1\" /> <path d=\"m10 14 11.9-6.9\" /> <path d=\"M14 19.8v-8.1\" /> <path d=\"M18 17.5V9.4\" /></g>",
        "boxes":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M2.97 12.92A2 2 0 0 0 2 14.63v3.24a2 2 0 0 0 .97 1.71l3 1.8a2 2 0 0 0 2.06 0L12 19v-5.5l-5-3-4.03 2.42Z\" /> <path d=\"m7 16.5-4.74-2.85\" /> <path d=\"m7 16.5 5-3\" /> <path d=\"M7 16.5v5.17\" /> <path d=\"M12 13.5V19l3.97 2.38a2 2 0 0 0 2.06 0l3-1.8a2 2 0 0 0 .97-1.71v-3.24a2 2 0 0 0-.97-1.71L17 10.5l-5 3Z\" /> <path d=\"m17 16.5-5-3\" /> <path d=\"m17 16.5 4.74-2.85\" /> <path d=\"M17 16.5v5.17\" /> <path d=\"M7.97 4.42A2 2 0 0 0 7 6.13v4.37l5 3 5-3V6.13a2 2 0 0 0-.97-1.71l-3-1.8a2 2 0 0 0-2.06 0l-3 1.8Z\" /> <path d=\"M12 8 7.26 5.15\" /> <path d=\"m12 8 4.74-2.85\" /> <path d=\"M12 13.5V8\" /></g>",
        "package":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M11 21.73a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73z\" /> <path d=\"M12 22V12\" /> <polyline points=\"3.29 7 12 12 20.71 7\" /> <path d=\"m7.5 4.27 9 5.15\" /></g>",
        "warehouse":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M18 21V10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1v11\" /> <path d=\"M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V8a2 2 0 0 1 1.132-1.803l7.95-3.974a2 2 0 0 1 1.837 0l7.948 3.974A2 2 0 0 1 22 8z\" /> <path d=\"M6 13h12\" /> <path d=\"M6 17h12\" /></g>",
        "factory":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M12 16h.01\" /> <path d=\"M16 16h.01\" /> <path d=\"M3 19a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V8.5a.5.5 0 0 0-.769-.422l-4.462 2.844A.5.5 0 0 1 15 10.5v-2a.5.5 0 0 0-.769-.422L9.77 10.922A.5.5 0 0 1 9 10.5V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2z\" /> <path d=\"M8 16h.01\" /></g>",
        "building-2":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M10 12h4\" /> <path d=\"M10 8h4\" /> <path d=\"M14 21v-3a2 2 0 0 0-4 0v3\" /> <path d=\"M6 10H4a2 2 0 0 0-2 2v7a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-2\" /> <path d=\"M6 21V5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v16\" /></g>",
        "map":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M14.106 5.553a2 2 0 0 0 1.788 0l3.659-1.83A1 1 0 0 1 21 4.619v12.764a1 1 0 0 1-.553.894l-4.553 2.277a2 2 0 0 1-1.788 0l-4.212-2.106a2 2 0 0 0-1.788 0l-3.659 1.83A1 1 0 0 1 3 19.381V6.618a1 1 0 0 1 .553-.894l4.553-2.277a2 2 0 0 1 1.788 0z\" /> <path d=\"M15 5.764v15\" /> <path d=\"M9 3.236v15\" /></g>",
        "route":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><circle cx=\"6\" cy=\"19\" r=\"3\" /> <path d=\"M9 19h8.5a3.5 3.5 0 0 0 0-7h-11a3.5 3.5 0 0 1 0-7H15\" /> <circle cx=\"18\" cy=\"5\" r=\"3\" /></g>",
        "navigation":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><polygon points=\"3 11 22 2 13 21 11 13 3 11\" /></g>",
        "compass":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><circle cx=\"12\" cy=\"12\" r=\"10\" /> <path d=\"m16.24 7.76-1.804 5.411a2 2 0 0 1-1.265 1.265L7.76 16.24l1.804-5.411a2 2 0 0 1 1.265-1.265z\" /></g>",
        "satellite-dish":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M18 12a6 6 0 00-6-6\" /> <path d=\"M2.824 10.459a8 8 0 0010.717 10.717c.558-.276.623-1.012.183-1.452l-9.448-9.448c-.44-.44-1.176-.375-1.452.183\" /> <path d=\"M22 12A10 10 0 0012 2\" /> <path d=\"m9 15 4-4\" /></g>",
        "battery-charging":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"m11 7-3 5h4l-3 5\" /> <path d=\"M14.856 6H16a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-2.935\" /> <path d=\"M22 14v-4\" /> <path d=\"M5.14 18H4a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h2.936\" /></g>",
        "zap":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M15.914 4a1.5 1.5 0 00-2.474-1.561l-9 9A1.5 1.5 0 005.5 14h4.002a.5.5 0 01.471.666L8.086 20a1.5 1.5 0 002.475 1.56l9-9A1.5 1.5 0 0018.5 10h-3.997a.5.5 0 01-.472-.667z\" /></g>",
        "thermometer":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z\" /></g>",
        "power":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M12 2v10\" /> <path d=\"M18.4 6.6a9 9 0 1 1-12.77.04\" /></g>",
        "workflow":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><rect width=\"8\" height=\"8\" x=\"3\" y=\"3\" rx=\"2\" /> <path d=\"M7 11v4a2 2 0 0 0 2 2h4\" /> <rect width=\"8\" height=\"8\" x=\"13\" y=\"13\" rx=\"2\" /></g>",
        "waypoints":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"m10.586 5.414-5.172 5.172\" /> <path d=\"m18.586 13.414-5.172 5.172\" /> <path d=\"M6 12h12\" /> <circle cx=\"12\" cy=\"20\" r=\"2\" /> <circle cx=\"12\" cy=\"4\" r=\"2\" /> <circle cx=\"20\" cy=\"12\" r=\"2\" /> <circle cx=\"4\" cy=\"12\" r=\"2\" /></g>",
        "hard-drive":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M10 16h.01\" /> <path d=\"M2.212 11.577a2 2 0 0 0-.212.896V18a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-5.527a2 2 0 0 0-.212-.896L18.55 5.11A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z\" /> <path d=\"M21.946 12.013H2.054\" /> <path d=\"M6 16h.01\" /></g>",
        "database":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><ellipse cx=\"12\" cy=\"5\" rx=\"9\" ry=\"3\" /> <path d=\"M3 5V19A9 3 0 0 0 21 19V5\" /> <path d=\"M3 12A9 3 0 0 0 21 12\" /></g>",
        "cloud-cog":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"m10.852 19.772-.383.924\" /> <path d=\"m13.148 14.228.383-.923\" /> <path d=\"M13.148 19.772a3 3 0 1 0-2.296-5.544l-.383-.923\" /> <path d=\"m13.53 20.696-.382-.924a3 3 0 1 1-2.296-5.544\" /> <path d=\"m14.772 15.852.923-.383\" /> <path d=\"m14.772 18.148.923.383\" /> <path d=\"M4.2 15.1a7 7 0 1 1 9.93-9.858A7 7 0 0 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.2\" /> <path d=\"m9.228 15.852-.923-.383\" /> <path d=\"m9.228 18.148-.923.383\" /></g>",
        "server-cog":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"m10.852 14.772-.383.923\" /> <path d=\"M13.148 14.772a3 3 0 1 0-2.296-5.544l-.383-.923\" /> <path d=\"m13.148 9.228.383-.923\" /> <path d=\"m13.53 15.696-.382-.924a3 3 0 1 1-2.296-5.544\" /> <path d=\"m14.772 10.852.923-.383\" /> <path d=\"m14.772 13.148.923.383\" /> <path d=\"M4.5 10H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2h-.5\" /> <path d=\"M4.5 14H4a2 2 0 0 0-2 2v4a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-4a2 2 0 0 0-2-2h-.5\" /> <path d=\"M6 18h.01\" /> <path d=\"M6 6h.01\" /> <path d=\"m9.228 10.852-.923-.383\" /> <path d=\"m9.228 13.148-.923.383\" /></g>",
        "server-crash":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M6 10H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2h-2\" /> <path d=\"M6 14H4a2 2 0 0 0-2 2v4a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-4a2 2 0 0 0-2-2h-2\" /> <path d=\"M6 6h.01\" /> <path d=\"M6 18h.01\" /> <path d=\"m13 6-4 6h6l-4 6\" /></g>",
    },
    "genericos": {
        "rocket":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5\" /> <path d=\"M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09\" /> <path d=\"M9 12a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.4 22.4 0 0 1-4 2z\" /> <path d=\"M9 12H4s.55-3.03 2-4c1.62-1.08 5 .05 5 .05\" /></g>",
        "target":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><circle cx=\"12\" cy=\"12\" r=\"10\" /> <circle cx=\"12\" cy=\"12\" r=\"6\" /> <circle cx=\"12\" cy=\"12\" r=\"2\" /></g>",
        "trophy":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M10 14.66V17a1 1 0 0 1-1 1 2 2 0 0 0-2 2v2\" /> <path d=\"M14 14.66V17a1 1 0 0 0 1 1 2 2 0 0 1 2 2v2\" /> <path d=\"M17.916 10H19.5A2.5 2.5 0 0 0 22 7.5V5a1 1 0 0 0-1-1h-3\" /> <path d=\"M4 22h16\" /> <path d=\"M6 9a6 6 0 0 0 12 0V3a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1z\" /> <path d=\"M6.084 10H4.5A2.5 2.5 0 0 1 2 7.5V5a1 1 0 0 1 1-1h3\" /></g>",
        "medal":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M7.21 15 2.66 7.14a2 2 0 0 1 .13-2.2L4.4 2.8A2 2 0 0 1 6 2h12a2 2 0 0 1 1.6.8l1.6 2.14a2 2 0 0 1 .14 2.2L16.79 15\" /> <path d=\"M11 12 5.12 2.2\" /> <path d=\"m13 12 5.88-9.8\" /> <path d=\"M8 7h8\" /> <circle cx=\"12\" cy=\"17\" r=\"5\" /> <path d=\"M12 18v-2h-.5\" /></g>",
        "award":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"m15.477 12.89 1.515 8.526a.5.5 0 0 1-.81.47l-3.58-2.687a1 1 0 0 0-1.197 0l-3.586 2.686a.5.5 0 0 1-.81-.469l1.514-8.526\" /> <circle cx=\"12\" cy=\"8\" r=\"6\" /></g>",
        "star":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z\" /></g>",
        "flame":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M12 3q1 4 4 6.5t3 5.5a1 1 0 0 1-14 0 5 5 0 0 1 1-3 1 1 0 0 0 5 0c0-2-1.5-3-1.5-5q0-2 2.5-4\" /></g>",
        "zap":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M15.914 4a1.5 1.5 0 00-2.474-1.561l-9 9A1.5 1.5 0 005.5 14h4.002a.5.5 0 01.471.666L8.086 20a1.5 1.5 0 002.475 1.56l9-9A1.5 1.5 0 0018.5 10h-3.997a.5.5 0 01-.472-.667z\" /></g>",
        "lightbulb":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5\" /> <path d=\"M9 18h6\" /> <path d=\"M10 22h4\" /></g>",
        "book-open":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M12 5v16\" /> <path d=\"M20.001 19A2 2 0 0022 17V5a2 2 0 00-1.999-2L16 3.002A5 5 0 0012 5a5 5 0 00-4-2H4a2 2 0 00-2 2v12a2 2 0 001.999 2H8a5 5 0 014 2 5 5 0 014-2z\" /></g>",
        "graduation-cap":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M21.42 10.922a1 1 0 0 0-.019-1.838L12.83 5.18a2 2 0 0 0-1.66 0L2.6 9.08a1 1 0 0 0 0 1.832l8.57 3.908a2 2 0 0 0 1.66 0z\" /> <path d=\"M22 10v6\" /> <path d=\"M6 12.5V16a6 3 0 0 0 12 0v-3.5\" /></g>",
        "map":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M14.106 5.553a2 2 0 0 0 1.788 0l3.659-1.83A1 1 0 0 1 21 4.619v12.764a1 1 0 0 1-.553.894l-4.553 2.277a2 2 0 0 1-1.788 0l-4.212-2.106a2 2 0 0 0-1.788 0l-3.659 1.83A1 1 0 0 1 3 19.381V6.618a1 1 0 0 1 .553-.894l4.553-2.277a2 2 0 0 1 1.788 0z\" /> <path d=\"M15 5.764v15\" /> <path d=\"M9 3.236v15\" /></g>",
        "compass":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><circle cx=\"12\" cy=\"12\" r=\"10\" /> <path d=\"m16.24 7.76-1.804 5.411a2 2 0 0 1-1.265 1.265L7.76 16.24l1.804-5.411a2 2 0 0 1 1.265-1.265z\" /></g>",
        "route":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><circle cx=\"6\" cy=\"19\" r=\"3\" /> <path d=\"M9 19h8.5a3.5 3.5 0 0 0 0-7h-11a3.5 3.5 0 0 1 0-7H15\" /> <circle cx=\"18\" cy=\"5\" r=\"3\" /></g>",
        "flag":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M4 22V4a1 1 0 0 1 .4-.8A6 6 0 0 1 8 2c3 0 5 2 7.333 2q2 0 3.067-.8A1 1 0 0 1 20 4v10a1 1 0 0 1-.4.8A6 6 0 0 1 16 16c-3 0-5-2-8-2a6 6 0 0 0-4 1.528\" /></g>",
        "badge-check":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z\" /> <path d=\"m16 9-5.5 5.5L8 12\" /></g>",
        "circle-check":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><circle cx=\"12\" cy=\"12\" r=\"10\" /> <path d=\"m16 9-5.5 5.5L8 12\" /></g>",
        "circle-x":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><circle cx=\"12\" cy=\"12\" r=\"10\" /> <path d=\"m15 9-6 6\" /> <path d=\"m9 9 6 6\" /></g>",
        "triangle-alert":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3\" /> <path d=\"M12 9v4\" /> <path d=\"M12 17h.01\" /></g>",
        "info":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><circle cx=\"12\" cy=\"12\" r=\"10\" /> <path d=\"M12 16v-4\" /> <path d=\"M12 8h.01\" /></g>",
        "circle-help":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><circle cx=\"12\" cy=\"12\" r=\"10\" /> <path d=\"M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3\" /> <path d=\"M12 17h.01\" /></g>",
        "arrow-up-right":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M7 7h10v10\" /> <path d=\"M7 17 17 7\" /></g>",
        "external-link":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M15 3h6v6\" /> <path d=\"M10 14 21 3\" /> <path d=\"M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6\" /></g>",
        "download":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M12 15V3\" /> <path d=\"M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4\" /> <path d=\"m7 10 5 5 5-5\" /></g>",
        "upload":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M12 3v12\" /> <path d=\"m17 8-5-5-5 5\" /> <path d=\"M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4\" /></g>",
        "share-2":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><circle cx=\"18\" cy=\"5\" r=\"3\" /> <circle cx=\"6\" cy=\"12\" r=\"3\" /> <circle cx=\"18\" cy=\"19\" r=\"3\" /> <line x1=\"8.59\" x2=\"15.42\" y1=\"13.51\" y2=\"17.49\" /> <line x1=\"15.41\" x2=\"8.59\" y1=\"6.51\" y2=\"10.49\" /></g>",
        "bookmark":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M17 3a2 2 0 0 1 2 2v15a1 1 0 0 1-1.496.868l-4.512-2.578a2 2 0 0 0-1.984 0l-4.512 2.578A1 1 0 0 1 5 20V5a2 2 0 0 1 2-2z\" /></g>",
        "heart":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M2 9.5a5.5 5.5 0 0 1 9.591-3.676.56.56 0 0 0 .818 0A5.49 5.49 0 0 1 22 9.5c0 2.29-1.5 4-3 5.5l-5.492 5.313a2 2 0 0 1-3 .019L5 15c-1.5-1.5-3-3.2-3-5.5\" /></g>",
        "thumbs-up":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M15 5.88 14 10h5.83a2 2 0 0 1 1.92 2.56l-2.33 8A2 2 0 0 1 17.5 22H4a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2h2.76a2 2 0 0 0 1.79-1.11L12 2a3.13 3.13 0 0 1 3 3.88Z\" /> <path d=\"M7 10v12\" /></g>",
        "clock":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><circle cx=\"12\" cy=\"12\" r=\"10\" /> <path d=\"M12 6v6l4 2\" /></g>",
        "calendar":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M8 2v3\" /> <path d=\"M16 2v3\" /> <rect x=\"3\" y=\"3\" width=\"18\" height=\"18\" rx=\"2\" /> <path d=\"M3 9h18\" /></g>",
        "hash":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><line x1=\"4\" x2=\"20\" y1=\"9\" y2=\"9\" /> <line x1=\"4\" x2=\"20\" y1=\"15\" y2=\"15\" /> <line x1=\"10\" x2=\"8\" y1=\"3\" y2=\"21\" /> <line x1=\"16\" x2=\"14\" y1=\"3\" y2=\"21\" /></g>",
        "gift":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M12 7v14\" /> <path d=\"M20 11v8a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-8\" /> <path d=\"M7.5 7a1 1 0 0 1 0-5A4.8 8 0 0 1 12 7a4.8 8 0 0 1 4.5-5 1 1 0 0 1 0 5\" /> <rect x=\"3\" y=\"7\" width=\"18\" height=\"4\" rx=\"1\" /></g>",
        "party-popper":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M5.8 11.3 2 22l10.7-3.79\" /> <path d=\"M4 3h.01\" /> <path d=\"M22 8h.01\" /> <path d=\"M15 2h.01\" /> <path d=\"M22 20h.01\" /> <path d=\"m22 2-2.24.75a2.9 2.9 0 0 0-1.96 3.12c.1.86-.57 1.63-1.45 1.63h-.38c-.86 0-1.6.6-1.76 1.44L14 10\" /> <path d=\"m22 13-.82-.33c-.86-.34-1.82.2-1.98 1.11c-.11.7-.72 1.22-1.43 1.22H17\" /> <path d=\"m11 2 .33.82c.34.86-.2 1.82-1.11 1.98C9.52 4.9 9 5.52 9 6.23V7\" /> <path d=\"M11 13c1.93 1.93 2.83 4.17 2 5-.83.83-3.07-.07-5-2-1.93-1.93-2.83-4.17-2-5 .83-.83 3.07.07 5 2Z\" /></g>",
        "megaphone":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M11 6a13 13 0 0 0 8.4-2.8A1 1 0 0 1 21 4v12a1 1 0 0 1-1.6.8A13 13 0 0 0 11 14H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2z\" /> <path d=\"M6 14a12 12 0 0 0 2.4 7.2 2 2 0 0 0 3.2-2.4A8 8 0 0 1 10 14\" /> <path d=\"M8 6v8\" /></g>",
        "sparkles":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M11.017 2.814a1 1 0 0 1 1.966 0l1.051 5.558a2 2 0 0 0 1.594 1.594l5.558 1.051a1 1 0 0 1 0 1.966l-5.558 1.051a2 2 0 0 0-1.594 1.594l-1.051 5.558a1 1 0 0 1-1.966 0l-1.051-5.558a2 2 0 0 0-1.594-1.594l-5.558-1.051a1 1 0 0 1 0-1.966l5.558-1.051a2 2 0 0 0 1.594-1.594z\" /> <path d=\"M20 2v4\" /> <path d=\"M22 4h-4\" /> <circle cx=\"4\" cy=\"20\" r=\"2\" /></g>",
        "crown":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M11.562 3.266a.5.5 0 0 1 .876 0L15.39 8.87a1 1 0 0 0 1.516.294L21.183 5.5a.5.5 0 0 1 .798.519l-2.834 10.246a1 1 0 0 1-.956.734H5.81a1 1 0 0 1-.957-.734L2.02 6.02a.5.5 0 0 1 .798-.519l4.276 3.664a1 1 0 0 0 1.516-.294z\" /> <path d=\"M5 21h14\" /></g>",
        "gem":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M10.5 3 8 9l4 13 4-13-2.5-6\" /> <path d=\"M17 3a2 2 0 0 1 1.6.8l3 4a2 2 0 0 1 .013 2.382l-7.99 10.986a2 2 0 0 1-3.247 0l-7.99-10.986A2 2 0 0 1 2.4 7.8l2.998-3.997A2 2 0 0 1 7 3z\" /> <path d=\"M2 9h20\" /></g>",
        "hourglass":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M5 22h14\" /> <path d=\"M5 2h14\" /> <path d=\"M17 22v-4.172a2 2 0 0 0-.586-1.414L12 12l-4.414 4.414A2 2 0 0 0 7 17.828V22\" /> <path d=\"M7 2v4.172a2 2 0 0 0 .586 1.414L12 12l4.414-4.414A2 2 0 0 0 17 6.172V2\" /></g>",
        "timer":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><line x1=\"10\" x2=\"14\" y1=\"2\" y2=\"2\" /> <line x1=\"12\" x2=\"15\" y1=\"14\" y2=\"11\" /> <circle cx=\"12\" cy=\"14\" r=\"8\" /></g>",
        "palette":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M12 22a1 1 0 0 1 0-20 10 9 0 0 1 10 9 5 5 0 0 1-5 5h-2.25a1.75 1.75 0 0 0-1.4 2.8l.3.4a1.75 1.75 0 0 1-1.4 2.8z\" /> <circle cx=\"13.5\" cy=\"6.5\" r=\".5\" fill=\"url(#c)\" /> <circle cx=\"17.5\" cy=\"10.5\" r=\".5\" fill=\"url(#c)\" /> <circle cx=\"6.5\" cy=\"12.5\" r=\".5\" fill=\"url(#c)\" /> <circle cx=\"8.5\" cy=\"7.5\" r=\".5\" fill=\"url(#c)\" /></g>",
        "pencil":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497z\" /> <path d=\"m15 5 4 4\" /></g>",
        "pen-tool":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"m18 13-.654-4.736a4 4 0 00-2.756-3.266l-9.163-2.9a2 2 0 00-2.017.493l-.82.819a2 2 0 00-.492 2.017l2.9 9.163a4 4 0 003.266 2.756L13 18\" /> <path d=\"M18.648 12.352a1.205 1.205 0 011.704 0l1.296 1.296a1.205 1.205 0 010 1.704l-6.296 6.296a1.205 1.205 0 01-1.704 0l-1.296-1.296a1.205 1.205 0 010-1.704z\" /> <path d=\"m3 3 6.586 6.586\" /> <circle cx=\"11\" cy=\"11\" r=\"2\" /></g>",
        "scissors":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><circle cx=\"6\" cy=\"6\" r=\"3\" /> <path d=\"M8.12 8.12 12 12\" /> <path d=\"M20 4 8.12 15.88\" /> <circle cx=\"6\" cy=\"18\" r=\"3\" /> <path d=\"M14.8 14.8 20 20\" /></g>",
        "wrench":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.106-3.105c.32-.322.863-.22.983.218a6 6 0 0 1-8.259 7.057l-7.91 7.91a1 1 0 0 1-2.999-3l7.91-7.91a6 6 0 0 1 7.057-8.259c.438.12.54.662.219.984z\" /></g>",
        "cog":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M11 10.27 7 3.34\" /> <path d=\"m11 13.73-4 6.93\" /> <path d=\"M12 22v-2\" /> <path d=\"M12 2v2\" /> <path d=\"M14 12h8\" /> <path d=\"m17 20.66-1-1.73\" /> <path d=\"m17 3.34-1 1.73\" /> <path d=\"M2 12h2\" /> <path d=\"m20.66 17-1.73-1\" /> <path d=\"m20.66 7-1.73 1\" /> <path d=\"m3.34 17 1.73-1\" /> <path d=\"m3.34 7 1.73 1\" /> <circle cx=\"12\" cy=\"12\" r=\"2\" /> <circle cx=\"12\" cy=\"12\" r=\"8\" /></g>",
        "search":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"m21 21-4.34-4.34\" /> <circle cx=\"11\" cy=\"11\" r=\"8\" /></g>",
        "filter":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M10 20a1 1 0 0 0 .553.895l2 1A1 1 0 0 0 14 21v-7a2 2 0 0 1 .517-1.341L21.74 4.67A1 1 0 0 0 21 3H3a1 1 0 0 0-.742 1.67l7.225 7.989A2 2 0 0 1 10 14z\" /></g>",
        "sliders-horizontal":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M10 5H3\" /> <path d=\"M12 19H3\" /> <path d=\"M14 3v4\" /> <path d=\"M16 17v4\" /> <path d=\"M21 12h-9\" /> <path d=\"M21 19h-5\" /> <path d=\"M21 5h-7\" /> <path d=\"M8 10v4\" /> <path d=\"M8 12H3\" /></g>",
        "users":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2\" /> <path d=\"M16 3.128a4 4 0 0 1 0 7.744\" /> <path d=\"M22 21v-2a4 4 0 0 0-3-3.87\" /> <circle cx=\"9\" cy=\"7\" r=\"4\" /></g>",
        "user-plus":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2\" /> <circle cx=\"9\" cy=\"7\" r=\"4\" /> <line x1=\"19\" x2=\"19\" y1=\"8\" y2=\"14\" /> <line x1=\"22\" x2=\"16\" y1=\"11\" y2=\"11\" /></g>",
        "message-square":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M22 17a2 2 0 0 1-2 2H6.828a2 2 0 0 0-1.414.586l-2.202 2.202A.71.71 0 0 1 2 21.286V5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2z\" /></g>",
        "mail":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"m22 7-8.991 5.727a2 2 0 0 1-2.009 0L2 7\" /> <rect x=\"2\" y=\"4\" width=\"20\" height=\"16\" rx=\"2\" /></g>",
        "phone":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M13.832 16.568a1 1 0 0 0 1.213-.303l.355-.465A2 2 0 0 1 17 15h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2A18 18 0 0 1 2 4a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2v3a2 2 0 0 1-.8 1.6l-.468.351a1 1 0 0 0-.292 1.233 14 14 0 0 0 6.392 6.384\" /></g>",
        "bell":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M10.268 21a2 2 0 0 0 3.464 0\" /> <path d=\"M3.262 15.326A1 1 0 0 0 4 17h16a1 1 0 0 0 .74-1.673C19.41 13.956 18 12.499 18 8A6 6 0 0 0 6 8c0 4.499-1.411 5.956-2.738 7.326\" /></g>",
        "tag":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M12.586 2.586A2 2 0 0 0 11.172 2H4a2 2 0 0 0-2 2v7.172a2 2 0 0 0 .586 1.414l8.704 8.704a2.426 2.426 0 0 0 3.42 0l6.58-6.58a2.426 2.426 0 0 0 0-3.42z\" /> <circle cx=\"7.5\" cy=\"7.5\" r=\".5\" fill=\"url(#c)\" /></g>",
        "ticket":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M2 9a3 3 0 0 1 0 6v2a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-2a3 3 0 0 1 0-6V7a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z\" /> <path d=\"M13 5v2\" /> <path d=\"M13 17v2\" /> <path d=\"M13 11v2\" /></g>",
        "wallet":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1\" /> <path d=\"M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4\" /></g>",
        "credit-card":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><rect width=\"20\" height=\"14\" x=\"2\" y=\"5\" rx=\"2\" /> <line x1=\"2\" x2=\"22\" y1=\"10\" y2=\"10\" /> <path d=\"M6 14h2\" /></g>",
        "briefcase":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M16 20V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16\" /> <rect width=\"20\" height=\"14\" x=\"2\" y=\"6\" rx=\"2\" /></g>",
        "building":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M12 10h.01\" /> <path d=\"M12 14h.01\" /> <path d=\"M12 6h.01\" /> <path d=\"M16 10h.01\" /> <path d=\"M16 14h.01\" /> <path d=\"M16 6h.01\" /> <path d=\"M8 10h.01\" /> <path d=\"M8 14h.01\" /> <path d=\"M8 6h.01\" /> <path d=\"M9 22v-3a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v3\" /> <rect x=\"4\" y=\"2\" width=\"16\" height=\"20\" rx=\"2\" /></g>",
        "home":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8\" /> <path d=\"M3 10a2 2 0 0 1 .709-1.528l7-6a2 2 0 0 1 2.582 0l7 6A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z\" /></g>",
        "puzzle":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M15.39 4.39a1 1 0 0 0 1.68-.474 2.5 2.5 0 1 1 3.014 3.015 1 1 0 0 0-.474 1.68l1.683 1.682a2.414 2.414 0 0 1 0 3.414L19.61 15.39a1 1 0 0 1-1.68-.474 2.5 2.5 0 1 0-3.014 3.015 1 1 0 0 1 .474 1.68l-1.683 1.682a2.414 2.414 0 0 1-3.414 0L8.61 19.61a1 1 0 0 0-1.68.474 2.5 2.5 0 1 1-3.014-3.015 1 1 0 0 0 .474-1.68l-1.683-1.682a2.414 2.414 0 0 1 0-3.414L4.39 8.61a1 1 0 0 1 1.68.474 2.5 2.5 0 1 0 3.014-3.015 1 1 0 0 1-.474-1.68l1.683-1.682a2.414 2.414 0 0 1 3.414 0z\" /></g>",
        "blocks":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M10 22V7a1 1 0 0 0-1-1H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-5a1 1 0 0 0-1-1H2\" /> <rect x=\"14\" y=\"2\" width=\"8\" height=\"8\" rx=\"1\" /></g>",
        "smile":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M15 10V9\" /> <path d=\"M16.472 15a6 6 0 01-8.943 0\" /> <path d=\"M9 10V9\" /> <circle cx=\"12\" cy=\"12\" r=\"10\" /></g>",
        "handshake":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"m11 17 2 2a1 1 0 1 0 3-3\" /> <path d=\"m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.88-3.88a3 3 0 0 0-4.24 0l-.88.88a1 1 0 1 1-3-3l2.81-2.81a5.79 5.79 0 0 1 7.06-.87l.47.28a2 2 0 0 0 1.42.25L21 4\" /> <path d=\"m21 3 1 11h-2\" /> <path d=\"M3 3 2 14l6.5 6.5a1 1 0 1 0 3-3\" /> <path d=\"M3 4h8\" /></g>",
        "scale":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M12 3v18\" /> <path d=\"m19 8 3 8a5 5 0 0 1-6 0zV7\" /> <path d=\"M3 7h1a17 17 0 0 0 8-2 17 17 0 0 0 8 2h1\" /> <path d=\"m5 8 3 8a5 5 0 0 1-6 0zV7\" /> <path d=\"M7 21h10\" /></g>",
        "landmark":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M10 18v-7\" /> <path d=\"M11.119 2.205a2 2 0 0 1 1.762 0l7.84 3.846A.5.5 0 0 1 20.5 7h-17a.5.5 0 0 1-.22-.949z\" /> <path d=\"M14 18v-7\" /> <path d=\"M18 18v-7\" /> <path d=\"M3 22h18\" /> <path d=\"M6 18v-7\" /></g>",
        "languages":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"m5 8 6 6\" /> <path d=\"m4 14 6-6 2-3\" /> <path d=\"M2 5h12\" /> <path d=\"M7 2h1\" /> <path d=\"m22 22-5-10-5 10\" /> <path d=\"M14 18h6\" /></g>",
        "quote":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M16 3a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2 1 1 0 0 1 1 1v1a2 2 0 0 1-2 2 1 1 0 0 0-1 1v2a1 1 0 0 0 1 1 6 6 0 0 0 6-6V5a2 2 0 0 0-2-2z\" /> <path d=\"M5 3a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2 1 1 0 0 1 1 1v1a2 2 0 0 1-2 2 1 1 0 0 0-1 1v2a1 1 0 0 0 1 1 6 6 0 0 0 6-6V5a2 2 0 0 0-2-2z\" /></g>",
        "plus":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M5 12h14\" /> <path d=\"M12 5v14\" /></g>",
        "check":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M20 6 9 17l-5-5\" /></g>",
        "x":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M18 6 6 18\" /> <path d=\"m6 6 12 12\" /></g>",
        "arrow-right":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M5 12h14\" /> <path d=\"m12 5 7 7-7 7\" /></g>",
        "move-right":
            "<g fill=\"none\" stroke=\"url(#c)\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M18 8L22 12L18 16\" /> <path d=\"M2 12H22\" /></g>",
    },
}

# Orden de rol sugerido (portada → puente → cierre) por categoría.
ORDEN = {
    "cybersec": ['shield-alert', 'lock-keyhole', 'fingerprint', 'scan-face', 'crosshair', 'siren', 'triangle-alert', 'user-x', 'badge-check', 'shield-off', 'key-round', 'bug-off', 'door-closed', 'mail-warning', 'link-2-off', 'biohazard', 'skull', 'scan-line', 'shield-plus', 'file-lock', 'user-check', 'alert-octagon', 'shield-ban', 'venetian-mask', 'footprints', 'key-square', 'shield-question', 'file-warning'],
    "dev": ['terminal', 'git-branch', 'code-xml', 'braces', 'package', 'workflow', 'test-tube', 'binary', 'regex', 'component', 'database', 'cpu', 'refresh-cw', 'square-function', 'file-code', 'boxes', 'flask-conical', 'wrench', 'cog', 'variable', 'git-merge', 'git-pull-request', 'git-fork', 'repeat', 'play', 'power', 'blocks', 'puzzle', 'keyboard', 'monitor-cog', 'table', 'grid-3x3', 'layers', 'file-terminal', 'list-checks', 'mouse-pointer-click'],
    "ai": ['brain-circuit', 'sparkles', 'bot', 'network', 'wand-sparkles', 'brain-cog', 'atom', 'orbit', 'cpu', 'microchip', 'scan-eye', 'message-square-code', 'audio-waveform', 'image', 'scan-text', 'telescope', 'satellite', 'antenna', 'radio', 'waves', 'waypoints', 'spline', 'activity', 'gauge', 'sigma', 'infinity', 'combine', 'merge', 'focus', 'bot-message-square', 'scan-search', 'search'],
    "infra": ['server', 'network', 'cloud', 'globe', 'router', 'radio-tower', 'signal', 'wifi', 'ethernet-port', 'cable', 'plug-zap', 'cpu', 'memory-stick', 'microchip', 'monitor', 'gauge', 'activity', 'trending-up', 'container', 'boxes', 'package', 'warehouse', 'factory', 'building-2', 'map', 'route', 'navigation', 'compass', 'satellite-dish', 'battery-charging', 'zap', 'thermometer', 'power', 'workflow', 'waypoints', 'hard-drive', 'database', 'cloud-cog', 'server-cog', 'server-crash'],
    "genericos": ['rocket', 'target', 'trophy', 'medal', 'award', 'star', 'flame', 'zap', 'lightbulb', 'book-open', 'graduation-cap', 'map', 'compass', 'route', 'flag', 'badge-check', 'circle-check', 'circle-x', 'triangle-alert', 'info', 'circle-help', 'arrow-up-right', 'external-link', 'download', 'upload', 'share-2', 'bookmark', 'heart', 'thumbs-up', 'clock', 'calendar', 'hash', 'gift', 'party-popper', 'megaphone', 'sparkles', 'crown', 'gem', 'hourglass', 'timer', 'palette', 'pencil', 'pen-tool', 'scissors', 'wrench', 'cog', 'search', 'filter', 'sliders-horizontal', 'users', 'user-plus', 'message-square', 'mail', 'phone', 'bell', 'tag', 'ticket', 'wallet', 'credit-card', 'briefcase', 'building', 'home', 'puzzle', 'blocks', 'smile', 'handshake', 'scale', 'landmark', 'languages', 'quote', 'plus', 'check', 'x', 'arrow-right', 'move-right'],
}
