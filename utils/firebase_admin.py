import os
import firebase_admin
from firebase_admin import credentials

if not firebase_admin._apps:

    firebase_path = os.getenv("FIREBASE_ADMIN_JSON")

    if firebase_path and os.path.exists(firebase_path):
        cred = credentials.Certificate(firebase_path)
    else:
        cred = credentials.Certificate(
            os.path.join("secrets", "firebase-admin.json")
        )

    firebase_admin.initialize_app(cred)

print("Firebase Admin Initialized ✅")