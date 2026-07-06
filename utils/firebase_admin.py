import firebase_admin
from firebase_admin import credentials
import streamlit as st

if not firebase_admin._apps:

    cred = credentials.Certificate(
        dict(st.secrets["firebase"])
    )

    firebase_admin.initialize_app(cred)

print("Firebase Admin Initialized ✅")