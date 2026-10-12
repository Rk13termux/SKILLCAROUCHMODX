"""Bloques de contenido para carruseles de CIBERSEGURIDAD.

Educativo y defensivo: explican qué es, cómo se detecta y cómo se defiende.
Sin payloads ejecutables, sin pasos para dañar, sin datos inventados.
"""

COBERTURA = (
    {
        "titulo": "Qué es {tema}, sin ruido",
        "cuerpo": "Definición corta: qué es, dónde aparece y por qué te afecta "
                  "aunque no seas el objetivo directo.",
        "componente": {"tipo": "card-info",
                       "props": {"variante": "info", "titulo": "Definición",
                                 "cuerpo": "{tema} es un patrón que se explota "
                                           "cuando un sistema confía de más en "
                                           "la entrada. Entenderlo es el primer "
                                           "paso para defenderse."}},
    },
    {
        "titulo": "El error más común",
        "cuerpo": "Casi todos tratan el síntoma y no la causa: confiar en "
                  "validar sólo en el cliente o desactivar el check «por ahora».",
        "componente": None,
    },
    {
        "titulo": "Cómo se detecta",
        "cuerpo": "Mirá las señales: anomalías en logs, picos de errores 4xx/5xx "
                  "y accesos que no siguen el patrón normal del servicio.",
        "componente": {"tipo": "terminal",
                       "props": {"titulo": "señales · logs",
                                 "lines": [
                                     {"t": "cmd", "v": "grep -i error app.log | tail -3"},
                                     {"t": "out", "v": "2026-01-12 03:14 input rechazada"},
                                     {"t": "warn", "v": "patrón inusual desde una IP nueva"},
                                     {"t": "ok", "v": "alerta creada en el canal de guardia"}]}},
    },
    {
        "titulo": "Cómo se defiende",
        "cuerpo": "Validación en servidor, principio de mínimo privilegio y "
                  "actualizaciones al día. La defensa es capas, no un producto.",
        "componente": {"tipo": "diagram",
                       "props": {"titulo": "Defensa en capas",
                                 "nodos": [
                                     {"v": "Entrada", "sub": "validar en servidor", "tipo": "info"},
                                     {"v": "WAF / rate limit", "sub": "frenar lo obvio"},
                                     {"v": "App", "sub": "mínimo privilegio", "tipo": "ok"},
                                     {"v": "Logs", "sub": "detectar y reaccionar"}]}},
    },
    {
        "titulo": "Mito vs realidad",
        "cuerpo": "«Si no hay firewall, no hay ataque.» Falso: el ataque casi "
                  "siempre entra por una decisión de configuración.",
        "componente": {"tipo": "mitos",
                       "props": {"mito": "Un producto seguro te cubre de todo",
                                 "mito_sub": "Se compra una herramienta y se olvida la configuración",
                                 "realidad": "La seguridad es una práctica continua",
                                 "realidad_sub": "Parches, revisiones y mínimo privilegio"}},
    },
    {
        "titulo": "Tu checklist de 4 puntos",
        "cuerpo": "Imprimila mentalmente: lo básico resuelve la mayoría de los "
                  "incidentes reales.",
        "componente": {"tipo": "checklist",
                       "props": {"titulo": "Checklist defensiva", "items": [
                           "Actualiza dependencias y sistemas",
                           "Valida toda entrada también en servidor",
                           "Usa autenticación de factores múltiples",
                           "Revisa logs con frecuencia"]}},
    },
    {
        "titulo": "Antes de la alerta, la revisión",
        "cuerpo": "Un repaso corto semanal de accesos y parches detecta más que "
                  "cualquier herramienta cara comprada por urgencia.",
        "componente": None,
    },
)

HOOKS = (
    "Nadie audita esto hasta que falla",
    "Tu sistema confía demasiado en la entrada",
    "El ataque empieza por una decisión tuya",
    "Lo que no se revisa, se explota",
    "Configurar bien cuesta menos que responder",
)

SUBHOOKS = (
    "Ciberseguridad explicada en 7 ideas prácticas y aplicables hoy.",
    "Defensa real: qué revisar, qué medir y qué ignorar.",
    "Sin alarmismo: el panorama técnico, paso a paso.",
)
