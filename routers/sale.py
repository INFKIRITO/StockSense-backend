from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.sale import Sale
from models.medicines import Medicine
from schemas.sale import SaleCreate, SaleResponse
from services.inventory_service import reduce_stock
from typing import List

router = APIRouter(prefix="/sales", tags=["Sales"])

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

@router.post("/", response_model=SaleResponse)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    
    medicine = reduce_stock(db, sale.medicine_id, sale.quantity_sold)
    
    if not medicine:
        raise HTTPException(
        status_code=404,
        detail="Medicine not found"
    )

    db_sale = Sale(**sale.model_dump())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)

    return db_sale


@router.get("/", response_model=List[SaleResponse])
def get_sales(db: Session = Depends(get_db)):
    return db.query(Sale).all()

