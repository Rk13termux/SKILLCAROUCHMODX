"""Componente qr: código QR para escanear desde la pantalla.

Cierra el funnel: el dominio (landing, curso, Telegram) escaneable directo.
Usa `segno` (pura Python) si está disponible; si no, degrada a aviso + URL.
"""

import html as _html

MAX_URL = 320


def _svg_qr(url, color="#000000"):
    import segno
    qr = segno.make(url, error="m")
    return qr.svg_inline(scale=1, dark=color, light=None, border=0)


def render(props, ctx, warnings=None):
    url = str(props.get("url") or props.get("link") or props.get("dominio")
              or props.get("texto") or "").strip()
    if not url:
        if warnings is not None:
            warnings.append("qr: falta `url`")
        return '<div class="qr qr--vacio">QR sin URL</div>'
    if len(url) > MAX_URL:
        if warnings is not None:
            warnings.append(f"qr: url de {len(url)} caracteres, se recorta")
        url = url[:MAX_URL]
    titulo = str(props.get("titulo") or "").strip()
    pie = str(props.get("pie") or props.get("caption") or "").strip()
    etiqueta = str(props.get("escanea") or "Escanea aquí").strip()
    color = str(props.get("color") or "#000000")
    try:
        svg = _svg_qr(url, color)
    except ImportError:
        if warnings is not None:
            warnings.append("qr: falta el paquete 'segno' "
                            "(pip install --user --break-system-packages segno)")
        return (f'<div class="qr"><div class="qr__vacio">'
                f'{_html.escape(url)}</div>'
                f'<div class="qr__pie">Falta el paquete segno</div></div>')
    except Exception as e:  # url inválida, contenido muy largo, etc.
        if warnings is not None:
            warnings.append(f"qr: no se pudo generar ({e})")
        return (f'<div class="qr"><div class="qr__vacio">'
                f'{_html.escape(url)}</div></div>')
    return (
        '<div class="qr">'
        + (f'<div class="qr__titulo">{_html.escape(titulo)}</div>' if titulo else "")
        + f'<div class="qr__caja">{svg}'
          f'<div class="qr__escanea">{_html.escape(etiqueta)}</div></div>'
        + (f'<div class="qr__pie">{_html.escape(pie)}</div>' if pie else "")
        + "</div>"
    )
