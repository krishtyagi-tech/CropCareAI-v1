import streamlit as st

def dashboard():

    st.title("🌿 CropCareAI")

    st.write("Welcome to CropCareAI")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("📷 Scan Crop", use_container_width=True):

            st.session_state.screen = "scan"
            st.rerun()

    with col2:

        if st.button("📂 My Crops", use_container_width=True):

            st.session_state.screen = "my_crops"
            st.rerun()