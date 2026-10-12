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
        "componente": {"tipo": "code",
                       "props": {"lenguaje": "python",
                                 "codigo": "def procesar(datos):\n"
                                           "    limpio = [d for d in datos if d]\n"
                                           "    return sorted(limpio, key=lambda d: d[0])",
                                 "notas": "Una función, una responsabilidad."}},
    },
    {
        "titulo": "El error que todos cometen",
        "cuerpo": "Copiar la solución sin entender el contrato: qué entrada "
                  "acepta, qué garantiza y qué lanza cuando falla.",
        "componente": None,
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
        "componente": None,
    },
)

HOOKS = (
    "Escribe código que se explica solo",
    "Tu función hace demasiado y no lo ves",
    "El bug no estaba donde buscabas",
    "Más tests no siempre es mejor",
    "El código más rápido es el que no escribes",
)

SUBHOOKS = (
    "Programación en 7 ideas que ahorran horas de depuración.",
    "Decisiones de código con criterio, no por moda.",
    "Menos trucos, más contratos claros en tu código.",
)
