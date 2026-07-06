from fastapi import APIRouter
from utils.database import (
    get_health_distribution,
    get_crop_distribution
)

router = APIRouter(
    prefix="/charts",
    tags=["Charts"]
)


@router.get("/health")
def health_distribution():

    try:

        return {
            "success": True,
            "data": get_health_distribution()
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


@router.get("/crop")
def crop_distribution():

    try:

        return {
            "success": True,
            "data": get_crop_distribution()
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }