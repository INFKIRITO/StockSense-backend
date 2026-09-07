from sqlalchemy import Column, Integer, String, UniqueConstraint
from database import Base

class Medicine(Base):
    __tablename__ = "medicines"

    __table_args__ = (UniqueConstraint('name', name='unique_medicine_name'),)

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String)
    current_stock = Column(Integer)
    reorder_level = Column(Integer)