from fastapi import APIRouter

router = APIRouter()

current_user = {}


@router.post("/session")
def create_session(data: dict):

    global current_user

    current_user = data

    return {
        "success": True
    }


@router.get("/session")
def get_session():

    return current_user