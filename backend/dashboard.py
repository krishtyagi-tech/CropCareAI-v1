from fastapi import APIRouter
from utils.database import get_dashboard_stats

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def dashboard():

    try:

        stats = get_dashboard_stats()

        return {
            "success": True,
            "data": stats
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }