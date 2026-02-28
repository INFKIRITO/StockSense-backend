from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship 
from database import Base

class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String)
    current_stock = Column(Integer)
    reorder_level = Column(Integer)

    class Sale(Base):
        __tablename__ = "sales"

        id = Column(Integer, primary_key=True, index=True)
        medicine_id = Column(Integer, ForeignKey("medicines.id"))
        quantity_sold = Column(Integer)
        sale_date = Column(Date)

        medicine = relationship("Medicine", back_populates="sales")