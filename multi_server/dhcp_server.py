import logging
import os
from ipaddress import IPv4Address, IPv4Network

from pyserve import listen_udp_threaded
from pydhcp.v4.server import Server
from pydhcp.v4.server.backend import MemoryBackend, CacheBackend

logger = logging.getLogger(__name__)

local_ip = os.environ.get("LOCAL_IP", "127.0.0.1")
local_network = os.environ.get("LOCAL_NETWORK")

# Prepare the custom memory backend as the base provider.
# The network and gateway are defined here.
backend = MemoryBackend(
    network=IPv4Network(local_network),
    dns=[IPv4Address(local_ip)],
    gateway=IPv4Address(local_ip)
)
# Wrap the backend with cache support (useful if you have non-memory backends)
backend = CacheBackend(backend)

# Launch the DHCP server using pyserve to listen on all interfaces (0.0.0.0) at UDP port 67.

def run_dhcp_server():
    listen_udp_threaded(
        address=('0.0.0.0', 67),
        factory=Server,
        allow_broadcast=True,
        backend=backend,
        logger=logger,
        server_id=IPv4Address(local_ip)  # DHCP server address
    )
