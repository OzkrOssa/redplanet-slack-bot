import os
from slack_bolt import App
from decouple import config
from settings import SLACK_CHANNELS, AP_HOSTS
from mikrotik import MikrotikACL
from ubiquiti import UbiquitiACL

# Initializes your app with your bot token and signing secret
app = App(
    token=config("SLACK_BOT_TOKEN"),
    signing_secret=config("SLACK_SIGNING_SECRET"),
)

@app.event("message")
def handle_message_events(message, say):

    split_message = message["text"].split("-")

    nombre = split_message[0]
    mac = split_message[1]
    codigo = str(split_message[2])

    if message["channel"]== SLACK_CHANNELS["conexiones-pppoe"]:
        print("PPPoE")
    elif message["channel"]== SLACK_CHANNELS["conexiones-puntos-de-acceso"]:
        # Si el dispositivo es un Mikrotik, se crea una instancia de MikrotikACL y se agrega la dirección MAC   
        try:
            if AP_HOSTS[codigo]["device"] == "mikrotik":
                mk = MikrotikACL(AP_HOSTS[codigo]["ip"])
                reply = mk.add_mac(mac,nombre)
                print(f"mikrotik {reply}")
                return say(text=str(reply))
        # Si el dispositivo es un Ubiquiti, se crea una instancia de UbiquitiACL y se agrega la dirección MAC
            elif AP_HOSTS[codigo]["device"] == "ubiquiti":
                ubnt = UbiquitiACL(AP_HOSTS[codigo]["ip"])
                reply = ubnt.add_mac(mac,nombre)
                print(f"ubiquiti {reply}")
                return say(text=str(reply))
        except KeyError:
            return say(text=f"{codigo} no existe")


    

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))