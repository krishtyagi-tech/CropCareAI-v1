import streamlit as st

def crop_workspace():

    st.button(
        "⬅ My Crops",
        on_click=lambda: st.session_state.update(
            {"screen":"my_crops"}
        )
    )

    st.title("🌱 Crop Workspace")

    st.info("Everything about one crop will come here.")