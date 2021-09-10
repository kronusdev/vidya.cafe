from sqlalchemy import *
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from files.__main__ import Base
import time


class Strikes(Base):

    __tablename__ = "strikes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    strike_reason = Column(String(500))
    strike_utc = Column(Integer, default=0)
    strike_expires_utc = Column(Integer, default=0)
    strike_url = Column(String(255))

    user = relationship("User",
                        uselist=False,
                        lazy="joined",
                        primaryjoin="Strikes.user_id==User.id"
                        )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<Strikes({self.id})>"
    
    @property
    def is_active(self):
        return self.strike_expires_utc < int(time.time())

    @property
    def strike_expires_timestamp(self):
        return datetime.utcfromtimestamp(self.strike_expires_utc).strftime('%Y-%m-%d %H:%M:%S')
    