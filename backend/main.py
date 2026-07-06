from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.auth import router as auth_router
from backend.session import router as session_router
from backend.crops import router as crop_router
from backend.dashboard import router as dashboard_router
from backend.charts import router as charts_router
from backend.alerts import router as alerts_router
from backend.activity import router as activity_router
from backend.scan import router as scan_router
from backend.history import router as history_router
from backend.delete_crop import router as delete_crop_router
from backend.delete_scan import router as delete_scan_router

app = FastAPI(
    title="CropCareAI Backend",
    version="1.0.0"
)

# -----------------------------
# CORS Configuration
# -----------------------------

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",

    # Vercel (we'll replace later)
    "https://your-project.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Routes
# -----------------------------

app.include_router(auth_router)
app.include_router(session_router)
app.include_router(crop_router)
app.include_router(dashboard_router)
app.include_router(charts_router)
app.include_router(alerts_router)
app.include_router(activity_router)
app.include_router(scan_router)
app.include_router(history_router)
app.include_router(delete_crop_router)
app.include_router(delete_scan_router)

@app.get("/")
def home():
    return {
        "message": "CropCareAI Backend Running 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "OK"
    }