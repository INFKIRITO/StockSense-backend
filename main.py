from fastapi import FastAPI
from database import engine
from models import medicines, sale
from routers import medicine as medicine_router
from routers import alerts as alerts_router
from routers import sale as sale_router
from routers import uploads as upload_router
from routers import dashboard as dashboard_router
from fastapi.middleware.cors import CORSMiddleware
import os


medicines.Base.metadata.create_all(bind=engine)
sale.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Comma-separated public frontend origins. The local address remains available
# for development; production supplies the Render static-site URL.
allowed_origins = [
    origin.strip()
    for origin in os.getenv("FRONTEND_ORIGINS", "http://localhost:8080").split(",")
    if origin.strip()
]
allowed_origin_regex = os.getenv(
    "FRONTEND_ORIGIN_REGEX",
    r"https://stocksense-frontend(?:-[a-z0-9]+)?\.onrender\.com",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=allowed_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "StockSense Backend Running 🚀"}

app.include_router(medicine_router.router)  
app.include_router(sale_router.router)
app.include_router(alerts_router.router)
app.include_router(upload_router.router)
app.include_router(dashboard_router.router)
