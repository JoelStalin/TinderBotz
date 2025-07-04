"""
Bot de Tinder personalizado para Joel
Modificado por ChatGPT - Loop infinito tras ajuste de distancia + Recs reset
"""

import requests
import time
import keyboard
from tinderbotz.session import Session
from tinderbotz.helpers.constants_helper import *

def get_current_location():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        loc = data.get("loc")  # Formato: "lat,long"
        if loc:
            latitude, longitude = map(float, loc.split(','))
            return latitude, longitude
    except Exception as e:
        print("⚠️ Error obteniendo la ubicación automática:", e)
    return 25.7617, -80.1918  # Fallback: Miami

if __name__ == "__main__":
    session = Session(store_session=True)

    # Establecer ubicación
    lat, lon = get_current_location()
    print(f"🌎 Ubicación detectada: {lat}, {lon}")
    session.set_custom_location(latitude=lat, longitude=lon)

    # Login manual
    print("🔐 Abriendo Tinder. Inicia sesión manualmente...")
    session.browser.get("https://tinder.com")
    input("Presiona ENTER cuando hayas iniciado sesión correctamente...")

    print("♻️ Iniciando ciclo infinito. Presiona 'q' para detener.")
    try:
        while True:
            if keyboard.is_pressed('q'):
                print("🛑 Bot detenido por el usuario.")
                break

            # Posicionarse en la sección de recomendaciones
            session.browser.get("https://tinder.com/app/recs")

            # Acciones básicas
            session.like(amount=1000, ratio="72.5%", sleep=1)
            session.dislike(amount=1)
            session.superlike(amount=1)

            # Ajustar preferencias
            session.set_distance_range(km=150)
            session.set_age_range(18, 55)
            session.set_sexuality(Sexuality.WOMEN)
            session.set_global(True)

            # Guardar matches antiguos
            for match in session.get_messaged_matches():
                session.store_local(match)

            # Enviar mensajes a nuevos matches
            new_matches = session.get_new_matches(amount=10, quickload=False)
            pickup_line = "Hey {}! You. Me. Pizza? O no te gusta la pizza?"
            for match in new_matches:
                name = match.get_name()
                chat_id = match.get_chat_id()
                print(f"💬 Enviando mensaje a: {name}")
                session.send_message(chatid=chat_id, message=pickup_line.format(name))
                session.send_gif(chatid=chat_id, gifname="")
                session.send_song(chatid=chat_id, songname="")
                session.send_socials(chatid=chat_id, media=Socials.INSTAGRAM, value="Fredjemees")

            # Geomatches
            for _ in range(5):
                geomatch = session.get_geomatch(quickload=False)
                session.store_local(geomatch)
                session.dislike()

            time.sleep(5)

    except KeyboardInterrupt:
        print("🛑 Bot detenido con Ctrl+C")
    except Exception as e:
        print(f"❌ Error en la ejecución del ciclo: {e}")
