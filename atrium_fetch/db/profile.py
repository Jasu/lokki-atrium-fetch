from atrium_fetch.db.base import Base
from sqlalchemy.orm import relationship, backref

from sqlalchemy import Column, Integer, String

class Profile(Base):
  __tablename__ = 'profiles'

  id = Column(Integer, primary_key=True, nullable=False)
  handle = Column(String(63), nullable=False, unique=True)

  lokki_db = Column(String(255), nullable=False)
  lokki_client_handle = Column(String(255))

  price_per_hour = Column(String(15))

  endpoint = Column(String(255))
  view_name = Column(String(255))
  display_name = Column(String(255))

  additional_lokki_db = Column(String(255))

