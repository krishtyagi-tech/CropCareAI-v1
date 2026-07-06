import streamlit as st
import tensorflow as tf
import numpy as np
import pickle
import os
from dotenv import load_dotenv
from google import genai
from PIL import Image
from utils.weather import get_weather
from streamlit_geolocation import streamlit_geolocation
from utils.database import (
    create_tables,
    add_crop,
    get_crops
)

# ==========================
# PAGE SETTINGS
# ==========================

st.set_page_config(
    page_title="CropCareAI",
    page_icon="🌿",
    layout="wide"
)
create_tables()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_uploaded_image" not in st.session_state:
    st.session_state.last_uploaded_image = None

if "selected_crop" not in st.session_state:
    st.session_state.selected_crop = None

st.title("🌿 CropCareAI")
with st.sidebar:

    st.header("🌱 Crop Management")

    st.subheader("Add New Crop")

    crop_name = st.text_input("Crop Name")

    plant_id = st.text_input("Plant ID")

    field_name = st.text_input("Field Name")

    planting_date = st.date_input("Planting Date")

    if st.button("Save Crop"):

        if crop_name and plant_id:

            try:

                add_crop(
                    crop_name,
                    plant_id,
                    field_name,
                    str(planting_date)
                )

                st.success("✅ Crop Added Successfully!")

            except Exception:

                st.error("❌ Plant ID already exists.")

    st.divider()

    st.subheader("Registered Crops")

    crops = get_crops()

    for crop in crops:

        if st.button(
            f"🌱 {crop[2]} ({crop[1]})",
            key=f"crop_{crop[0]}"
    ):
            st.session_state.selected_crop = crop
st.write("AI Powered Crop Disease Detection")
if st.session_state.selected_crop:

    st.success(
        f"🌱 Selected Crop: {st.session_state.selected_crop[2]} ({st.session_state.selected_crop[1]})"
    )
# ==========================
# LOAD MODEL
# ==========================

model = tf.keras.models.load_model("model/cropcare_model.keras")

with open("model/labels.pkl", "rb") as f:
    labels = pickle.load(f)

class_names = list(labels.keys())

# ==========================
# GEMINI SETUP
# ==========================

load_dotenv()

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

# ==========================
# IMAGE UPLOAD
# ==========================

uploaded_file = st.file_uploader(
    "Upload a Leaf Image",
    type=["jpg", "jpeg", "png"]
)
# Reset chat when a new image is uploaded

if uploaded_file is not None:

    current_image = uploaded_file.name

    if "last_uploaded_image" not in st.session_state:
        st.session_state.last_uploaded_image = current_image

    elif st.session_state.last_uploaded_image != current_image:

        st.session_state.messages = []

        st.session_state.last_uploaded_image = current_image

# city = st.text_input(
#     "📍 Enter Your City",
#     placeholder="e.g. Ghaziabad"
# )
location = streamlit_geolocation()
# ==========================
# PREDICTION
# ==========================

if uploaded_file is not None:

    # Load Image
    image = Image.open(uploaded_file).convert("RGB")

    # Display Uploaded Image
    st.success("Prediction Completed Successfully ✅")

    left, right = st.columns([1, 2])

    with left:
        st.image(
            image,
            caption="Uploaded Leaf",
            use_container_width=True
        )

    # ==========================
    # IMAGE PREPROCESSING
    # ==========================

    img = image.resize((224, 224))
    img = np.array(img)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    # ==========================
    # PREDICTION
    # ==========================

    prediction = model.predict(img)

    predicted_index = np.argmax(prediction)

    confidence = prediction[0][predicted_index] * 100

    predicted_class = class_names[predicted_index]

    crop, disease = predicted_class.split("_", 1)

    disease = disease.replace("_", " ")

    status = "🟢 Healthy" if "healthy" in disease.lower() else "🔴 Diseased"

    # ==========================
    # PREDICTION SUMMARY
    # ==========================

    with right:

        st.subheader("🌱 Prediction Summary")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("🌱 Crop", crop)
            st.metric("📌 Status", status)

        with col2:
            st.metric("📊 Confidence", f"{confidence:.2f}%")

        st.markdown("### 🦠 Predicted Disease")

        st.info(disease)
    # ==========================
# WEATHER
# ==========================

weather = None

# # if city:

# #     weather = get_weather_by_city(city)

#     if weather:

#         st.divider()
#         st.subheader("🌦 Live Weather")

#         c1, c2, c3, c4 = st.columns(4)

#         with c1:
#             st.metric(
#                 "🌡 Temperature",
#                 f"{weather['temperature']} °C"
#             )

#         with c2:
#             st.metric(
#                 "💧 Humidity",
#                 f"{weather['humidity']} %"
#             )

#         with c3:
#             st.metric(
#                 "🌬 Wind",
#                 f"{weather['wind_speed']} m/s"
#             )

#         with c4:
#             st.metric(
#                 "☁ Weather",
#                 weather["description"].title()
#             )

#         st.caption(f"📍 {weather['city']}")

#     else:
#         st.error("Unable to fetch weather. Please check the city name.")
weather = None

if location:

    latitude = location["latitude"]
    longitude = location["longitude"]

    weather = get_weather(latitude, longitude)

    if weather:

        st.divider()

        st.subheader("🌦 Live Weather")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "🌡 Temperature",
                f"{weather['temperature']} °C"
            )

        with c2:
            st.metric(
                "💧 Humidity",
                f"{weather['humidity']} %"
            )

        with c3:
            st.metric(
                "🌬 Wind",
                f"{weather['wind_speed']} m/s"
            )

        with c4:
            st.metric(
                "☁ Weather",
                weather["description"].title()
            )

        st.caption(f"📍 {weather['city']}")

    else:

        st.warning("Unable to fetch weather.")

# ==========================
# CropCareAI Assistant
# ==========================

st.divider()

st.subheader("🤖 CropCareAI Assistant")

st.caption(
    "Ask questions about the detected disease, weather, treatment, or prevention."
)

# Show previous conversation
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_question = st.chat_input(
    "Ask anything about your crop..."
)

if user_question:

    # Show user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    with st.chat_message("user"):
        st.markdown(user_question)

    # Weather text (safe even if no city entered)
    if weather:

        weather_text = f"""
Temperature: {weather['temperature']}°C
Humidity: {weather['humidity']}%
Weather: {weather['description']}
"""

    else:

        weather_text = "Weather information not available."

    prompt = f"""
You are CropCareAI, an intelligent agricultural assistant.

Current Crop:
{crop}

Current Disease:
{disease}

Confidence:
{confidence:.2f}%

{weather_text}

The user already knows the prediction.
Answer ONLY the user's question.

User Question:
{user_question}
"""

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            answer = response.text

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )