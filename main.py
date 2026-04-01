from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import time
import logging

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
        texto = data.get("input", "").lower()

        # 🧠 Lógica SIMPLE pero estable
        if "agua" in texto:
            respuesta = "Recuerda tomar agua"
        elif "noche" in texto:
            respuesta = "Buenas noches, activando rutina"
        elif "hola" in texto:
            respuesta = "Hola, estoy en línea"
        else:
            respuesta = "No entendí el comando, intenta otra vez"

        return {"respuesta": respuesta}

    except Exception as e:
        logging.error(f"Error en /command: {e}")
        return JSONResponse(
            status_code=200,
            content={"respuesta": "Hubo un error, pero sigo activo"}
        )