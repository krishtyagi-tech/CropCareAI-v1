import tensorflow as tf
import numpy as np
import pickle
from PIL import Image

# ===========================
# LOAD MODEL
# ===========================

model = tf.keras.models.load_model("model/cropcare_model.keras")

print("✅ Model Loaded Successfully")

# ===========================
# LOAD LABELS
# ===========================

with open("model/labels.pkl", "rb") as f:
    labels = pickle.load(f)

# Convert label dictionary into list
class_names = list(labels.keys())

# ===========================
# IMAGE PATH
# ===========================

IMAGE_PATH = "test.jpg"   # Change this to your image name

# ===========================
# LOAD IMAGE
# ===========================

image = Image.open(IMAGE_PATH).convert("RGB")

image = image.resize((224, 224))

img = np.array(image)

img = img / 255.0

img = np.expand_dims(img, axis=0)

print("✅ Image Loaded Successfully")

# ===========================
# PREDICT
# ===========================

prediction = model.predict(img)

top5 = np.argsort(prediction[0])[::-1][:5]

print("\nTop 5 Predictions\n")

for i in top5:
    print(f"{class_names[i]} : {prediction[0][i]*100:.2f}%")