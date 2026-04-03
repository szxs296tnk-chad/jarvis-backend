import re
import subprocess
import threading
import queue

# ─────────────────────────────
# LIMPIEZA DE TEXTO
# ─────────────────────────────

_CORRECCIONES = {
    "espotivali": "spotify",
    "espotifai":  "spotify",
    "spotifi":    "spotify",
    "yutub":      "youtube",
    "netflis":    "netflix",
    "jarvi":      "jarvis",
    "jarbis":     "jarvis",
}


def limpiar_texto(texto: str) -> str:
    if not texto:
        return ""

    texto = texto.lower().strip()
    texto = re.sub(r"[^\w\s]", "", texto)

    for error, correcto in _CORRECCIONES.items():
        texto = texto.replace(error, correcto)

    return texto


# ─────────────────────────────
# VOICE ENGINE BLINDADO
# ─────────────────────────────

class VoiceEngine:
    def __init__(self):
        self._init_engine()

        self.thread = threading.Thread(
            target=self._worker,
            daemon=True
        )
        self.thread.start()

        print("✅ VoiceEngine listo")

    # 🔥 inicialización segura
    def _init_engine(self):
        self.queue = queue.Queue()
        self.lock = threading.Lock()
        self.running = True

    # 🔥 protección total
    def _ensure_ready(self):
        if not hasattr(self, "queue"):
            print("⚠️ Reinicializando VoiceEngine...")
            self._init_engine()

    # ────────────────
    # API
    # ────────────────

    def speak(self, texto: str):
        if not texto:
            return

        self._ensure_ready()

        try:
            if self.queue.qsize() > 5:
                self.queue.get_nowait()
        except:
            pass

        self.queue.put(texto)

    # ────────────────
    # WORKER
    # ────────────────

    def _worker(self):
        while True:
            self._ensure_ready()

            try:
                texto = self.queue.get(timeout=1)
                if texto:
                    self._hablar(texto)

            except queue.Empty:
                continue
            except Exception as e:
                print("Error VoiceEngine:", e)

    # ────────────────
    # TTS
    # ────────────────

    def _hablar(self, texto: str):
        with self.lock:

            texto_safe = (
                texto.replace('"', "")
                     .replace("'", "")
                     .replace("\\", "")
                     .replace("\n", " ")
            )

            script = (
                "Add-Type -AssemblyName System.Speech; "
                "$voz = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
                "$voz.Rate = 1; "
                "$voz.Volume = 100; "
                f'$voz.Speak("{texto_safe}"); '
                "$voz.Dispose();"
            )

            try:
                subprocess.run(
                    ["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=20
                )
            except subprocess.TimeoutExpired:
                print("⚠️ TTS timeout")
            except Exception as e:
                print("⚠️ Error TTS:", e)


# ─────────────────────────────
# INSTANCIA GLOBAL
# ─────────────────────────────

_voice_engine = VoiceEngine()


# ─────────────────────────────
# INTERFAZ
# ─────────────────────────────

def hablar(texto: str):
    print(f"Jarvis: {texto}")
    _voice_engine.speak(texto)


def hablar_async(texto: str):
    hablar(texto)