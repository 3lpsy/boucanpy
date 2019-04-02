import requests
import textwrap
import copy
from dnslib.server import DNSServer, BaseResolver
from dnslib import RR, QTYPE, RCODE
from bountydns.core import logger
from bountydns.dns.zone_template import ZONE_TEMPLATE
from bountydns.dns.record import Record


class Resolver(BaseResolver):
    def __init__(self, api_client):
        # super().__init__(upstream, 53, 5)
        self.api_client = api_client
        self.records = self.zones_to_records(self.get_zones())

    def zones_to_records(self, zones):
        records = []
        for zone in zones:
            try:
                for rr in self.zone_to_rr(zone):
                    logger.debug(
                        "registering zone rr name {} and type {}".format(
                            rr.rname, QTYPE[rr.rtype]
                        )
                    )
                    record = Record(zone, rr)
                    records.append(record)
                    logger.debug(" %2d: %s", len(records), record)
            except Exception as e:
                raise RuntimeError(
                    f'Error processing line ({e.__class__.__name__}: {e}) "{zone.domain}"'
                ) from e
            logger.info("zone map generated {}".format(str(zone)))
        logger.info("%d zone resource records generated", len(records))
        return records

    def get_zones(self):
        return self.api_client.get_zones()

    def zone_to_rr(self, zone):
        z = ZONE_TEMPLATE.format(domain_name=zone.domain, domain_ip=zone.ip)
        return RR.fromZone(textwrap.dedent(z))

    def resolve(self, request, handler):
        reply = request.reply()
        logger.warning(request.__class__.__name__)
        qname = request.q.qname
        qtype = QTYPE[request.q.qtype]
        for record in self.records:
            # Check if label & type match
            if record.match(request.q):
                a = copy.copy(record.rr)
                reply.add_answer(a)
        if reply.rr:
            return reply

        if not reply.rr:
            reply.header.rcode = RCODE.NXDOMAIN
        return reply
