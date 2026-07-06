import sqlite3
import streamlit as st

from utils.database import (
    create_tables,
    add_crop,
    get_all_crops,
    get_dashboard_stats,
    get_current_alerts,
    get_health_distribution,
    get_crop_distribution,
    get_recent_activity
)
import plotly.express as px
import pandas as pd
import requests
# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="CropCareAI",
    page_icon="🌿",
    layout="wide"
)
st.markdown("""
<style>

/* Metric Cards */

div[data-testid="stMetric"] {

    background-color: #f8fafc;

    border: 1px solid #dbeafe;

    padding: 18px;

    border-radius: 15px;

    text-align: center;

    box-shadow: 0px 3px 8px rgba(0,0,0,0.08);

}

/* Metric Value */

div[data-testid="stMetricValue"] {

    font-size: 34px;

    font-weight: bold;

    color: #15803d;

}

/* Metric Label */

div[data-testid="stMetricLabel"] {

    font-size: 16px;

    font-weight: 600;

}

.metric-card{
    background:#1e293b;
    border-left:6px solid #22c55e;
    border-radius:15px;
    padding:12px 16px;
    margin-bottom:10px;
    box-shadow:0 4px 12px rgba(0,0,0,.25);
}

.metric-title{
    color:#cbd5e1;
    font-size:16px;
    font-weight:600;
}

.metric-value{
    color:white;
    font-size:30px;
    font-weight:700;
    margin-top:8px;
}            
.metric-value{
    font-size:40px;
    font-weight:800;
}
.alert-card{
    background:#1e293b;
    border-left:6px solid #ef4444;
    border-radius:14px;
    padding:18px;
    margin-bottom:15px;
}

.alert-title{
    color:white;
    font-size:24px;
    font-weight:700;
}

.alert-subtitle{
    color:#94a3b8;
    font-size:15px;
}

.alert-disease{
    color:#f87171;
    font-size:18px;
    font-weight:600;
}

.alert-date{
    color:#cbd5e1;
    font-size:14px;
}

/* ============================= */
/* Sidebar */
/* ============================= */

section[data-testid="stSidebar"] {

    background-color:#1f2937;

}

section[data-testid="stSidebar"] .stButton>button{

    width:100%;

    height:50px;

    border-radius:12px;

    font-weight:700;

    font-size:16px;

    background:#22c55e;

    color:white;

    border:none;

    transition:0.25s;

}

section[data-testid="stSidebar"] .stButton>button:hover{

    background:#16a34a;

    transform:translateY(-2px);

}

section[data-testid="stSidebar"] input{

    border-radius:12px !important;

}

section[data-testid="stSidebar"] textarea{

    border-radius:12px !important;

}

section[data-testid="stSidebar"] [data-baseweb="select"]{

    border-radius:12px !important;

}

section[data-testid="stSidebar"] .stDateInput{

    border-radius:12px;

}
</style>
""", unsafe_allow_html=True)

create_tables()
try:
    response = requests.get(
        "https://cropcareai-v1.onrender.com/session",
        timeout=30
    )

    if response.status_code != 200:
        st.error(f"Backend returned {response.status_code}")
        st.stop()

    session = response.json()

    # if "uid" not in session:
    #     st.switch_page("pages/login.py")
    #     st.stop()

except requests.exceptions.Timeout:
    st.error("Backend is waking up. Please wait 30-60 seconds and refresh.")
    st.stop()

except requests.exceptions.ConnectionError:
    st.error("Cannot connect to backend.")
    st.stop()

except Exception as e:
    st.error(f"Unexpected error: {e}")
    st.stop()
    
# try:

#     session = requests.get(
#         "https://cropcareai-v1.onrender.com/session"
#     ).json()

#     if "uid" not in session:

#         st.error("Please login first.")

#         st.stop()

# except Exception:

#     st.error("Backend not running.")

#     st.stop()



# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:
    try:

        session = requests.get(
            "https://cropcareai-v1.onrender.com/session"
        ).json()

        if "name" in session:

            st.image(
                "https://cdn-icons-png.flaticon.com/512/149/149071.png",
                width=90
            )

            st.markdown(
                f"### 👤 {session['name']}"
            )

            st.caption(session["email"])

            st.divider()

    except Exception:

        pass

    st.markdown("""
    ## 🌿 CropCareAI

    AI Crop Monitoring System
    """)

    st.divider()

    st.subheader("🌱 Register Crop")

    st.caption("Crop")

    crop_name = st.selectbox(
        "",
        [
            "Tomato",
            "Potato",
            "Pepper"
        ]
    )

    st.caption("Plant ID")

    plant_id = st.text_input(
        "",
        placeholder="Tomato-01"
    )

    st.caption("Field Name")

    field_name = st.text_input(
        "",
        placeholder="North Field"
    )

    st.caption("Planting Date")

    planting_date = st.date_input("")

    if st.button(
        "💾 Register Crop",
        use_container_width=True
    ):

        if plant_id.strip() == "":

            st.warning("Plant ID cannot be empty.")

        else:

            try:

                response = requests.post(
                    "https://cropcareai-v1.onrender.com/crops/",
                    json={
                        "crop_name": crop_name,
                        "plant_id": plant_id,
                        "field_name": field_name,
                        "planting_date": str(planting_date)
                    }
                )

                result = response.json()

                if result["success"]:

                    st.success("✅ Crop Registered Successfully!")

                else:

                    st.error(result["error"])

            except Exception as e:

                st.error(f"Error: {e}")
    # -----------------------------------
    # Quick Tip (Always Visible)
    # -----------------------------------

    st.divider()

    st.success(
        """
### 🌿 Quick Tip

Register each plant only once.

Every future scan will automatically be linked to that plant.
"""
    )

st.subheader("🌾 Select Crop")

response = requests.get(
    "https://cropcareai-v1.onrender.com/crops/"
)

result = response.json()

if result["success"]:

    crops = result["data"]

else:

    crops = []

if len(crops) == 0:

    st.warning("No crops registered yet.")

else:

    selected_crop = st.selectbox(
        "Choose Crop",
        crops,
        format_func=lambda crop: f"{crop['plant_id']} ({crop['crop_name']})"
    )

    st.session_state.selected_crop = selected_crop

# =====================================================
# TITLE
# =====================================================

st.title("🌿 CropCareAI")

st.caption(
    "AI Powered Crop Monitoring & Disease Detection System"
)

st.divider()

st.subheader("📊 Dashboard Overview")
# =====================================================
# DASHBOARD
# =====================================================

response = requests.get(
    "https://cropcareai-v1.onrender.com/dashboard/"
)

result = response.json()

if result["success"]:

    stats = result["data"]

else:

    stats = {
        "plants": 0,
        "scans": 0,
        "healthy": 0,
        "diseased": 0
    }

st.divider()

c1, c2, c3, c4 = st.columns(4)

cards = [
    ("🌱 Total Plants", stats["plants"], "#22c55e"),
    ("📸 Total Scans", stats["scans"], "#3b82f6"),
    ("🟢 Healthy", stats["healthy"], "#16a34a"),
    ("🔴 Diseased", stats["diseased"], "#ef4444")
]

for col, (title, value, color) in zip(
    [c1, c2, c3, c4],
    cards
):

    with col:

        st.markdown(
            f"""
            <div class="metric-card" style="border-left-color:{color};">
                <div class="metric-title">{title}</div>
                <div class="metric-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
st.divider()
# =====================================================
# HEALTH CHART + CURRENT ALERTS
# =====================================================



# =====================================================
# Health Distribution + Crop Distribution
# =====================================================

# Health Distribution
response = requests.get(
    "https://cropcareai-v1.onrender.com/charts/health"
)

result = response.json()

if result["success"]:
    distribution = result["data"]
else:
    distribution = []


# Crop Distribution
response = requests.get(
    "https://cropcareai-v1.onrender.com/charts/crop"
)

result = response.json()

if result["success"]:
    crop_distribution = result["data"]
else:
    crop_distribution = []

# -----------------------------
# Health Distribution
# -----------------------------

df = pd.DataFrame(
    {
        "Status": [
            "Healthy",
            "Diseased"
        ],
        "Count": [
            distribution["Healthy"],
            distribution["Diseased"]
        ]
    }
)

fig = px.pie(
    df,
    names="Status",
    values="Count",
    hole=0.55,
    color="Status",
    color_discrete_map={
        "Healthy": "#22c55e",
        "Diseased": "#ef4444"
    }
)

fig.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

fig.update_layout(
    showlegend=True,
    margin=dict(
        l=10,
        r=10,
        t=40,
        b=10
    ),
    height=420
)

# -----------------------------
# Crop Distribution
# -----------------------------

if crop_distribution:

    df_crop = pd.DataFrame(
        crop_distribution,
        columns=["Crop", "Plants"]
    )

    fig_crop = px.bar(
        df_crop,
        x="Crop",
        y="Plants",
        text="Plants",
        title="Registered Plants by Crop"
    )

    fig_crop.update_traces(
        textposition="outside",
         marker_color="#22c55e"
    )

    fig_crop.update_layout(
        xaxis_title="Crop",
        yaxis_title="Number of Plants",
        height=420
    )

    # -----------------------------
    # Show Charts Side by Side
    # -----------------------------

    left_chart, right_chart = st.columns(2)

    with left_chart:

        with st.container(border=True):

            st.subheader("🥧 Health Distribution")

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    with right_chart:

        with st.container(border=True):

            st.subheader("🌱 Crop Distribution")

            st.plotly_chart(
                fig_crop,
                use_container_width=True
            )

else:

    st.subheader("🥧 Health Distribution")

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.info("No crop data available.")
# -----------------------------
# Current Alerts
# -----------------------------

# =====================================================
# CURRENT ALERTS
# =====================================================

# =====================================================
# CURRENT ALERTS
# =====================================================

st.divider()

st.subheader("⚠ Current Alerts")

response = requests.get(
    "https://cropcareai-v1.onrender.com/alerts/"
)

result = response.json()

if result["success"]:
    alerts = result["data"]
else:
    alerts = []

if len(alerts) == 0:

    st.success(
        "✅ All monitored plants are currently healthy."
    )

else:

    for alert in alerts:

        (
            crop_id,
            crop_name,
            plant_id,
            field_name,
            disease,
            status,
            scan_date
        ) = alert

        with st.container(border=True):

            top_left, top_right = st.columns([5, 1])

            with top_left:

                st.markdown(
                    f"### 🔴 {plant_id}"
                )

                st.caption(
                    f"🌱 {crop_name}   •   📍 {field_name}"
                )

            with top_right:

                st.error("Diseased")

            st.markdown(
                f"**🦠 Disease:** {disease}"
            )

            st.markdown(
                f"**📅 Last Scan:** {scan_date[:10]}"
            )

            if st.button(
                "👁 View Details",
                key=f"history_{crop_id}",
                use_container_width=True
            ):

                st.session_state.selected_history = {
                    "crop_id": crop_id,
                    "latest_scan": scan_date
                }

                st.switch_page(
                    "pages/my_crops.py"
                )
# =====================================================
# RECENT ACTIVITY
# =====================================================

st.divider()

st.subheader("🕒 Recent Activity")

response = requests.get(
    "https://cropcareai-v1.onrender.com/activity/"
)

result = response.json()

if result["success"]:
    activities = result["data"]
else:
    activities = []

if len(activities) == 0:

    st.info("No scans yet.")

else:

    for activity in activities:

        (
            crop_name,
            plant_id,
            disease,
            status,
            scan_date
        ) = activity

        left, right = st.columns([5, 1])

        with st.container(border=True):

            left, right = st.columns([5, 1])

            with left:

                icon = "🟢" if "Healthy" in status else "🔴"

                st.markdown(
                    f"### {icon} {plant_id}"
                )

                st.caption(
                    f"🌱 {crop_name}"
                )

                st.write(
                    f"🦠 **{disease}**"
                )

                st.write(
                    f"📅 {scan_date[:10]}"
                )

            with right:

                if "Healthy" in status:

                    st.success("Healthy")

                else:

                    st.error("Diseased")
# =====================================================
# ACTION BUTTONS
# =====================================================

st.divider()

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "📷 Scan Crop",
        use_container_width=True
    ):

        st.switch_page("pages/scan.py")

with col2:

    if st.button(
        "📂 My Crops",
        use_container_width=True
    ):

        st.switch_page("pages/my_crops.py")
