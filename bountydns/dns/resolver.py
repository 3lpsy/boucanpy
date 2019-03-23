import textwrap 
import copy
from dnslib.server import DNSServer, BaseResolver
from dnslib import RR,QTYPE,RCODE
from bountydns.core import logger
from bountydns.dns.zone_template import ZONE_TEMPLATE
from bountydns.dns.record import Record

class Resolver(BaseResolver):
    def __init__(self, zone_maps, upstream, api_url, api_token):
        # super().__init__(upstream, 53, 5)
        self.zones = self.maps_to_zones(zone_maps)
        self.api_url = api_url
        self.api_token = api_token
    
    def maps_to_zones(self, maps):
        zones = []
        for zone_map in maps:
            try:
                for rr in self.map_to_rr(zone_map):
                    logger.debug('registering zone rr name {} and type {}'.format(rr.rname, QTYPE[rr.rtype]))
                    zone = Record(zone_map, rr)
                    zones.append(zone)
                    logger.debug(' %2d: %s', len(zones), zone)

            except Exception as e:
                raise RuntimeError(f'Error processing line ({e.__class__.__name__}: {e}) "{zone_map[0].strip()}"') from e
        logger.debug('%d zone resource records generated', len(zones))
        return zones

    def map_to_rr(self, zone_map):
        z = ZONE_TEMPLATE.format(domain_name=zone_map[0], domain_ip=zone_map[1])
        return RR.fromZone(textwrap.dedent(z))

    def resolve(self, request, handler):
        reply = request.reply()
        logger.warning(request.__class__.__name__)
        qname = request.q.qname
        qtype = QTYPE[request.q.qtype]
        for record in self.zones:
            # Check if label & type match
            if record.match(request.q):
                logger.warning("resolver: found match request {}:{} to name {}:{}".format(qtype,qname, record.type, record.name))
                a = copy.copy(record.rr)
                reply.add_answer(a)
        if reply.rr:
            return reply
            
        if not reply.rr:
            reply.header.rcode = RCODE.NXDOMAIN
        return reply