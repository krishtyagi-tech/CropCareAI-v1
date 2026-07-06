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

from utils.database import save_scan
from datetime import datetime
import requests

# ==========================
# PAGE SETTINGS
# ==========================

# create_tables()
# ==========================
# BACK BUTTON
# ==========================

if st.button("⬅ Dashboard"):
    st.switch_page("app.py")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_uploaded_image" not in st.session_state:
    st.session_state.last_uploaded_image = None

if "selected_crop" not in st.session_state:
    st.session_state.selected_crop = None

st.title("🌿 CropCareAI")
selected_crop = st.session_state.get("selected_crop")

if selected_crop is None:

    st.error("Please select a crop from the Dashboard first.")

    st.stop()

st.success(
   f"🌱 Monitoring: {selected_crop['crop_name']} ({selected_crop['plant_id']})"
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
# ==========================
# PREDICTION
# ==========================

if uploaded_file is not None:

    # Load Image
    image = Image.open(uploaded_file).convert("RGB")

    # Create uploads folder
    os.makedirs("uploads", exist_ok=True)

    # Image path
   # Generate unique filename
    filename = (
        datetime.now().strftime("%Y%m%d_%H%M%S_")
        + uploaded_file.name
    )

    # Image path
    image_path = os.path.join(
        "uploads",
        filename
    )

    # Save image
    image.save(image_path)

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
    confidence = float(confidence)

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

    location = streamlit_geolocation()
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

    # Display previous messages
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_question = st.chat_input(
        "Ask anything about your crop..."
    )

    if user_question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_question
            }
        )

        with st.chat_message("user"):
            st.markdown(user_question)

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
    st.divider()

    st.subheader("💾 Save Scan")

    with st.form("save_scan_form"):

        st.write(f"**Crop:** {selected_crop['crop_name']}")
        st.write(f"**Plant ID:** {selected_crop['plant_id']}")

        submitted = st.form_submit_button("💾 Save Scan")

        if submitted:

            crop_id = selected_crop["id"]

            # Build chat history
            chat_history = ""

            for message in st.session_state.messages:
                chat_history += (
                    f"{message['role']}: "
                    f"{message['content']}\n"
                )

            # Weather values
            if weather:

                city = weather["city"]
                temperature = weather["temperature"]
                humidity = weather["humidity"]
                pressure = weather["pressure"]
                wind_speed = weather["wind_speed"]
                weather_desc = weather["description"]

            else:

                city = ""
                temperature = 0
                humidity = 0
                pressure = 0
                wind_speed = 0
                weather_desc = ""


            # <-- OUTSIDE the else block
            api_response = requests.post(
                "https://cropcareai-v1.onrender.com/scan/",
                json={
                    "crop_id": crop_id,
                    "image_path": image_path,
                    "disease": disease,
                    "status": status,
                    "confidence": confidence,
                    "city": city,
                    "temperature": temperature,
                    "humidity": humidity,
                    "pressure": pressure,
                    "wind_speed": wind_speed,
                    "weather": weather_desc,
                    "ai_chat": chat_history
                }
            )

            result = api_response.json()

            if not result["success"]:
                st.error(result["error"])

            st.success("✅ Scan saved successfully!")
            st.balloons() 