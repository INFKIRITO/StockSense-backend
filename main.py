from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
from models import medicines, sale

from routers import medicine as medicine_router
from routers import alerts as alerts_router
from routers import sale as sale_router
from routers import uploads as upload_router
from routers import dashboard as dashboard_router


# ---------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------

app = FastAPI(
    title="StockSense API",
    description="Medical Store Inventory Management API",
    version="1.0.0",
)


# ---------------------------------------------------------
# CORS Configuration
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # Production frontend
        "https://stocksense-frontend-ai0r.onrender.com",

        # Local development
        "http://localhost:8080",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Database Tables
# ---------------------------------------------------------

# Create database tables if they don't already exist.
# NOTE: For production, Alembic migrations are recommended.
try:
    medicines.Base.metadata.create_all(bind=engine)
    sale.Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Database initialization warning: {e}")


# ---------------------------------------------------------
# Root / Health Check
# ---------------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "StockSense Backend Running 🚀",
        "status": "healthy"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# ---------------------------------------------------------
# API Routers
# ---------------------------------------------------------

app.include_router(medicine_router.router)
app.include_router(sale_router.router)
app.include_router(alerts_router.router)
app.include_router(upload_router.router)
app.include_router(dashboard_router.router)