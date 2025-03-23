import logging
import json
import os
import requests
import paho.mqtt.client as mqtt
import time
from datetime import datetime, timezone
from tz_utils import get_posix_tz_string


# Configuración del broker MQTT
BROKER_ADDRESS = os.environ.get("MQTT_SERVER", "mosquitto")  # Dirección del broker MQTT
BROKER_PORT = 1883            # Puerto del broker MQTT

logger = logging.getLogger(__name__)

# Tópicos
TOPIC_SUBSCRIBE = "divoom/2/+/set"

def transform_current_weather(source):
    # Construir el objeto destino con las claves raíz que se mantienen
    target = {
        "coord": source["coord"],
        "weather": [
            {
                "icon": source["weather"][0]["icon"]
            }
        ],
        "main": source["main"],
        "visibility": source["visibility"],
        "wind": {
            "speed": source["wind"]["speed"]
        },
        "dt": source["dt"],
        "sys": {
            "sunrise": source["sys"]["sunrise"],
            "sunset": source["sys"]["sunset"]
        },
        "cod": source["cod"],
    }

    return target

def transform_forecast(source):
    # Construir el objeto destino con las claves raíz que se mantienen
    target = {
        "cod": source["cod"],
        "message": source["message"],
        "cnt": source["cnt"],
        "list": []
    }

    # Recorrer cada entrada en "list" del JSON original
    for item in source["list"]:
        new_item = {
            "dt": item["dt"],
            "main": {
                # Se extraen únicamente temp_min y temp_max
                "temp_min": item["main"]["temp_min"],
                "temp_max": item["main"]["temp_max"]
            },
            "weather": []
        }

        # Extraer el icono de la lista weather (asumiendo que siempre hay al menos uno)
        if item.get("weather"):
            new_item["weather"].append({"icon": item["weather"][0]["icon"]})

        target["list"].append(new_item)

    return target

def send_weather_now(client, payload):
    if all(key in payload for key in ["Command", "DeviceId", "PacketFlag", "DeviceType"]):
        api_key = os.environ.get("OPENWEATHER_API_KEY")
        lat = os.environ.get("LOCATION_LAT", 0.0)
        lon = os.environ.get("LOCATION_LOT", 0.0)
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}')

        if response.status_code == 200:
            weather_data = response.json()
            transformed_data = transform_current_weather(weather_data)
            utc_timestamp = int(datetime.now(tz=timezone.utc).timestamp())

            transformed_data["RequestTime"] = utc_timestamp
            transformed_data["DeviceId"] = payload["DeviceId"]
            transformed_data["Command"] = payload["Command"]
            transformed_data["PacketFlag"] = payload["PacketFlag"]
        else:
            logger.error("Failed to retrieve weather data")
            return

        publish_topic = "divoom/2/" + str(payload["DeviceId"]) + "/get"
        client.publish(publish_topic, json.dumps(transformed_data))
        logger.debug(f"Response published on {publish_topic}: {transformed_data}")
    else:
        logger.error("Invalid parameters in message")


def send_forecast(client, payload):
    if all(key in payload for key in ["Command", "DeviceId", "PacketFlag", "DeviceType"]):
        api_key = os.environ.get("OPENWEATHER_API_KEY")
        lat = os.environ.get("LOCATION_LAT", 0.0)
        lon = os.environ.get("LOCATION_LOT", 0.0)
        response = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={api_key}')
        transformed_data = {}

        if response.status_code == 200:
            weather_data = response.json()
            transformed_data = transform_forecast(weather_data)
            utc_timestamp = int(datetime.now(tz=timezone.utc).timestamp())

            transformed_data["RequestTime"] = utc_timestamp
            transformed_data["Type"] = 1
            transformed_data["DeviceId"] = payload["DeviceId"]
            transformed_data["Command"] = payload["Command"]
            transformed_data["PacketFlag"] = payload["PacketFlag"]
        else:
            logger.error("Failed to retrieve weather data")
            return


        publish_topic = "divoom/2/" + str(payload["DeviceId"]) + "/get"
        # Publicar la respuesta en el tópico de respuesta
        client.publish(publish_topic, json.dumps(transformed_data))
        logger.debug(f"Response published on {publish_topic}: {transformed_data}")
    else:
        logger.error("Invalid parameters in message")

def send_hearbeat(client, payload):
# Verificar que el mensaje contiene los campos necesarios
    if all(key in payload for key in ["Command", "DeviceId", "PacketFlag", "DeviceType"]):
        # Crear la respuesta
        response = {
            "Command": payload["Command"],
            "DeviceId": payload["DeviceId"],
            "PacketFlag": payload["PacketFlag"]
        }
        publish_topic = "divoom/2/" + str(payload["DeviceId"]) + "/get"
        # Publicar la respuesta en el tópico de respuesta
        client.publish(publish_topic, json.dumps(response))
        logger.debug(f"Response published on {publish_topic}: {response}")
    else:
        logger.error("Invalid parameters in message")

def send_config(client, payload):
    if all(key in payload for key in ["Command", "DeviceId", "PacketFlag", "DeviceType"]):

        location_lot = os.environ.get("LOCATION_LOT", 0.0)
        location_lat = os.environ.get("LOCATION_LAT", 0.0)
        timezone = os.environ.get("TZ", "UTC")
        posix_timezone = get_posix_tz_string(timezone)

        # Crear la respuesta
        response = {
            "ReturnCode": 0,
            "ReturnMessage": "",
            "CurClockId": 182,
            "OnOff": 0,
            "StartTime": 0,
            "EndTime": 360,
            "Brightness": 68,
            "ChannelIndex": 0,
            "RotationFlag": 0,
            "ClockTime": 60,
            "GalleryTime": 60,
            "SingleGalleyTime": -1,
            "GalleryShowTimeFlag": -1,
            "Time24Flag": 0,
            "LocationMode": 0,
            "LocationCityName": "",
            "LocationCityId": 0,
            "Longitude": location_lot,
            "Latitude": location_lat,
            "TimeZoneMode": 0,
            "TimeZoneInfo": 0,
            "TemperatureMode": 0,
            "StartupFileId": "",
            "GyrateAngle": 0,
            "DeviceAutoUpdate": 1,
            "TimeZoneName": timezone,
            "TimeZoneValue": posix_timezone,
            "WhiteBalanceR": 100,
            "WhiteBalanceG": 100,
            "WhiteBalanceB": 100,
            "MirrorFlag": 0,
            "HighLight": 0,
            "DateFormat": 0,
            "LcdImageArray": [
                "",
                "",
                "",
                "",
                ""
            ],
            "StartUpClockId": 57,
            "OnOffVolume": 1,
            "NotificationSound": 100,
            "BluetoothAutoConnect": 1,
            "AutoPowerOff": 0,
            "DisableMic": 1,
            "Language": 0,
            "ScreenProtection": 0,
            "LockScreenTime": 600,
            "DeviceId": payload["DeviceId"],
            "Command": payload["Command"],
            "PacketFlag": payload["PacketFlag"]
        }
        publish_topic = "divoom/2/" + str(payload["DeviceId"]) + "/get"
        # Publicar la respuesta en el tópico de respuesta
        client.publish(publish_topic, json.dumps(response))
        logger.debug(f"Response published on {publish_topic}: {response}")
    else:
        logger.error("Invalid parameters in message")



# Callback que se ejecuta al conectar con el broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True
        logger.info("Connected to MQTT broker")
        client.subscribe(TOPIC_SUBSCRIBE)
    else:
        logger.error(f"Failed to connect to MQTT broker. Error code: {rc}")

# Callback que se ejecuta al recibir un mensaje
def on_message(client, userdata, msg):
    try:
        # Decodificar el payload del mensaje
        payload = json.loads(msg.payload.decode('utf-8'))

        logger.info(f"Received command {payload['Command']}")

        if payload["Command"] == "Device/Hearbeat": send_hearbeat(client, payload)
        elif payload["Command"] == "Sys/GetConf": send_config(client, payload)
        elif payload["Command"] == "Weather/GetForecastWeatherInfo": send_forecast(client, payload)
        elif payload["Command"] == "Weather/GetRealWeatherInfo": send_weather_now(client, payload)
        else: logger.info(f"Command {payload['Command']}  not supported")

    except json.JSONDecodeError:
        logger.error("Error decoding message")

def on_connect_fail(client, userdata):
    logger.error(f"Failed to connect to broker")

def run_mqtt_client():

    # Crear una instancia del cliente MQTT
    mqtt.Client.connected_flag=False
    client = mqtt.Client()

    client.enable_logger()

    # Asignar los callbacks
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_connect_fail = on_connect_fail

    # Mantener el cliente en funcionamiento
    client.loop_start()

    # Conectar al broker
    try:
        client.connect(BROKER_ADDRESS, BROKER_PORT, 60)
    except Exception as e:
        logger.error(f"Initial connect to broker failed: {e}")
