import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

import os

# Initialize Firebase only once
if not firebase_admin._apps:

    cred = credentials.Certificate(
        os.path.join(
            "secrets",
            "firebase-admin.json"
        )
    )

    firebase_admin.initialize_app(cred)
print("Firebase Admin Initialized ✅")