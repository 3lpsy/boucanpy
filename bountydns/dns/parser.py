from textwrap import dedent
from dnslib import RR, QTYPE, RCODE
from bountydns.core import logger
from bountydns.dns.record import Record
from bountydns.dns.zone_template import ZONE_TEMPLATE


class RecordParser:
    def __init__(self, records):
        self.records = records

    # TODO: make this better
    @classmethod
    def from_zones(cls, zones):
        records = []
        for zone in zones:
            records = records + cls.from_zone(zone).records
        logger.debug("%d zone resource records generated", len(records))
        return cls(records)

    @classmethod
    def from_zone(cls, zone):
        records = []
        logger.info(
            f"from_zone@parser.py - Loading zone: {zone.domain}/{zone.ip} ({zone.id})"
        )
        dns_records = zone.dns_records or []
        # if the zone has no records, create some default ones
        if not dns_records:
            logger.warning(
                f"from_zone@parser.py - Zone has no dns_records. loading defaults: {zone.domain}/{zone.ip} ({zone.id})"
            )
            rrs = RR.fromZone(
                ZONE_TEMPLATE.format(domain_name=zone.domain, domain_ip=zone.ip)
            )
            zone_records = [Record.make(zone, rr) for rr in rrs]
            for zr in zone_records:
                # TODO: make this clean on output
                rrstr = str(dedent(str(zr.rr)))
                logger.debug(f"from_zone@parser.py - Loading record entry: {rrstr}")
                logger.debug(
                    "from_zone@parser.py - Loaded record details - name: {} | rtype: {} | rr: {}".format(
                        str(zr.rr.rname), str(QTYPE[zr.rr.rtype]), str(zr.rr)
                    )
                )
        else:
            # loop over each dns_record of the zone and convert it to RR record
            dns_records = sorted(dns_records, key=lambda x: x.sort)
            zone_records = []
            for dns_record in dns_records:
                try:
                    rrs = RR.fromZone(dns_record.record)
                    _zone_records = [Record.make(zone, rr) for rr in rrs]
                    for zr in _zone_records:
                        rrstr = str(dedent(str(zr.rr)))
                        logger.debug(
                            f"from_zone@parser.py - Loading record: {str(dns_record.record)}"
                        )
                        logger.debug(
                            f"from_zone@parser.py - Loading record entry: {rrstr}"
                        )
                        logger.debug(
                            "from_zone@parser.py - Loaded record details - name: {} | rtype: {} | rr: {}".format(
                                str(zr.rr.rname), str(QTYPE[zr.rr.rtype]), str(zr.rr)
                            )
                        )
                    zone_records = zone_records + _zone_records
                except Exception as e:
                    logger.critical(
                        f'from_zone@parser.py - Error processing line ({e.__class__.__name__}: {e}) "{dns_record.id}:{dns_record.record}" '
                    )
                    raise e

        # add the records for the zone to the rest of the records
        records = records + zone_records
        return cls(records)

    def get_rrs(self):
        return [record.rr for record in self.records]
