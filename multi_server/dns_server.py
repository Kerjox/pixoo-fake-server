import os
import time
import logging
from dnslib import DNSRecord, RR, A, QTYPE
from dnslib.server import DNSServer, BaseResolver

logger = logging.getLogger(__name__)

class EnvIPResolver(BaseResolver):
    def resolve(self, request, handler):
        # Get the local IP from the environment variable LOCAL_IP
        local_ip = os.environ.get("LOCAL_IP", "127.0.0.1")
        reply = request.reply()
        qname = request.q.qname
        # Add an A record with the obtained IP
        reply.add_answer(RR(qname, QTYPE.A, rdata=A(local_ip), ttl=60))
        return reply

def run_dns_server():
    resolver = EnvIPResolver()
    # Listen on 0.0.0.0:53 (standard DNS port)
    server = DNSServer(resolver, port=53, address="0.0.0.0", tcp=False)
    server.start_thread()
    logger.info("DNS Server running on port 53.")
    # Wait until the stop_event is set
    while True:
        time.sleep(1)
