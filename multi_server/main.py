import logging
import threading
import time
import os

from web_server import run_server as run_flask
from dns_server import run_dns_server
# from dhcp_server import run_dhcp_server
from mqtt_client import run_mqtt_client

if __name__ == '__main__':

    logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO'), format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    # Create threads for each service
    flask_thread = threading.Thread(target=run_flask, name="FlaskServer")
    dns_thread = threading.Thread(target=run_dns_server, name="DNSServer")
    # dhcp_thread = threading.Thread(target=run_dhcp_server, name="DHCPServer")
    mqtt_thread = threading.Thread(target=run_mqtt_client, name="MQTTclient")

    flask_thread.daemon = True
    dns_thread.daemon = True
    # dhcp_thread.daemon = True
    mqtt_thread.daemon = True

    # Start the threads
    flask_thread.start()
    dns_thread.start()
    # dhcp_thread.start()
    mqtt_thread.start()

    logger.info("Server started")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Servers stopped")
