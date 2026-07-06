from fastapi import APIRouter
from pydantic import BaseModel

from utils.database import (
    save_scan,
    get_scans
)

router = APIRouter(
    prefix="/scan",
    tags=["Scan"]
)


class ScanRequest(BaseModel):

    crop_id: int

    image_path: str

    disease: str

    status: str

    confidence: float

    city: str

    temperature: float

    humidity: float

    pressure: float

    wind_speed: float

    weather: str

    ai_chat: str


@router.post("/")
def create_scan(data: ScanRequest):

    try:

        save_scan(

            data.crop_id,

            data.image_path,

            data.disease,

            data.status,

            data.confidence,

            data.city,

            data.temperature,

            data.humidity,

            data.pressure,

            data.wind_speed,

            data.weather,

            data.ai_chat

        )

        return {

            "success": True,

            "message": "Scan Saved"

        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)

        }


@router.get("/{crop_id}")
def scan_history(crop_id: int):

    try:

        scans = get_scans(crop_id)

        return {

            "success": True,

            "data": scans

        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)

        }