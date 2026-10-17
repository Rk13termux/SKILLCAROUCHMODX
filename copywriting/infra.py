"""Bloques de contenido para carruseles de INFRAESTRUCTURA / REDES / DEVOPS."""

COBERTURA = (
    {
        "titulo": "Qué pasa por debajo de {tema}",
        "cuerpo": "El mapa mental: qué componentes toca, en qué orden y qué "
                  "pasa cuando uno de ellos se cae.",
        "componente": {"tipo": "diagram",
                       "props": {"titulo": "Recorrido de una petición",
                                 "nodos": [
                                     {"v": "Cliente", "sub": "navegador o app", "tipo": "info"},
                                     {"v": "DNS + CDN", "sub": "resolver y acercar"},
                                     {"v": "Balanceador", "sub": "repartir carga"},
                                     {"v": "Servicio", "sub": "aplicación viva", "tipo": "ok"}]}},
    },
    {
        "titulo": "El comando que necesitas",
        "cuerpo": "Diagnóstico en tres líneas. Correlo primero y decide "
                  "después: sin datos no hay incidente.",
        "componente": {"tipo": "terminal",
                       "props": {"titulo": "diagnóstico",
                                 "lines": [
                                     {"t": "cmd", "v": "df -h && free -m"},
                                     {"t": "out", "v": "/dev/sda1   48G   31G   15G  68% /"},
                                     {"t": "warn", "v": "memoria: 82% en uso"},
                                     {"t": "ok", "v": "siguiente: revisar procesos"}]}},
    },
    {
        "titulo": "El error clásico",
        "cuerpo": "Escalar agregando máquinas sin mirar el cuello de botella "
                  "real: casi siempre es una cola o una consulta.",
        "componente": {"tipo": "layers",
                       "props": {"titulo": "Dónde buscar el cuello",
                                 "capas": [
                                     {"v": "Red", "sub": "latencia y DNS"},
                                     {"v": "App", "sub": "colas y reintentos", "tipo": "api"},
                                     {"v": "Base de datos", "sub": "consultas lentas", "tipo": "db"}]}},
    },
    {
        "titulo": "Configuración segura",
        "cuerpo": "Los defaults rara vez son los de producción. Revisá tiempos "
                  "de espera, límites y quién puede conectar.",
        "componente": {"tipo": "code",
                       "props": {"lenguaje": "bash",
                                 "codigo": "# endurecer el acceso\n"
                                           "ssh: PasswordAuthentication no\n"
                                           "firewall: abrir sólo 443\n"
                                           "logs: retención 30 días",
                                 "notas": "Cada línea es una decisión revisable."}},
    },
    {
        "titulo": "Antes / después del monitoreo",
        "cuerpo": "Sin métricas discutes opiniones; con métricas discutes "
                  "hechos y arreglas más rápido.",
        "componente": {"tipo": "card-compare",
                       "props": {"titulo": "Operar sin adivinar",
                                 "cols": [
                                     {"nombre": "Sin observabilidad",
                                      "badge": "ANTES",
                                      "items": [
                                          {"ok": False, "v": "Te enteras por el usuario"},
                                          {"ok": False, "v": "Causa adivinada"},
                                          {"ok": False, "v": "Rollback lento"}]},
                                     {"nombre": "Con observabilidad",
                                      "badge": "DESPUÉS",
                                      "items": [
                                          {"ok": True, "v": "Alerta automática"},
                                          {"ok": True, "v": "Causa en los logs"},
                                          {"ok": True, "v": "Rollback en minutos"}]}]}},
    },
    {
        "titulo": "Checklist de despliegue",
        "cuerpo": "La rutina corta que convierte un deploy en aburrido, que es "
                  "exactamente lo que se busca.",
        "componente": {"tipo": "checklist",
                       "props": {"titulo": "Deploy seguro", "items": [
                           "Prueba en staging con datos reales",
                           "Rollback probado antes de publicar",
                           "Métricas visibles durante el cambio",
                           "Aviso al equipo antes de empezar"]}},
    },
    {
        "titulo": "Aburrido es sinónimo de fiable",
        "cuerpo": "La infraestructura buena no se nota: no suena, no despierta "
                  "a nadie y no aparece en ningún chat de urgencias.",
        "componente": {"tipo": "pipeline",
                       "props": {"titulo": "Deploy aburrido = deploy bueno",
                                 "etapas": [
                                     {"v": "test", "estado": "ok"},
                                     {"v": "staging", "estado": "ok"},
                                     {"v": "canaria 10%", "estado": "ok"},
                                     {"v": "prod", "estado": "ok"}]}},
    },
)

HOOKS = (
    "Tu disco se llena esta noche",
    "El deploy falla donde no miraste",
    "Escalar sin medir es caro",
    "El pod lleva 14 restarts",
    "Operar sin métricas es operar a ciegas",
    "El cuello de botella no es donde crees",
)

SUBHOOKS = (
    "Infraestructura en 7 ideas para operar sin sorpresas.",
    "Del disco lleno al deploy aburrido.",
    "De la petición al log: cómo se sostiene un sistema.",
)

# Portada: terminal con el incidente que todos temen.
HOOK_COMPS = (
    {"tipo": "terminal",
     "props": {"titulo": "guardia · 03:14",
               "lines": [
                   {"t": "cmd", "v": "df -h /var && kubectl get pods"},
                   {"t": "warn", "v": "/var al 98% · logs sin rotar"},
                   {"t": "err", "v": "api-7d9f CrashLoopBackOff · 14 restarts"},
                   {"t": "ok", "v": "todo esto se veía venir"}]}},
    {"tipo": "terminal",
     "props": {"titulo": "diagnóstico · 3 líneas",
               "lines": [
                   {"t": "cmd", "v": "uptime && free -m | tail -1"},
                   {"t": "out", "v": "load 12.4 · memoria 94% en uso"},
                   {"t": "warn", "v": "escalar aquí es tirar dinero"},
                   {"t": "ok", "v": "primero: la cola, después: el cluster"}]}},
)
