from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class DnsRecord(Base):
    __tablename__ = "dns_records"
    id = Column(Integer, primary_key=True, index=True)
    record = Column(String(1024), index=True)
    sort = Column(Integer)

    zone_id = Column(ForeignKey("zones.id", ondelete="CASCADE"), index=True)
    zone = relationship(
        "bountydns.db.models.zone.Zone",
        foreign_keys="bountydns.db.models.dns_record.DnsRecord.zone_id",
        back_populates="dns_records",
    )
