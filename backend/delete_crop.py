from fastapi import APIRouter
from utils.database import delete_crop

router = APIRouter(
    prefix="/crop",
    tags=["Delete Crop"]
)


@router.delete("/{crop_id}")
def remove_crop(crop_id: int):

    try:

        delete_crop(crop_id)

        return {
            "success": True,
            "message": "Crop deleted successfully."
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }