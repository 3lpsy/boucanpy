import copy
from dnslib.server import DNSServer, BaseResolver
from dnslib import RR, QTYPE, RCODE
from boucanpy.core import logger
from boucanpy.dns.parser import RecordParser


class Resolver(BaseResolver):
    def __init__(self, api_client, glob=True):
        # super().__init__(upstream, 53, 5)
        self.api_client = api_client
        self.records = self.make_records()
        self.glob = glob
        self.eq = "matchGlob" if glob else "__eq__"

    # pull the zones + records from the API and convert them to RR records
    def make_records(self):
        self.api_client.load_zones()
        parsed = RecordParser.from_zones(self.api_client.zones)
        return parsed.records

    def resolve(self, request, handler):
        reply = request.reply()
        qname = request.q.qname
        qtype = QTYPE[request.q.qtype]
        for name, rtype, rr in self.get_split_records():
            # Check if label & type match
            if getattr(qname, self.eq)(name) and (
                qtype == rtype or qtype == "ANY" or rtype == "CNAME"
            ):
                logger.debug(
                    "record matched - name: {} | rtype: {} | rr: {} | qname: {}".format(
                        str(name), str(rtype), str(rr), str(qname)
                    )
                )
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
            else:
                logger.debug(
                    "record not matched: {} for {}".format(str(name), str(qname))
                )
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
