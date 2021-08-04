from sqlalchemy import *
from flask import g
<<<<<<< HEAD:drama/classes/images.py
from drama.__main__ import Base
import os, random
=======
from files.__main__ import Base

>>>>>>> df20530d2b49c78a8af64ef8f9c953e974de2cc5:files/classes/images.py

class Image(Base):
	__tablename__ = "images"
	id = Column(BigInteger, primary_key=True)
	state = Column(String(8))
	number = Column(Integer)
	text = Column(String(64))
	deletehash = Column(String(64))

	@property
	def path(self):
		onlyfiles = next(os.walk("/assets/images/loginbackgrounds"))[2] #dir is your directory path as string
		nFiles = len(onlyfiles)
		pic = random.randint(1, nFiles)
		return f"/assets/images/loginbackgrounds/bg-{pic}.png"

		#return f"/assets/images/platy.jpg"

def random_background():
	#change the 2nd number when adding backgrounds
	pic = random.randint(1, 11)
	return f"/assets/images/loginbackgrounds/bg-{pic}"

def random_image():
	n=g.db.query(Image).count()
	return g.db.query(Image).order_by(Image.id.asc()).first()



class BadPic(Base):

	#Class for tracking fuzzy hashes of banned csam images

	__tablename__="badpics"
	id = Column(BigInteger, primary_key=True)
	description=Column(String(255))
	phash=Column(String(64))
	ban_reason=Column(String(64))
	ban_time=Column(Integer)

	
