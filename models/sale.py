from sqlalchemy import Column, Integer, Date, ForeignKey
from datetime import date
from database import Base

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    medicine_id = Column(Integer, ForeignKey("medicines.id"))
    date = Column(Date, default=date.today)
    quantity_sold = Column(Integer)