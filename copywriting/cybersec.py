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
        "componente": {"tipo": "diff",
                       "props": {"titulo": "Validación: cliente vs servidor",
                                 "antes": "login(user_input)\n# confía en el formulario",
                                 "despues": "if valido(user_input):\n    login(user_input)"}},
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
        "componente": {"tipo": "quiz",
                       "props": {"pregunta": "¿Qué revisas primero un lunes?",
                                 "opciones": [
                                     {"v": "Logs de accesos raros"},
                                     {"v": "Parches pendientes", "ok": True},
                                     {"v": "Nada, todo verde"}]}},
    },
    {
        "titulo": "Así se ve un endpoint expuesto",
        "cuerpo": "Sin token, sin rol, respuesta completa. Si tu API responde "
                  "esto, el problema no es el atacante: es el diseño.",
        "componente": {"tipo": "http",
                       "props": {"metodo": "GET", "ruta": "/api/users/1",
                                 "codigo": "200 OK", "nota_estado": "sin auth",
                                 "response": '{\n  "id": 1,\n  "rol": "admin",\n  "email": "ceo@…"\n}'}},
    },
)

HOOKS = (
    "Tu API responde sin pedir permiso",
    "El ataque ya probó tu endpoint",
    "Tu sistema confía demasiado en la entrada",
    "Lo que no se revisa, se explota",
    "El log que ignoras es la pista",
    "Configurar bien cuesta menos que responder",
)

SUBHOOKS = (
    "Ciberseguridad en 7 ideas: qué revisar hoy mismo.",
    "Defensa real con comandos y capas, sin alarmismo.",
    "Del endpoint expuesto al checklist defensivo.",
)

# Portada: terminal con evidencia que duele (defensiva, de laboratorio).
HOOK_COMPS = (
    {"tipo": "terminal",
     "props": {"titulo": "evidencia · lab propio",
               "lines": [
                   {"t": "cmd", "v": "curl -s https://api.demo.local/users/1"},
                   {"t": "out", "v": "200 OK · perfil completo"},
                   {"t": "warn", "v": "sin token, sin rol, sin límite"},
                   {"t": "err", "v": "esto NO debería responder así"}]}},
    {"tipo": "terminal",
     "props": {"titulo": "escaneo · red propia",
               "lines": [
                   {"t": "cmd", "v": "nmap -sV 10.0.0.5"},
                   {"t": "out", "v": "22/tcp open · 80/tcp open · 3306/tcp open"},
                   {"t": "warn", "v": "base de datos visible desde fuera"},
                   {"t": "ok", "v": "3 servicios que revisar hoy"}]}},
)
