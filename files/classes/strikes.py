from sqlalchemy import *
from sqlalchemy.orm import relationship
from files.__main__ import Base
import time

class Strikes(Base):
    __tablename__ = "strikes"
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    reason = Column(String(500))
    strike_utc = Column(Integer, default=0)


    user = relationship(
        "User",
        uselist=False,
        primaryjoin="User.id==Strikes.user_id")
    
    def __init__(self, *args, **kwargs):
	    super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"<Strikes(id={self.id})>"