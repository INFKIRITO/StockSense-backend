from pydantic import BaseModel
from datetime import date

class SaleBase(BaseModel):
    medicine_id: int
    quantity_sold: int

class SaleCreate(SaleBase):
    pass

class SaleResponse(SaleBase):
    id: int
    date: date

    class Config:
        from_attributes = True