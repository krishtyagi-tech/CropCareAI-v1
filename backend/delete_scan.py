from fastapi import APIRouter
from utils.database import delete_scan

router = APIRouter(
    prefix="/scan",
    tags=["Delete Scan"]
)


@router.delete("/{scan_id}")
def remove_scan(scan_id: int):

    try:

        delete_scan(scan_id)

        return {
            "success": True,
            "message": "Scan deleted successfully."
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }