from decimal import Decimal
from sqlalchemy import *
from files.__main__ import Base

class Donation(Base):
	__tablename__ = "donations"
	id = Column(Integer, primary_key=True)
	amount = Column(Decimal, default=0.00)
	currency = Column(String, default="USD")
	purchase_id = Column(String, default="")
	purchase_email = Column(String)
	data = Column(String)
	payment_company = Column(String)