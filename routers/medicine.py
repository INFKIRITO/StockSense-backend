from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from models.medicines import Medicine
from models.sale import Sale
from schemas.medicines import MedicineCreate, MedicineResponse
from typing import List

router = APIRouter(prefix="/medicines", tags=["Medicines"])

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

@router.post("/", response_model=MedicineResponse)
def create_medicine(medicine: MedicineCreate, db: Session = Depends(get_db)):
    existing_medicine = db.query(Medicine).filter(Medicine.name == medicine.name).first()
    if existing_medicine:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A medicine with this name already exists",
        )

    db_medicine = Medicine(**medicine.model_dump())
    db.add(db_medicine)
    db.commit()
    db.refresh(db_medicine)
    return db_medicine


@router.get("/", response_model=List[MedicineResponse])
def get_medicines(db: Session = Depends(get_db)):
    return db.query(Medicine).all()


@router.delete("/{medicine_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_medicine(medicine_id: int, db: Session = Depends(get_db)):
    medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not medicine:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medicine not found")

    has_sales = db.query(Sale.id).filter(Sale.medicine_id == medicine_id).first()
    if has_sales:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This medicine cannot be deleted because it has sales history",
        )

    db.delete(medicine)
    db.commit()
