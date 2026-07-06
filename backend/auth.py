import utils.firebase_admin

from fastapi import APIRouter
from pydantic import BaseModel
from firebase_admin import auth

router = APIRouter()


class TokenRequest(BaseModel):
    token: str


@router.post("/verify-token")
def verify_token(data: TokenRequest):

    try:

        decoded = auth.verify_id_token(data.token)

        return {
            "success": True,
            "uid": decoded["uid"],
            "email": decoded.get("email"),
            "name": decoded.get("name")
        }

    except Exception as e:

        print("VERIFY TOKEN ERROR:", e)

        return {
            "success": False,
            "error": str(e)
        }