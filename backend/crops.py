from fastapi import APIRouter
from pydantic import BaseModel

from utils.database import (
    add_crop,
    get_crops
)

router = APIRouter(
    prefix="/crops",
    tags=["Crops"]
)


# =====================================
# Crop Model
# =====================================

class Crop(BaseModel):
    crop_name: str
    plant_id: str
    field_name: str
    planting_date: str


# =====================================
# Get All Crops
# =====================================

@router.get("/")
def get_all_crops_api():

    try:

        rows = get_crops()

        crops = []

        for row in rows:

            crops.append({

                "id": row[0],
                "user_uid": row[1],
                "crop_name": row[2],
                "plant_id": row[3],
                "field_name": row[4],
                "planting_date": row[5]

            })

        return {

            "success": True,
            "count": len(crops),
            "data": crops

        }

    except Exception as e:

        return {

            "success": False,
            "error": str(e)

        }


# =====================================
# Add Crop
# =====================================

@router.post("/")
def create_crop(crop: Crop):

    try:

        add_crop(

            "TEST_USER",

            crop.crop_name,

            crop.plant_id,

            crop.field_name,

            crop.planting_date

        )

        return {

            "success": True,
            "message": "Crop Registered"

        }

    except Exception as e:

        return {

            "success": False,
            "error": str(e)

        }