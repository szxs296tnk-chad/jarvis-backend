import requests

# ─────────────────────────────
# CONFIG
# ─────────────────────────────

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "llama3"

# Timeout más realista
TIMEOUT = 10

# ─────────────────────────────
# PENSAR
# ─────────────────────────────

def pensar(comando: str) -> str:

    if not comando:
        return "No entendí el comando."

    try:

        prompt = _construir_prompt(comando)

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODELO,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,   # más preciso
                    "num_predict": 60    # límite controlado
                }
            },
            timeout=TIMEOUT
        )
        
        if response.status_code != 200:
            return "Error en el servidor de inteligencia."
        data = response.json()
        texto = data.get("response", "").strip()

        if not texto:
            return "No entendí la solicitud."

        return _limpiar_respuesta(texto)

    except requests.exceptions.Timeout:
        return "Estoy procesando, intente nuevamente."

    except Exception as e:
        return "No pude procesar la solicitud."


# ─────────────────────────────
# PROMPT INTELIGENTE
# ─────────────────────────────

def _construir_prompt(comando: str) -> str:

    return f"""
Eres Jarvis, un asistente de computadora preciso, directo y eficiente.

INSTRUCCIONES:

1. Si el usuario quiere ejecutar una acción responde SOLO:
ACCION:nombre_accion

2. Acciones disponibles:
- abrir_spotify
- abrir_youtube
- abrir_netflix
- abrir_navegador
- abrir_calculadora
- abrir_notas
- captura_pantalla
- apagar_pc
- reiniciar_pc

3. Si NO es una acción:
Responde de forma breve, clara y natural.

Usuario: {comando}
"""


# ─────────────────────────────
# LIMPIAR RESPUESTA
# ─────────────────────────────

def _limpiar_respuesta(texto: str) -> str:

    # evita respuestas largas innecesarias
    texto = texto.strip()

    # seguridad extra
    if texto.lower().startswith("accion:"):
        return texto

    # limitar longitud (voz)
    if len(texto) > 200:
        texto = texto[:200]

    return texto