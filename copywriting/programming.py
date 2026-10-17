"""Bloques de contenido para carruseles de PROGRAMACIÓN."""

COBERTURA = (
    {
        "titulo": "Qué hace {tema}",
        "cuerpo": "La idea en una frase y el problema que resuelve. Si no "
                  "sabés qué problema resuelve, no es la herramienta correcta.",
        "componente": {"tipo": "card-info",
                       "props": {"variante": "info", "titulo": "Contexto",
                                 "cuerpo": "{tema} se usa cuando el costo de "
                                           "cambiarlo después es mayor que el "
                                           "costo de entenderlo ahora."}},
    },
    {
        "titulo": "El patrón en código",
        "cuerpo": "Pocas líneas, una responsabilidad. Código que se lee solo "
                  "gana siempre al código que presume.",
        "componente": {"tipo": "editor",
                       "props": {"archivo": "patron.py", "lenguaje": "python",
                                 "codigo": "def procesar(datos):\n"
                                           "    limpio = [d for d in datos if d]\n"
                                           "    return sorted(limpio, key=lambda d: d[0])",
                                 "salida": "$ python3 patron.py\n"
                                           "3 passed in 0.02s"}},
    },
    {
        "titulo": "El error que todos cometen",
        "cuerpo": "Copiar la solución sin entender el contrato: qué entrada "
                  "acepta, qué garantiza y qué lanza cuando falla.",
        "componente": {"tipo": "faq",
                       "props": {"titulo": "El error, diseccionado",
                                 "items": [
                                     {"q": "¿Por qué pasa?",
                                      "a": "Stack Overflow responde rápido; el contrato del código tarda en leerse."},
                                     {"q": "¿Cómo se evita?",
                                      "a": "Lee la firma y los casos borde antes de pegar. Un minuto ahorra una hora."}]}},
    },
    {
        "titulo": "Cómo se prueba",
        "cuerpo": "Si no puedes probarlo en un minuto, el diseño te lo está "
                  "pidiendo a gritos. Casos felices y caso de error.",
        "componente": {"tipo": "terminal",
                       "props": {"titulo": "tests · local",
                                 "lines": [
                                     {"t": "cmd", "v": "pytest -q tests/test_core.py"},
                                     {"t": "out", "v": "..F"},
                                     {"t": "err", "v": "1 falló: entrada vacía sin cubrir"},
                                     {"t": "ok", "v": "arreglá el caso borde, no el test"}]}},
    },
    {
        "titulo": "Antes y después",
        "cuerpo": "La refactorización buena no cambia el comportamiento: cambia "
                  "lo caro que es cambiarlo la próxima vez.",
        "componente": {"tipo": "card-compare",
                       "props": {"titulo": "Código que envejece bien",
                                 "cols": [
                                     {"nombre": "Rápido de escribir",
                                      "badge": "ANTES",
                                      "items": [
                                          {"ok": False, "v": "Mezcla lógica y datos"},
                                          {"ok": False, "v": "Sin tests claros"},
                                          {"ok": False, "v": "Cambios con miedo"}]},
                                     {"nombre": "Rápido de cambiar",
                                      "badge": "DESPUÉS",
                                      "items": [
                                          {"ok": True, "v": "Una responsabilidad"},
                                          {"ok": True, "v": "Contratos explícitos"},
                                          {"ok": True, "v": "Cambios predecibles"}]}]}},
    },
    {
        "titulo": "Tu checklist antes de commitear",
        "cuerpo": "Cuatro preguntas. Si alguna falla, el commit espera.",
        "componente": {"tipo": "checklist",
                       "props": {"titulo": "Pre-commit", "items": [
                           "¿Leerá esto alguien a las 3 a. m.?",
                           "¿Tiene test el caso borde?",
                           "¿El nombre dice qué hace?",
                           "¿El diff es de un solo tema?"]}},
    },
    {
        "titulo": "Lee primero, escribe después",
        "cuerpo": "La mitad de las funciones nuevas se evitan entendiendo qué "
                  "ya existe en el módulo.",
        "componente": {"tipo": "tree",
                       "props": {"titulo": "Explora antes de crear",
                                 "nodos": [
                                     {"v": "mi-app/", "tipo": "dir"},
                                     {"v": "core/", "depth": 1, "tipo": "dir"},
                                     {"v": "pagos.py", "depth": 2},
                                     {"v": "ya existe: reutilízalo", "depth": 2}]}},
    },
    {
        "titulo": "El repo detrás del tema",
        "cuerpo": "Todo lo de este carrusel vive en un repo: estrellas, "
                  "lenguajes y el comando para traerlo a tu máquina.",
        "componente": {"tipo": "card-repo",
                       "props": {"repo": "{short}/codigo", "desc": "Código del tema, listo para clonar.",
                                 "install": "git clone https://github.com/ejemplo/{short}.git",
                                 "badges": ["MIT", "docs"]}},
    },
)

HOOKS = (
    "Tu test en verde miente",
    "El bug no estaba donde buscabas",
    "Tu función hace demasiado y no lo ves",
    "Copiaste la solución sin leer el contrato",
    "El código más rápido es el que no escribes",
    "0.1 + 0.2 no es 0.3",
)

SUBHOOKS = (
    "Programación en 7 ideas que ahorran horas de depuración.",
    "Del test que miente al commit que envejece bien.",
    "Menos trucos, más contratos claros en tu código.",
)

# Portada: terminal con el fallo que todos reconocen.
HOOK_COMPS = (
    {"tipo": "terminal",
     "props": {"titulo": "tests · local",
               "lines": [
                   {"t": "cmd", "v": "pytest -q tests/"},
                   {"t": "out", "v": "47 passed en 2.1s"},
                   {"t": "err", "v": "1 failed: pago con centavos"},
                   {"t": "warn", "v": "el verde total escondía el caso borde"}]}},
    {"tipo": "terminal",
     "props": {"titulo": "python · repl",
               "lines": [
                   {"t": "cmd", "v": "python3 -c \"print(0.1 + 0.2)\""},
                   {"t": "out", "v": "0.30000000000000004"},
                   {"t": "warn", "v": "tu dinero no cabe en un float"},
                   {"t": "ok", "v": "Decimal existe por algo"}]}},
)
