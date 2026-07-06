from fastapi import APIRouter
from utils.database import get_recent_activity

router = APIRouter(
    prefix="/activity",
    tags=["Activity"]
)


@router.get("/")
def activity():

    try:

        return {
            "success": True,
            "data": get_recent_activity()
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }