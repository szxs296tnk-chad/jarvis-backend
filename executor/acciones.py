import os
import webbrowser
import logging
from datetime import datetime

from core.config import CONFIG
from utils.utils import *

# ─────────────────────────────
# LOGGING
# ─────────────────────────────

logger = logging.getLogger("jarvis_acciones")


# ─────────────────────────────
# EJECUTOR PRINCIPAL
# ─────────────────────────────

def ejecutar(accion: str) -> str:

    if not accion:
        return "Acción no válida."

    accion = accion.strip().lower()

    handler = ACCIONES.get(accion)

    if not handler:
        logger.warning(f"Acción desconocida: {accion}")
        return "No reconozco esa acción."

    try:
        logger.info(f"Ejecutando: {accion}")
        resultado = handler()

        if not resultado:
            return "Acción ejecutada."

        return resultado

    except Exception as e:
        logger.error(f"Error en acción {accion}: {e}")
        return "Error al ejecutar la acción."


# ─────────────────────────────
# ACCIONES
# ─────────────────────────────

def abrir_spotify():
    os.system(CONFIG["SPOTIFY_CMD"])
    return "Abriendo Spotify"


def abrir_youtube():
    webbrowser.open("https://youtube.com")
    return "Abriendo YouTube"


def abrir_netflix():
    webbrowser.open("https://netflix.com")
    return "Abriendo Netflix"


def abrir_navegador():
    webbrowser.open("https://google.com")
    return "Abriendo navegador"


def abrir_calculadora():
    os.system(CONFIG["CALCULADORA_CMD"])
    return "Abriendo calculadora"


def abrir_notas():
    os.system(CONFIG["NOTAS_CMD"])
    return "Abriendo bloc de notas"


def captura_pantalla():
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta = os.path.expanduser(f"~/Desktop/captura_{timestamp}.png")

        cmd = f'''
powershell -command "Add-Type -AssemblyName System.Windows.Forms;
Add-Type -AssemblyName System.Drawing;
$bmp=[System.Windows.Forms.Screen]::PrimaryScreen.Bounds;
$img=New-Object System.Drawing.Bitmap $bmp.Width,$bmp.Height;
$g=[System.Drawing.Graphics]::FromImage($img);
$g.CopyFromScreen($bmp.Location,[System.Drawing.Point]::Empty,$bmp.Size);
$img.Save('{ruta}')"
'''

        os.system(cmd)
        return "Captura guardada"

    except Exception as e:
        logger.error(f"Error captura: {e}")
        return "No pude hacer la captura."


def apagar_pc():
    return "Por seguridad, esta acción requiere confirmación."


def reiniciar_pc():
    return "Por seguridad, esta acción requiere confirmación."


# ─────────────────────────────
# REGISTRO DE ACCIONES
# ─────────────────────────────

ACCIONES = {
    "abrir_spotify": abrir_spotify,
    "abrir_youtube": abrir_youtube,
    "abrir_netflix": abrir_netflix,
    "abrir_navegador": abrir_navegador,
    "abrir_calculadora": abrir_calculadora,
    "abrir_notas": abrir_notas,
    "captura_pantalla": captura_pantalla,
    "apagar_pc": apagar_pc,
    "reiniciar_pc": reiniciar_pc,
}