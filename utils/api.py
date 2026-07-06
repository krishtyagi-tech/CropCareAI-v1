import requests
import streamlit as st


API_URL = "https://cropcareai-v1.onrender.com"


def get_headers():

    if "firebase_token" not in st.session_state:

        return {}

    return {
        "Authorization": f"Bearer {st.session_state.firebase_token}"
    }


def api_get(endpoint):

    return requests.get(
        f"{API_URL}{endpoint}",
        headers=get_headers()
    )


def api_post(endpoint, data):

    return requests.post(
        f"{API_URL}{endpoint}",
        json=data,
        headers=get_headers()
    )


def api_delete(endpoint):

    return requests.delete(
        f"{API_URL}{endpoint}",
        headers=get_headers()
    )


def api_put(endpoint, data):

    return requests.put(
        f"{API_URL}{endpoint}",
        json=data,
        headers=get_headers()
    )