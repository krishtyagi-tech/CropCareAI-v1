from fastapi import Header, HTTPException
from firebase_admin import auth


def get_current_user(authorization: str = Header(None)):

    if authorization is None:

        raise HTTPException(
            status_code=401,
            detail="Authorization header missing"
        )

    if not authorization.startswith("Bearer "):

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    token = authorization.split(" ")[1]

    try:

        decoded = auth.verify_id_token(token)

        return decoded

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Invalid Firebase Token"
        )