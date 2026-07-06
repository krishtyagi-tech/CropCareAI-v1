from fastapi import APIRouter
from utils.database import get_scans_with_crop

router = APIRouter(
    prefix="/history",
    tags=["History"]
)


@router.get("/")
def history():

    try:

        rows = get_scans_with_crop()

        return {
            "success": True,
            "data": rows
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }