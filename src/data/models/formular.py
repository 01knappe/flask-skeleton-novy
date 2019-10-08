from datetime import datetime, timedelta
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Boolean, Integer, String, DateTime

from ..database import db
from ..mixins import CRUDModel

class Formular(CRUDModel):
    __tablename__ = 'formular'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True )
    jmeno = Column(String, nullable=False, index=False)
    prijmeni = Column(String, nullable=False, index=True)



