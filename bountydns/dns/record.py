from dnslib import DNSLabel, QTYPE, RR, dns
from textwrap import wrap
from .types import TYPES
from bountydns.core import logger


class Record:
    def __init__(self, zone, rr):
        self.zone = zone
        self.rr = rr
        self.type = QTYPE[rr.rtype]
        self.name = DNSLabel(rr.rname)
        self.data = rr.rdata

    def match(self, q):
        matched = False
        logger.debug(
            "record matcher: comparing types {} with {} (or any)".format(
                QTYPE[q.qtype], self.type
            )
        )

        if q.qtype == QTYPE.ANY or QTYPE[q.qtype] == self.type:
            if str(self.name) in [".", "@", "*"]:
                record_name = self.zone.domain
                logger.debug(
                    "record matcher: replacing rname {} with record {}".format(
                        self.name, record_name
                    )
                )
            else:
                record_name = self.name
            logger.debug(
                "record matcher: comparing request {}:{} to name {}:{}".format(
                    QTYPE[q.qtype], q.qname, self.type, record_name
                )
            )
            matched = q.qname.matchGlob(record_name)
        if matched:
            logger.info(
                "record matcher: match found {}:{} to name {}:{}".format(
                    QTYPE[q.qtype], q.qname, self.type, record_name
                )
            )
        return matched
