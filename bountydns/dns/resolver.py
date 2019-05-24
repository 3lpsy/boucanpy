import requests
from textwrap import dedent
import copy
from dnslib.server import DNSServer, BaseResolver
from dnslib import RR, QTYPE, RCODE
from bountydns.core import logger
from bountydns.dns.zone_template import ZONE_TEMPLATE
from bountydns.dns.record import Record


class Resolver(BaseResolver):
    def __init__(self, api_client, glob=False):
        # super().__init__(upstream, 53, 5)
        self.api_client = api_client
        self.records = self.make_records()
        self.glob = glob
        self.eq = "matchGlob" if glob else "__eq__"

    # pull the zones + records from the API and convert them to RR records
    def make_records(self):
        zones = self.api_client.get_zones()
        records = []
        for zone in zones:
            logger.info(f"loading zone: {zone.domain} ({zone.id})")
            dns_records = zone.dns_records or []
            # if the zone has no records, create some default ones
            if not dns_records:
                logger.warning(
                    f"zone has not dns_records. loading default: {zone.id} ({zone.domain})"
                )
                rrs = RR.fromZone(
                    ZONE_TEMPLATE.format(domain_name=zone.domain, domain_ip=zone.ip)
                )
                zone_records = zone_records + [Record(zone, rr) for rr in rrs]
            else:
                # loop over each dns_record of the zone and convert it to RR record
                dns_records = sorted(zone.dns_records, key=lambda x: x.sort)
                zone_records = []
                for dns_record in dns_records:
                    try:
                        rrs = zone_records + RR.fromZone(dns_record.record)
                        zone_records = zone_records + [Record(zone, rr) for rr in rrs]
                    except Exception as e:
                        raise RuntimeError(
                            f'Error processing line ({e.__class__.__name__}: {e}) "{dns_record.id}:{dns_record.record}"'
                        ) from e

            # add the records for the zone to the rest of the records
            records = records + zone_records

        logger.debug("%d zone resource records generated", len(records))
        return records

    def resolve(self, request, handler):
        reply = request.reply()
        qname = request.q.qname
        qtype = QTYPE[request.q.qtype]
        for name, rtype, rr in self.get_split_records():
            # Check if label & type match
            if getattr(qname, self.eq)(name) and (
                qtype == rtype or qtype == "ANY" or rtype == "CNAME"
            ):
                # If we have a glob match fix reply label
                if self.glob:
                    a = copy.copy(rr)
                    a.rname = qname
                    reply.add_answer(a)
                else:
                    reply.add_answer(rr)
                # Check for A/AAAA records associated with reply and
                # add in additional section
                if rtype in ["CNAME", "NS", "MX", "PTR"]:
                    for a_name, a_rtype, a_rr in self.get_split_records():
                        if a_name == rr.rdata.label and a_rtype in ["A", "AAAA"]:
                            reply.add_ar(a_rr)
        if not reply.rr:
            reply.header.rcode = RCODE.NXDOMAIN
        return reply

    def get_split_records(self):
        return [(rr.rname, QTYPE[rr.rtype], rr) for rr in self.get_rrs()]

    def get_rrs(self):
        return [record.rr for record in self.records]

    # def resolve(self, request, handler):
    #     reply = request.reply()
    #     logger.warning(request.__class__.__name__)
    #     qname = request.q.qname
    #     qtype = QTYPE[request.q.qtype]
    #     for record in self.records:
    #         # Check if label & type match
    #         if record.match(request.q):
    #             a = copy.copy(record.rr)
    #             reply.add_answer(a)
    #     if reply.rr:
    #         return reply

    #     if not reply.rr:
    #         reply.header.rcode = RCODE.NXDOMAIN
    #     return reply
