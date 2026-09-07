from pydantic import BaseModel

class MedicineBase(BaseModel):
    name: str
    category: str
    current_stock: int
    reorder_level: int

class MedicineCreate(MedicineBase):
    pass

class MedicineResponse(MedicineBase):
    id: int

    class Config:
        from_attributes = True