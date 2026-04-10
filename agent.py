import requests
import time
import webbrowser

URL_SERVIDOR = "https://jarvis-backend-production-786c.up.railway.app/command?token=jarvis_ultra_170174"  # cambia esto

def ejecutar_comando(texto):
    texto = texto.lower()

    if "youtube" in texto:
        webbrowser.open("https://www.youtube.com")
        print("🎬 Abriendo YouTube")

    elif "google" in texto:
        webbrowser.open("https://www.google.com")
        print("🌐 Abriendo Google")

    else:
        print("❓ Comando no reconocido:", texto)


def escuchar():
    print("🤖 Jarvis Agent en línea...")

    while True:
        try:
            response = requests.get(URL_SERVIDOR)
            
            if response.status_code == 200:
                data = response.json()
                comando = data.get("comando")

                if comando:
                    print("🧠 Recibido:", comando)
                    ejecutar_comando(comando)

            time.sleep(2)

        except Exception as e:
            print("⚠️ Error:", e)
            time.sleep(5)


if __name__ == "__main__":
    escuchar()