import streamlit as st
import os
from collections import defaultdict

from utils.pdf_report import (
    create_pdf,
    create_complete_report
)

from utils.database import (
    get_scans_with_crop,
    get_complete_plant_history,
    delete_scan,
    delete_crop
)
import tempfile
import requests
st.set_page_config(
    page_title="My Crops",
    page_icon="📂",
    layout="wide"
)

if st.button("⬅ Dashboard"):
    st.switch_page("app.py")

st.title("📂 My Crops")

st.caption(
    "Browse your registered plants, scan history and reports."
)

st.divider()

st.subheader("🔍 Search & Filters")

search = st.text_input(
    "",
    placeholder="Search by Plant ID..."
)

col1, col2 = st.columns(2)

with col1:

    crop_filter = st.selectbox(

        "🌱 Crop",

        [
            "All",
            "Tomato",
            "Potato",
            "Pepper"
        ]

    )

with col2:

    status_filter = st.selectbox(

        "Status",

        [
            "All",
            "Healthy",
            "Diseased"
        ]

    )

st.divider()
# =====================================================
# Open selected alert automatically
# =====================================================

selected_history = st.session_state.get("selected_history")

selected_crop_id = None
selected_scan_date = None

if selected_history:

    selected_crop_id = selected_history["crop_id"]
    selected_scan_date = selected_history["latest_scan"]

# =====================================================
# Load Records
# =====================================================

response = requests.get(
    "https://cropcareai-v1.onrender.com/history/"
)

result = response.json()

if result["success"]:
    records = result["data"]
else:
    records = []

if not records:

    st.info("No saved scans yet.")

else:

    crops = defaultdict(lambda: defaultdict(list))

    for record in records:

        (
            scan_id,
            crop_id,
            crop_name,
            plant_id,
            field_name,
            image_path,
            disease,
            status,
            confidence,
            city,
            temperature,
            humidity,
            pressure,
            wind_speed,
            weather,
            ai_chat,
            scan_date
        ) = record

        # -----------------------------
        # Search Filter
        # -----------------------------

        if search:

            if search.lower() not in plant_id.lower():

                continue

        # -----------------------------
        # Crop Filter
        # -----------------------------

        if crop_filter != "All":

            if crop_name != crop_filter:

                continue

        # -----------------------------
        # Status Filter
        # -----------------------------

        if status_filter != "All":

            if status_filter not in status:

                continue

        # Add remaining records
        crops[crop_name][plant_id].append(record)

    # =====================================================
    # Crop Folder
    # =====================================================

    for crop_name in sorted(crops.keys()):

        with st.expander(
            f"🌱 {crop_name}",
            expanded=True
        ):

            plant_dict = crops[crop_name]

            # =====================================================
            # Plant Folder
            # =====================================================

            for plant_id, scans in plant_dict.items():

                field_name = scans[0][4]

                crop_id = scans[0][1]

                open_plant = (
                    crop_id == selected_crop_id
                )

                with st.expander(
                    f"🌿 {plant_id} ({len(scans)} scans)",
                    expanded=open_plant
                ):

                    st.caption(f"🌾 {field_name}")
                    # =====================================================
                    # Plant Health Summary
                    # =====================================================

                    latest_scan = scans[0]

                    latest_status = latest_scan[7]
                    latest_disease = latest_scan[6]
                    latest_confidence = latest_scan[8]
                    latest_scan_date = latest_scan[16]

                    first_scan_date = scans[-1][16]

                    st.markdown("### 📊 Plant Health Summary")

                    c1, c2, c3 = st.columns(3)

                    with c1:

                        st.metric(
                            "Latest Status",
                            latest_status
                        )

                        st.metric(
                            "Total Scans",
                            len(scans)
                        )

                    with c2:

                        st.metric(
                            "Disease",
                            latest_disease
                        )

                        st.metric(
                            "Confidence",
                            f"{latest_confidence:.2f}%"
                        )

                    with c3:

                        st.metric(
                            "First Scan",
                            first_scan_date[:10]
                        )

                        st.metric(
                            "Last Scan",
                            latest_scan_date[:10]
                        )

                    st.divider()

                    # ==========================================
                    # Delete Plant
                    # ==========================================

                    if st.button(
                        "🗑 Delete Plant",
                        key=f"delete_crop_{crop_id}"
                    ):

                        response = requests.delete(
                            f"https://cropcareai-v1.onrender.com/crop/{crop_id}"
                        )

                        result = response.json()

                        if result["success"]:

                            st.success("✅ Plant deleted successfully!")

                            st.rerun()

                        else:

                            st.error(result["error"])

                    st.divider()

                    # ===========================================
                    # Complete Plant Report
                    # ===========================================

                    if st.button(
                        "📚 Download Complete Plant Report",
                        key=f"complete_{crop_id}"
                    ):

                        history = get_complete_plant_history(crop_id)

                        pdf_path = os.path.join(
                            tempfile.gettempdir(),
                            f"{plant_id}_Complete_Report.pdf"
                        )

                        create_complete_report(
                            output_path=pdf_path,
                            history=history
                        )

                        with open(pdf_path, "rb") as pdf_file:

                            st.download_button(
                                "⬇ Download Complete Report",
                                pdf_file,
                                file_name=f"{plant_id}_Complete_Report.pdf",
                                mime="application/pdf",
                                key=f"download_complete_{crop_id}"
                            )

                    st.divider()
                    st.markdown("### 📈 Progress Timeline")

                    
                    scan_number = len(scans)

                    for scan in scans:

                        (
                            scan_id,
                            crop_id,
                            crop_name,
                            plant_id,
                            field_name,
                            image_path,
                            disease,
                            status,
                            confidence,
                            city,
                            temperature,
                            humidity,
                            pressure,
                            wind_speed,
                            weather,
                            ai_chat,
                            scan_date
                        ) = scan

                        scan_open = (
                            crop_id == selected_crop_id
                            and scan_date == selected_scan_date
                        )

                        icon = "🟢" if "Healthy" in status else "🔴"

                        title = (
                            f"{icon} "
                            f"Scan #{scan_number}   "
                            f"{scan_date[:10]}"
                        )

                        with st.expander(
                            title,
                            expanded=scan_open
                        ):

                            left, right = st.columns([1, 2])

                            with left:

                                if os.path.exists(image_path):

                                    st.image(
                                        image_path,
                                        use_container_width=True
                                    )

                                else:

                                    st.warning("Image not found.")

                            with right:

                                if "Healthy" in status:

                                    st.success(f"🟢 {disease}")

                                else:

                                    st.error(f"🔴 {disease}")

                                st.metric(
                                    "Confidence",
                                    f"{confidence:.2f}%"
                                )

                                st.metric(
                                    "Status",
                                    status
                                )

                                st.write(
                                    f"📍 **City:** {city}"
                                )

                                st.write(
                                    f"🌡 **Temperature:** {temperature} °C"
                                )

                                st.write(
                                    f"💧 **Humidity:** {humidity}%"
                                )

                                st.write(
                                    f"☁ **Weather:** {weather.title()}"
                                )

                                st.write(
                                    f"📅 **Scan Date:** {scan_date}"
                                )
                                # -----------------------------
                                # PDF Report
                                # -----------------------------

                                st.divider()

                                if st.button(
                                    "📄 Generate PDF Report",
                                    key=f"pdf_{scan_id}"
                                ):

                                    pdf_path = os.path.join(
                                        tempfile.gettempdir(),
                                        f"{plant_id}_{scan_id}.pdf"
                                    )

                                    create_pdf(
                                        output_path=pdf_path,
                                        crop_name=crop_name,
                                        plant_id=plant_id,
                                        field_name=field_name,
                                        disease=disease,
                                        status=status,
                                        confidence=confidence,
                                        city=city,
                                        temperature=temperature,
                                        humidity=humidity,
                                        weather=weather,
                                        scan_date=scan_date,
                                        image_path=image_path,
                                        ai_chat=ai_chat if ai_chat else "No AI conversation."
                                    )

                                    with open(pdf_path, "rb") as pdf_file:

                                        st.download_button(
                                            "⬇ Download PDF",
                                            pdf_file,
                                            file_name=f"{plant_id}_report.pdf",
                                            mime="application/pdf",
                                            key=f"download_{scan_id}"
                                        )
                                st.divider()

                            if st.button(
                                "🗑 Delete Scan",
                                key=f"delete_scan_{scan_id}"
                            ):

                                response = requests.delete(
                                    f"https://cropcareai-v1.onrender.com/scan/{scan_id}"
                                )

                                result = response.json()

                                if result["success"]:

                                    st.success("✅ Scan deleted!")

                                    st.rerun()

                                else:

                                    st.error(result["error"])
                                    
                            if ai_chat:
                                with st.expander(
                                     "🤖 AI Conversation"
                                    ):

                                    st.text(ai_chat)

                        scan_number -= 1
# =====================================================
# Clear selected history after opening once
# =====================================================

if "selected_history" in st.session_state:
    del st.session_state["selected_history"]