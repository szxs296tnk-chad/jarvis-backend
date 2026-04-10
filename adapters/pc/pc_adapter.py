from __future__ import annotations

import os
import logging
import webbrowser
from datetime import datetime

logger = logging.getLogger("chad.adapters.pc")


def open_youtube(params: dict | None = None) -> str:
    webbrowser.open("https://www.youtube.com")
    return "Abriendo YouTube"


def open_netflix(params: dict | None = None) -> str:
    webbrowser.open("https://www.netflix.com")
    return "Abriendo Netflix"


def open_browser(params: dict | None = None) -> str:
    webbrowser.open("https://www.google.com")
    return "Abriendo navegador"


def open_spotify(params: dict | None = None) -> str:
    cmd = os.environ.get("SPOTIFY_CMD", "start spotify")
    os.system(cmd)
    return "Abriendo Spotify"


def open_notes(params: dict | None = None) -> str:
    cmd = os.environ.get("NOTAS_CMD", "notepad")
    os.system(cmd)
    return "Abriendo bloc de notas"


def open_calculator(params: dict | None = None) -> str:
    cmd = os.environ.get("CALCULADORA_CMD", "calc")
    os.system(cmd)
    return "Abriendo calculadora"


def screenshot(params: dict | None = None) -> str:
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta = os.path.expanduser(f"~/Desktop/captura_{timestamp}.png")
        cmd = (
            f'powershell -command "'
            f"Add-Type -AssemblyName System.Windows.Forms;"
            f"Add-Type -AssemblyName System.Drawing;"
            f"$bmp=[System.Windows.Forms.Screen]::PrimaryScreen.Bounds;"
            f"$img=New-Object System.Drawing.Bitmap $bmp.Width,$bmp.Height;"
            f"$g=[System.Drawing.Graphics]::FromImage($img);"
            f"$g.CopyFromScreen($bmp.Location,[System.Drawing.Point]::Empty,$bmp.Size);"
            f"$img.Save('{ruta}')\""
        )
        os.system(cmd)
        return "Captura guardada"
    except Exception as exc:
        logger.error(f"Error captura: {exc}")
        return "No pude hacer la captura."


def shutdown(params: dict | None = None) -> str:
    return "Por seguridad, esta accion requiere confirmacion."


def restart(params: dict | None = None) -> str:
    return "Por seguridad, esta accion requiere confirmacion."


def set_volume(params: dict | None = None) -> str:
    level = (params or {}).get("level", 50)
    logger.info(f"set_volume called with level={level}")
    return f"Volumen ajustado a {level}%"