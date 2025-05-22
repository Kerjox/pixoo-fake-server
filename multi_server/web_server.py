import os
from flask import Flask, jsonify, request
from datetime import datetime, timezone
import random

app = Flask(__name__)

@app.route('/Device/InitV2', methods=['GET'])
def device_init():
    utc_timestamp = int(datetime.now(tz=timezone.utc).timestamp())
    packet_flag = request.json['PacketFlag']
    broker_ip = os.environ.get("MOSQUITTO_IP", "127.0.0.1")
    device_id = random.randint(100, 9999999)
    location_lot = os.environ.get("LOCATION_LOT", 0.0)
    location_lat = os.environ.get("LOCATION_LAT", 0.0)

    response = {
        "ReturnCode": 0,
        "ReturnMessage": "",
        "DevicePublicIP": "1.1.1.1",
        "IP": broker_ip,
        "lot": location_lot,
        "lat": location_lat,
        "SummerZone": 0,
        "TimeZoneCode": "",
        "UTCTime": utc_timestamp,
        "DeviceId": device_id,
        "LogLevel": 0,
        "IsResetAll": 0,
        "DeviceToken": "password_mqtt",
        "ServerType": 1,
        "LastClockId": 182,
        "Command": "Device/InitV2",
        "PacketFlag": packet_flag
    }
    return jsonify(response)

@app.route('/Test/GetIP', methods=['GET'])
def device_test_getip():
    packet_flag = request.json['PacketFlag']
    device_id = request.json['DeviceId']

    response = {
        "ReturnCode": 0,
        "ReturnMessage": "",
        "CustonIP": "1.1.1.1",
        "DeviceId": device_id,
        "Command": "Device/UpdateDevicePublicIP",
        "PacketFlag": packet_flag
    }
    return jsonify(response)

@app.route('/Device/UpdateDevicePublicIP', methods=['GET'])
def device_update_device_public_ip():
    packet_flag = request.json['PacketFlag']
    device_id = request.json['DeviceId']

    response = {
        "ReturnCode": 0,
        "ReturnMessage": "",
        "DeviceId": device_id,
        "Command": "Device/UpdateDevicePublicIP",
        "PacketFlag": packet_flag
    }
    return jsonify(response)

def run_server():
    # Disable use_reloader to avoid spawning additional processes.
    app.run(host="0.0.0.0", port=80, debug=False, use_reloader=False)
