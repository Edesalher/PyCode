import paho.mqtt.client as mqtt
import logging
import time
import os
from brokerData import *  # Informacion de la conexion

LOG_FILENAME = 'mqtt.log'

# Configuracion inicial de logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] (%(threadName)-10s) %(message)s'
)


# Callback que se ejecuta cuando nos conectamos al broker
def on_connect(client, userdata, rc):
    logging.info("Conectado al broker")


# Callback que se ejecuta cuando llega un mensaje al topic suscrito
def on_message(client, userdata, msg):
    # Se muestra en pantalla informacion que ha llegado
    logging.info("Ha llegado el mensaje al topic: " + str(msg.topic))
    logging.info("El contenido del mensaje es: " + str(msg.payload))

    # Y se almacena en el log
    logCommand = 'echo "(' + str(msg.topic) + ') -> ' + str(msg.payload) + '" >> ' + LOG_FILENAME
    os.system(logCommand)


client = mqtt.Client(clean_session=True)  # Nueva instancia de cliente
client.on_connect = on_connect  # Se configura la funcion "Handler" cuando suceda la conexion
client.on_message = on_message  # Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
client.username_pw_set(MQTT_USER, MQTT_PASS)  # Credenciales requeridas por el broker
client.connect(host=MQTT_HOST, port=MQTT_PORT)  # Conectar al servidor remoto

# Nos conectaremos a distintos topics:
qos = 2

# Subscripcion simple con tupla (topic,qos)
client.subscribe(("sensores/6/hum", qos))

# Subscripcion multiple con lista de tuplas
client.subscribe([("sensores/8/#", qos), ("sensores/+/atm", qos), ("sensores/0/temp", qos)])

# Iniciamos el thread (implementado en paho-mqtt) para estar atentos a mensajes en los topics subscritos
client.loop_start()

# El thread de MQTT queda en el fondo, mientras en el main loop hacemos otra cosa

try:
    while True:
        logging.info("olakease")
        time.sleep(10)


except KeyboardInterrupt:
    logging.warning("Desconectando del broker...")

finally:
    client.loop_stop()  # Se mata el hilo que verifica los topics en el fondo
    client.disconnect()  # Se desconecta del broker
    logging.info("Desconectado del broker. Saliendo...")