from sqlalchemy import *
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from files.__main__ import Base
import time

class Strikes(Base):
    __tablename__ = "strikes"
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    strike_reason = Column(String(500))
    strike_utc = Column(Integer, default=0)
    strike_expires_utc = Column(Integer, default=0)


    user = relationship(
        "User",
        uselist=False,
        primaryjoin="User.id==Strikes.user_id")
    
    def __init__(self, *args, **kwargs):
	    super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"<Strikes(id={self.id})>"

    @property
    def user_id(self):
        return self.user_id
    
    @property
    def strike_reason(self):
        return self.strike_reason

    @property
    def strike_utc(self):
        return self.strike_utc
    
#    @property
#    def strike_expires_utc(self):
#        return int((datetime.utcfromtimestamp(self.strike_utc) + timedelta(days=30)).timestamp())
    
    @property
    def strike_timestamp(self):
        return datetime.utcfromtimestamp(self.strike_utc).strftime('%Y-%m-%d %H:%M:%S')
    

    @property
    def strike_expires_timestamp(self):
        return (datetime.utcfromtimestamp(self.strike_utc) + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')

    @property
    def is_active(self):
        return self.strike_expires_utc < int(time.time())