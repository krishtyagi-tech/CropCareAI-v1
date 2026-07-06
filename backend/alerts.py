from fastapi import APIRouter
from utils.database import get_current_alerts

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)


@router.get("/")
def alerts():

    try:

        return {
            "success": True,
            "data": get_current_alerts()
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }