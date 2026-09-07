from sqlalchemy.orm import Session
from models.medicines import Medicine

def reduce_stock(db: Session, medicine_id: int, quantity: int):
    medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    
    if not medicine:
        return None
    
    medicine.current_stock -= quantity
    db.commit()
    db.refresh(medicine)
    
    return medicine


def get_low_stock_medicines(db: Session):
    medicines = db.query(Medicine).all()
    
    low_stock = [
        med for med in medicines
        if med.current_stock < med.reorder_level
    ]
    
    return low_stock