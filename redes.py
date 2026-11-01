"""Perfiles de red social: formato, densidad y recorte de slides.

Una red no es un formato suelto: es un **perfil** con formato, cuántos slides
conviene publicar, cuánto texto entra, cuántos hashtags van y qué zona de la
imagen tapa la UI de la app.

El builder no duplica lógica: hace una corrida normal del pipeline por perfil,
cambiando solo el formato (ya soportado) y el directorio de salida.

Sin `--redes` este módulo no interviene: la salida legacy no cambia.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Perfil:
    nombre: str
    formato: str                 # clave de tech_carousel.FORMATOS
    slides_min: int
    slides_max: int
    cuerpo_px: int               # tamaño de cuerpo base del slide
    palabras_slide: int          # techo de palabras por slide
    copy_min: int                # palabras del caption
    copy_max: int
    hashtags: int
    cta: str
    zona_segura: dict = field(default_factory=dict)
    nota: str = ""

    def recorta(self, n_fuente: int) -> bool:
        return n_fuente > self.slides_max


PERFILES = {
    "tiktok": Perfil(
        nombre="tiktok",
        formato="9:16",
        slides_min=6,
        slides_max=8,
        cuerpo_px=48,
        palabras_slide=25,
        copy_min=30,
        copy_max=50,
        hashtags=5,
        cta="serie",
        zona_segura={"top": 120, "bottom": 250, "right": 120},
        nota=("Photo Mode: la UI tapa la franja inferior y la columna derecha; "
              "el gancho tiene que estar en el slide 1."),
    ),
    "instagram": Perfil(
        nombre="instagram",
        formato="4:5",
        slides_min=7,
        slides_max=10,
        cuerpo_px=44,
        palabras_slide=45,
        copy_min=60,
        copy_max=95,
        hashtags=9,
        cta="comentar",
        zona_segura={"top": 60, "bottom": 60, "grid": 1080},
        nota=("La grilla del perfil recorta a 1:1: el texto crítico va dentro"
              " del cuadrado central de 1080×1080."),
    ),
    "facebook": Perfil(
        nombre="facebook",
        formato="4:5",
        slides_min=5,
        slides_max=6,
        cuerpo_px=46,
        palabras_slide=45,
        copy_min=60,
        copy_max=110,
        hashtags=5,
        cta="link",
        zona_segura={"top": 60, "bottom": 60, "margen": 0.08},
        nota=("No hay carrusel orgánico: se publica como multi-foto. Menos "
              "slides y CTA a link rinden mejor que pedir un comentario."),
    ),
}

ORDEN = ("tiktok", "instagram", "facebook")


def resolver_redes(valor):
    """'todas' | 'tiktok,instagram' | None → lista de perfiles en orden.

    Lanza ValueError si una red no existe (el CLI lo muestra como error).
    """
    if not valor:
        return []
    texto = str(valor).strip().lower()
    if texto in ("todas", "all", "*"):
        return list(ORDEN)
    pedidas = [p.strip() for p in texto.replace(";", ",").split(",") if p.strip()]
    if not pedidas:
        return []
    desconocidas = [p for p in pedidas if p not in PERFILES]
    if desconocidas:
        raise ValueError(
            f"red desconocida: {', '.join(desconocidas)} "
            f"(válidas: {', '.join(ORDEN)}, o 'todas')")
    # Orden canónico y sin repetidos: el render es determinista.
    return [r for r in ORDEN if r in pedidas]


def perfil(red):
    clave = str(red).strip().lower()
    if clave not in PERFILES:
        raise ValueError(f"red desconocida: {red}")
    return PERFILES[clave]


def _muestrear(items, cuantos):
    """Submuestra determinista de `items` conservando el primero y el último."""
    if cuantos <= 0:
        return []
    if cuantos >= len(items):
        return list(items)
    if cuantos == 1:
        return [items[0]]
    paso = (len(items) - 1) / (cuantos - 1)
    vistos, salida = set(), []
    for i in range(cuantos):
        idx = round(i * paso)
        if idx not in vistos:
            vistos.add(idx)
            salida.append(items[idx])
    return salida


def seleccion(red, n_fuente, forzado=None):
    """Qué slides fuente se usan en esta red.

    Devuelve `(indices, fuera)` con índices 1-based y en orden.

    - Portada (1), puente (N-1) y cierre (N) siempre entran.
    - El contenido (2..N-2) se submuestrea parejo si sobra.
    """
    if n_fuente < 3:
        raise ValueError("la fuente necesita al menos 3 slides")
    p = perfil(red)
    objetivo = forzado if forzado else min(n_fuente, p.slides_max)
    if objetivo > n_fuente:
        objetivo = n_fuente
    if objetivo < 3:
        objetivo = 3

    todos = list(range(1, n_fuente + 1))
    if objetivo >= n_fuente:
        return todos, []

    contenido = list(range(2, n_fuente - 1))     # 2..N-2
    cuantos = max(0, objetivo - 3)               # 1 portada + puente + cierre
    elegidos = _muestrear(contenido, cuantos)

    indices = [1] + elegidos + ([n_fuente - 1] if n_fuente > 2 else []) + [n_fuente]
    # Sin duplicados y en orden (fuentes chicas pueden solapar puente/cierre).
    vistos, limpio = set(), []
    for i in indices:
        if i not in vistos:
            vistos.add(i)
            limpio.append(i)
    fuera = [i for i in todos if i not in vistos]
    return limpio, fuera


def planear(n_fuente, redes, forzados=None):
    """Plan por red: cuántos slides, qué formato y qué queda afuera."""
    forzados = forzados or {}
    plan = []
    for red in redes:
        p = perfil(red)
        forzado = forzados.get(red)
        indices, fuera = seleccion(red, n_fuente, forzado)
        avisos = []
        if fuera:
            avisos.append(
                f"{len(fuera)} slide(s) quedan fuera por el perfil "
                f"({p.slides_max} máx): {', '.join(f'slide-{i:02d}' for i in fuera)}")
        if len(indices) < p.slides_min:
            avisos.append(
                f"el perfil pide mínimo {p.slides_min} slides y quedan "
                f"{len(indices)}: el carrusel puede quedar corto")
        plan.append({
            "red": red,
            "formato": p.formato,
            "n": len(indices),
            "indices": indices,
            "fuera": fuera,
            "perfil": p,
            "avisos": avisos,
        })
    return plan
