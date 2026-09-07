from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.medicines import Medicine
from models.sale import Sale
from datetime import datetime
from pydantic import BaseModel
from typing import List
import pandas as pd

router = APIRouter(prefix="/upload", tags=["Uploads"])


# ---------------- DATABASE DEPENDENCY ---------------- #

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


# ---------------- MEDICINE CSV UPLOAD ---------------- #

@router.post("/medicines")
async def upload_medicines_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    df = pd.read_csv(file.file)

    required_columns = {"name", "category", "current_stock", "reorder_level"}

    if not required_columns.issubset(df.columns):
        raise HTTPException(
            status_code=400,
            detail=f"CSV must contain columns: {required_columns}"
        )

    inserted = 0
    errors = []

    for index, row in df.iterrows():
        try:
            if row["current_stock"] < 0 or row["reorder_level"] < 0:
                raise ValueError("Stock values cannot be negative")

            medicine = Medicine(
                name=row["name"],
                category=row["category"],
                current_stock=int(row["current_stock"]),
                reorder_level=int(row["reorder_level"])
            )

            db.add(medicine)
            inserted += 1

        except Exception as e:
            errors.append({
                "row": index + 1,
                "error": str(e)
            })

    return {
        "inserted_records": inserted,
        "errors": errors
    }


# ---------------- SALES CSV UPLOAD ---------------- #

@router.post("/sales")
async def upload_sales_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    df = pd.read_csv(file.file)

    required_columns = {"product", "quantity", "revenue", "date"}

    if not required_columns.issubset(df.columns):
        raise HTTPException(
            status_code=400,
            detail=f"CSV must contain columns: {required_columns}"
        )

    inserted = 0
    errors = []

    for index, row in df.iterrows():
        try:
            medicine = db.query(Medicine).filter(
                Medicine.name == row["product"]
            ).first()

            if not medicine:
                raise ValueError("Medicine not found")

            quantity = int(row["quantity"])

            if medicine.current_stock < quantity:
                raise ValueError("Not enough stock available")

            sale = Sale(
                medicine_id=medicine.id,
                quantity_sold=quantity,
                date=datetime.strptime(row["date"], "%Y-%m-%d").date()
            )

            medicine.current_stock -= quantity
            db.add(sale)
            inserted += 1

        except Exception as e:
            errors.append({
                "row": index + 1,
                "error": str(e)
            })

    return {
        "inserted_records": inserted,
        "errors": errors
    }


# ---------------- MANUAL SALES JSON UPLOAD ---------------- #

class ManualSale(BaseModel):
    product: str
    quantity: int
    date: datetime


@router.post("/sales/manual")
def upload_sales_manual(
    entries: List[ManualSale],
    db: Session = Depends(get_db)
):

    inserted = 0

    for entry in entries:

        medicine = db.query(Medicine).filter(
            Medicine.name == entry.product
        ).first()

        if not medicine:
            raise HTTPException(
                status_code=404,
                detail=f"Medicine '{entry.product}' not found"
            )

        if medicine.current_stock < entry.quantity:
            raise HTTPException(
                status_code=400,
                detail="Not enough stock available"
            )

        sale = Sale(
            medicine_id=medicine.id,
            quantity_sold=entry.quantity,
            date=entry.date
        )

        medicine.current_stock -= entry.quantity
        db.add(sale)
        inserted += 1

    return {"inserted_records": inserted}