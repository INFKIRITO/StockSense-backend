from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from services.inventory_service import get_low_stock_medicines
from schemas.medicines import MedicineResponse
from typing import List

router = APIRouter(prefix="/alerts", tags=["Inventory Alerts"])

def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()

@router.get("/", response_model=List[MedicineResponse])
def low_stock_alerts(db: Session = Depends(get_db)):
    return get_low_stock_medicines(db)