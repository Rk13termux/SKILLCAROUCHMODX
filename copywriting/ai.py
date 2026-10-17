"""Bloques de contenido para carruseles de INTELIGENCIA ARTIFICIAL."""

COBERTURA = (
    {
        "titulo": "Qué es {tema} de verdad",
        "cuerpo": "Sin humo: qué hace el sistema, qué esperar de él y dónde "
                  "empieza a fallar. Toda herramienta tiene techo.",
        "componente": {"tipo": "card-info",
                       "props": {"variante": "info", "titulo": "Definición",
                                 "cuerpo": "{tema} organiza información para "
                                           "reducir trabajo repetitivo. Sigue "
                                           "siendo una herramienta, no una "
                                           "decisión por ti."}},
    },
    {
        "titulo": "Cómo funciona por dentro",
        "cuerpo": "Entrada, proceso y salida. Si no ves el proceso, no puedes "
                  "entender los errores del resultado.",
        "componente": {"tipo": "diagram",
                       "props": {"titulo": "Flujo de un sistema de IA",
                                 "nodos": [
                                     {"v": "Pregunta clara", "sub": "contexto y restricciones", "tipo": "info"},
                                     {"v": "Modelo", "sub": "patrones aprendidos"},
                                     {"v": "Respuesta", "sub": "verificar antes de usar", "tipo": "ok"}]}},
    },
    {
        "titulo": "Un prompt que funciona",
        "cuerpo": "Rol, contexto, tarea y formato. Cuatro bloques y el "
                  "resultado cambia por completo.",
        "componente": {"tipo": "code",
                       "props": {"lenguaje": "generic",
                                 "titulo": "prompt",
                                 "codigo": "Rol: revisor de código\n"
                                           "Contexto: repo Python, equipo de 3\n"
                                           "Tarea: señala riesgos, no estilo\n"
                                           "Formato: lista priorizada",
                                 "notas": "Cuatro bloques: rol, contexto, tarea, formato."}},
    },
    {
        "titulo": "El error más caro",
        "cuerpo": "Confiar en la primera respuesta. Verificar es parte del "
                  "trabajo, no un paso opcional.",
        "componente": {"tipo": "faq",
                       "props": {"titulo": "Verificar, siempre",
                                 "items": [
                                     {"q": "¿Qué se verifica primero?",
                                      "a": "Cifras, nombres propios y código que vas a ejecutar."},
                                     {"q": "¿Y si suena muy seguro?",
                                      "a": "Peor: la seguridad del tono no predice la verdad."}]}},
    },
    {
        "titulo": "Mito vs realidad",
        "cuerpo": "La IA no reemplaza el criterio: lo acelera. El que decide "
                  "sigue siendo humano.",
        "componente": {"tipo": "mitos",
                       "props": {"mito": "El modelo siempre tiene razón",
                                 "mito_sub": "Si suena seguro, debe ser cierto",
                                 "realidad": "Suena seguro incluso cuando falla",
                                 "realidad_sub": "Verifica datos y números siempre"}},
    },
    {
        "titulo": "Checklist para usar IA en tu trabajo",
        "cuerpo": "Rutina corta que evita la mayoría de los errores repetidos.",
        "componente": {"tipo": "checklist",
                       "props": {"titulo": "Uso responsable", "items": [
                           "Da contexto completo en cada petición",
                           "Verifica cifras y nombres propios",
                           "No pegues datos sensibles",
                           "Revisa el código antes de ejecutarlo"]}},
    },
    {
        "titulo": "El valor está en tu criterio",
        "cuerpo": "La herramienta multiplica lo que ya sabes hacer; no crea "
                  "criterio donde no lo hay.",
        "componente": {"tipo": "quote",
                       "props": {"texto": "La IA multiplica tu criterio; no lo crea. Úsala para ir más rápido, no para pensar menos.",
                                 "autor": "CHMODX", "rol": "línea editorial"}},
    },
)

HOOKS = (
    "Tu prompt vago tiene respuesta vaga",
    "La IA no piensa: predice",
    "Pegaste datos sensibles al chat",
    "Confías en una respuesta sin verificar",
    "El modelo olvidó tu contexto a mitad",
    "Criterio humano, velocidad de máquina",
)

SUBHOOKS = (
    "IA en 7 ideas para usarla con criterio, no con fe.",
    "Del prompt vago al sistema que sí responde.",
    "Menos humo, más práctica con modelos y agentes.",
)

# Portada: terminal con el fallo típico de contexto.
HOOK_COMPS = (
    {"tipo": "terminal",
     "props": {"titulo": "prompt · intento 1",
               "lines": [
                   {"t": "cmd", "v": "prompt: «hazlo bien»"},
                   {"t": "err", "v": "respuesta genérica, 0 criterios"},
                   {"t": "cmd", "v": "prompt: rol + contexto + formato"},
                   {"t": "ok", "v": "respuesta usable al primer intento"}]}},
    {"tipo": "terminal",
     "props": {"titulo": "contexto · límite",
               "lines": [
                   {"t": "cmd", "v": "pegar documento de 200 páginas"},
                   {"t": "warn", "v": "ventana llena: olvidó el inicio"},
                   {"t": "ok", "v": "resume por partes, verifica al final"}]}},
)
