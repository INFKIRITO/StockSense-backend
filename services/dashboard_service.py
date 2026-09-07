from sqlalchemy.orm import Session
from sqlalchemy import func
from models.medicines import Medicine
from models.sale import Sale


def get_dashboard_data(db: Session):

    total_medicines = db.query(func.count(Medicine.id)).scalar()

    total_sales = db.query(func.sum(Sale.quantity_sold)).scalar() or 0

    low_stock_count = db.query(func.count(Medicine.id)) \
        .filter(Medicine.current_stock < Medicine.reorder_level) \
        .scalar()

    # Top selling medicines
    top_selling = db.query(
    Medicine.name,
    func.sum(Sale.quantity_sold).label("total_sold")
    ).join(Sale, Sale.medicine_id == Medicine.id) \
    .group_by(Medicine.name) \
    .order_by(func.sum(Sale.quantity_sold).desc()) \
    .limit(5).all()

    return {
        "total_medicines": total_medicines,
        "total_sales_quantity": total_sales,
        "low_stock_count": low_stock_count,
        "top_selling": [
            {
                "total_sold": item.total_sold
            }
            for item in top_selling
        ]
    }