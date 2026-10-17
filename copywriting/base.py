"""Base de copywriting tech: palabra CTA determinista + QA de dialecto.

Fuente de verdad ÚNICA de la palabra del CTA: tech_carousel.py y
generar_copy_tech.py importan de aquí, así el Slide N, el caption.txt y el
copy-redes.md piden siempre la misma palabra.
"""

import re
import unicodedata
import zlib

# ── Palabra CTA: familias por vertical ─────────────────────────────
# Cada familia tiene 4 palabras para que dos temas vecinos no repitan el
# mismo token (repetir el mismo verbo de comentario en todas las
# publicaciones es lo que dispara el clasificador de spam). La elección
# dentro de la familia es determinista (crc32 del slug).

PALABRAS_CLAVE_POR_TEMA = {
    # DEFENSA (ciberseguridad defensiva, appsec, blue team)
    "ciber": "DEFENSA", "seguridad": "DEFENSA", "segurid": "DEFENSA",
    "vulner": "DEFENSA", "pentest": "DEFENSA", "hardening": "DEFENSA",
    "firewall": "DEFENSA", "defensa": "DEFENSA", "zero-trust": "DEFENSA",
    "zerotrust": "DEFENSA", "owasp": "DEFENSA", "bounty": "DEFENSA",
    "2fa": "DEFENSA", "mfa": "DEFENSA", "cifrado": "DEFENSA",

    # AMENAZA (threats, incidentes, análisis ofensivo)
    "phishing": "AMENAZA", "ransom": "AMENAZA", "malware": "AMENAZA",
    "ataque": "AMENAZA", "atac": "AMENAZA", "exploit": "AMENAZA",
    "cve": "AMENAZA", "amenaza": "AMENAZA", "riesgo": "AMENAZA",
    "forensic": "AMENAZA", "incidente": "AMENAZA", "ddos": "AMENAZA",
    "injection": "AMENAZA", "inyecc": "AMENAZA", "xss": "AMENAZA",
    "csrf": "AMENAZA", "xxe": "AMENAZA", "deserializ": "AMENAZA",
    "buffer": "AMENAZA", "fuga": "AMENAZA", "credencial": "AMENAZA",

    # CODIGO (programación, testing, calidad)
    "python": "CODIGO", "javascript": "CODIGO", "java": "CODIGO",
    "rust": "CODIGO", "golang": "CODIGO", "git": "CODIGO",
    "commit": "CODIGO", "test": "CODIGO", "testing": "CODIGO",
    "codigo": "CODIGO", "código": "CODIGO", "refactor": "CODIGO",
    "debug": "CODIGO", "linter": "CODIGO", "funcion": "CODIGO",
    "función": "CODIGO", "repositorio": "CODIGO", "github": "CODIGO",

    # ARQUITECTURA (diseño, patrones, sistemas)
    "arquitectura": "ARQUITECTURA", "patron": "ARQUITECTURA",
    "patrón": "ARQUITECTURA", "diseno": "ARQUITECTURA",
    "diseño": "ARQUITECTURA", "algoritmo": "ARQUITECTURA",
    "api": "ARQUITECTURA", "rest": "ARQUITECTURA", "microservicio": "ARQUITECTURA",
    "base-de-datos": "ARQUITECTURA", "database": "ARQUITECTURA",

    # MODELO (IA, LLMs, prompts, agentes)
    "ia": "MODELO", "inteligencia": "MODELO", "llm": "MODELO",
    "gpt": "MODELO", "prompt": "MODELO", "agente": "MODELO",
    "modelo": "MODELO", "entrena": "MODELO", "fine-tun": "MODELO",
    "transformer": "MODELO", "guardrail": "MODELO", "mcp": "MODELO",

    # DATOS (RAG, embeddings, pipelines, métricas)
    "rag": "DATOS", "embedding": "DATOS", "vector": "DATOS",
    "token": "DATOS", "datos": "DATOS", "dataframe": "DATOS",
    "metrica": "DATOS", "métrica": "DATOS", "eval": "DATOS",
    "dashboard": "DATOS", "analitica": "DATOS", "analítica": "DATOS",

    # DEPLOY (infra, DevOps, CI/CD, cloud)
    "deploy": "DEPLOY", "docker": "DEPLOY", "kubernetes": "DEPLOY",
    "k8s": "DEPLOY", "pipeline": "DEPLOY", "ci-cd": "DEPLOY",
    "nube": "DEPLOY", "aws": "DEPLOY", "terraform": "DEPLOY",
    "ansible": "DEPLOY", "sre": "DEPLOY", "backup": "DEPLOY",

    # RED (redes, protocolos, topología)
    "red": "RED", "redes": "RED", "dns": "RED", "tcp": "RED",
    "udp": "RED", "subred": "RED", "vpn": "RED", "nginx": "RED",
    "balanceo": "RED", "cluster": "RED", "servidor": "RED",

    # RENDIMIENTO (performance, escalado, optimización)
    "rendimiento": "RENDIMIENTO", "performance": "RENDIMIENTO",
    "latencia": "RENDIMIENTO", "escala": "RENDIMIENTO",
    "cache": "RENDIMIENTO", "optimiz": "RENDIMIENTO",
    "carga": "RENDIMIENTO", "memoria": "RENDIMIENTO",
}

_STOPWORDS_CTA = {
    "de", "la", "el", "los", "las", "y", "a", "con", "para", "como", "en",
    "del", "al", "que", "lo", "un", "una", "tu", "su", "contra", "hacia",
    "por", "e", "o", "sobre", "sin", "ser", "estar", "hay",
}

_CLAVES_ORDENADAS = sorted(PALABRAS_CLAVE_POR_TEMA, key=len, reverse=True)

_FAMILIAS_CTA = {
    "DEFENSA": ("DEFENSA", "ESCUDO", "HARDENING", "FORTALEZA"),
    "AMENAZA": ("AMENAZA", "RIESGO", "HALLAZGO", "FALLO"),
    "CODIGO": ("CODIGO", "COMMIT", "REFACTOR", "TEST"),
    "ARQUITECTURA": ("ARQUITECTURA", "MODULO", "PATRON", "DISENO"),
    "MODELO": ("MODELO", "PROMPT", "AGENTE", "RUTINA"),
    "DATOS": ("DATOS", "INDICE", "CACHE", "EMBEDDING"),
    "DEPLOY": ("DEPLOY", "PIPELINE", "ROLLBACK", "RELEASE"),
    "RED": ("RED", "NODO", "LATENCIA", "PUERTA"),
    "RENDIMIENTO": ("RENDIMIENTO", "ESCALA", "PERFIL", "CARGA"),
}


def normalizar(texto):
    """Minúsculas + sin acentos, para matchear claves sin tilde."""
    return "".join(
        c for c in unicodedata.normalize("NFKD", (texto or "").lower())
        if not unicodedata.combining(c)
    )


def _indice_estable(semilla, modulo):
    if modulo <= 0:
        return 0
    return zlib.crc32(normalizar(semilla).encode("utf-8")) % modulo


def _palabra_cta_valida(palabra):
    norm = normalizar(palabra).replace(" ", "")
    return len(norm) >= 3 and norm.isalpha()


def seleccionar_palabra_clave(tema_slug, palabra_defecto="CLAVE"):
    """Gana la PRIMERA palabra del slug que matchea; dentro, el match más largo."""
    norm = normalizar(tema_slug)
    for palabra in re.findall(r"[a-z0-9]+", norm):
        for key in _CLAVES_ORDENADAS:
            if key in palabra:
                familia = PALABRAS_CLAVE_POR_TEMA[key]
                pool = _FAMILIAS_CTA.get(familia, (familia,))
                return pool[_indice_estable(tema_slug, len(pool))]
    return palabra_defecto


def _primera_palabra_significativa(slug, cantidad=1):
    palabras = re.findall(r"[A-Za-zÁÉÍÓÚáéíóúÑñ]+",
                          (slug or "").replace("-", " "))
    claves = [p for p in palabras if normalizar(p) not in _STOPWORDS_CTA] or palabras
    claves = [p for p in claves if _palabra_cta_valida(p)]
    return " ".join(claves[:cantidad]).upper() if claves else ""


def resolver_cta_palabra(tema_slug, forzado=None, palabra_defecto="CLAVE"):
    """Cadena: --cta-palabra → diccionario → primera palabra → defecto."""
    if forzado and str(forzado).strip():
        return str(forzado).strip().upper()
    por_diccionario = seleccionar_palabra_clave(tema_slug, "")
    if por_diccionario:
        return por_diccionario
    return _primera_palabra_significativa(tema_slug, 1) or palabra_defecto


# ── QA de dialecto: tuteo neutro latino ────────────────────────────

VOSEO = {
    "guardá": "guarda", "contame": "cuéntame", "mirá": "mira",
    "tenés": "tienes", "querés": "quieres", "podés": "puedes",
    "hacé": "haz", "creé": "crea", "probá": "prueba", "usá": "usa",
    "escribí": "escribe", "pensá": "piensa", "fijá": "fija",
    "decí": "di", "agarrá": "agarra", "dejá": "deja", "poné": "pone",
    "traé": "trae", "pasá": "pasa", "seguí": "sigue",
}
REGIONALISMOS = {
    "laburo": "trabajo", "pibe": "chico", "che": "oye", "copado": "bueno",
    "re lindo": "muy lindo", "bondi": "autobús", "dpto": "departamento",
    "depto": "departamento", "bárbaro": "genial",
}
RITUALES = {
    "mate": "té", "yerba": "té", "asado": "comida",
    "dulce de leche": "crema", "chamuyo": "charla",
}

_RE_VOSEO = re.compile(
    r"\b(guardá|contame|mirá|tenés|querés|podés|hacé|creé|probá|usá|"
    r"escribí|pensá|fijá|decí|agarrá|dejá|poné|traé|seguí)\b", re.I)


def corregir_dialecto(texto):
    """tuteo-latam-neutro: devuelve (texto_corregido, cambios)."""
    if not texto:
        return texto, 0
    original = texto
    for viejo, nuevo in {**VOSEO, **REGIONALISMOS, **RITUALES}.items():
        texto = re.sub(rf"\b{re.escape(viejo)}\b", nuevo, texto, flags=re.I)
    cambios = 1 if texto != original else 0
    return texto, cambios


def voseo_presente(texto):
    return bool(_RE_VOSEO.search(texto or ""))


def regionalismos_presentes(texto):
    t = normalizar(texto or "")
    return [k for k in REGIONALISMOS
            if re.search(rf"\b{re.escape(normalizar(k))}\b", t)]


def rituales_presentes(texto):
    t = normalizar(texto or "")
    return [k for k in RITUALES
            if re.search(rf"\b{re.escape(normalizar(k))}\b", t)]


# ── QA de contenido educativo ──────────────────────────────────────

# Payloads/instrucciones que NO deben aparecer en el copy de un carrusel
# educativo (responsable por diseño).
PATRONES_BLOQUEADOS = (
    r"rm\s+-rf\s+/", r"\bdrop\s+table\b", r";\s*shutdown\b",
    r"--privilege escalation paso a paso", r"\bkeylogger\b.{0,20}código",
    r"c2\s+del\s+atacante", r"para\s+robar\s+credenciales",
    r"víctimas\s+reales", r"\bbotnet\s+propia\b",
)


def contenido_responsable(texto):
    """Devuelve lista de infracciones (vacía = OK)."""
    t = (texto or "").lower()
    return [p for p in PATRONES_BLOQUEADOS if re.search(p, t)]


def datos_inventados(texto):
    """Aserciones numéricas sin fuente: las marcas para revisión manual."""
    return re.findall(r"\b\d{1,3}(?:\.\d+)?\s?%", texto or "")
