from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import time
import logging
from brain import pensar
from acciones import ejecutar
from utils import limpiar_texto

app = FastAPI()

# 🔧 Configuración de logs (para ver errores reales)
logging.basicConfig(level=logging.INFO)

# ⏱️ Tiempo máximo de respuesta (segundos)
TIMEOUT_LIMIT = 5


# 🛡️ Middleware para evitar requests lentos
@app.middleware("http")
async def timeout_middleware(request: Request, call_next):
    start_time = time.time()
    
    try:
        response = await call_next(request)
    except Exception as e:
        logging.error(f"Error interno: {e}")
        return JSONResponse(
            status_code=500,
            content={"respuesta": "Error interno controlado"}
        )
    
    process_time = time.time() - start_time

    if process_time > TIMEOUT_LIMIT:
        logging.warning(f"Respuesta lenta: {process_time:.2f}s")

    return response


# ❤️ Health check (para saber si está vivo)
@app.get("/")
def health():
    return {"status": "ok", "mensaje": "Jarvis backend activo"}


# 🎯 Endpoint principal
@app.post("/command")
async def command(request: Request):
    try:
        data = await request.json()

        texto = data.get("input", "")

        texto = limpiar_texto(texto)

        if not texto:
            return {"respuesta": "No recibí comando"}

        logging.info(f"COMANDO: {texto}")

        # 🔥 comandos directos
        if "hora" in texto:
            hora = time.strftime("%H:%M")
            return {"respuesta": f"Son las {hora}"}

        if "hola" in texto or "jarvis" in texto:
            return {"respuesta": "Estoy en línea"}

        # 🔥 detección rápida de acciones
        accion = None

        if "spotify" in texto:
            accion = "abrir_spotify"
        elif "youtube" in texto or "yt" in texto:
            accion = "abrir_youtube"
        elif "netflix" in texto:
            accion = "abrir_netflix"
        elif "navegador" in texto or "google" in texto:
            accion = "abrir_navegador"
        elif "calculadora" in texto:
            accion = "abrir_calculadora"
        elif "notas" in texto:
            accion = "abrir_notas"
        elif "captura" in texto:
            accion = "captura_pantalla"

        if accion:
            resultado = ejecutar(accion)
            return {"respuesta": resultado}

        # 🔥 IA (cerebro real)
        respuesta = pensar(texto)

        # si la IA devuelve acción
        if respuesta.startswith("ACCION:"):
            accion = respuesta.replace("ACCION:", "").strip()
            resultado = ejecutar(accion)
            return {"respuesta": resultado}

        texto = data.get("input", "").lower().strip()

        if not texto:
            return {"respuesta": "No recibí comando"}

        # 🔥 comandos directos
        if "hora" in texto:
            hora = time.strftime("%H:%M")
            return {"respuesta": f"Son las {hora}"}

        if "hola" in texto or "jarvis" in texto:
            return {"respuesta": "Estoy en línea"}

        # 🔥 acciones básicas simuladas
        if "youtube" in texto:
            return {"respuesta": "Abriendo YouTube"}

        if "spotify" in texto:
            return {"respuesta": "Abriendo Spotify"}

        if "agua" in texto:
            return {"respuesta": "Recuerda tomar agua"}


        if "noche" in texto:
            return {"respuesta": "Buenas noches, activando rutina"}

        # fallback
        return {"respuesta": "No entendí el comando"}

    except Exception as e:
        logging.error(f"Error en /command: {e}")
        return JSONResponse(
            status_code=200,
            content={"respuesta": "Error controlado"}
        )