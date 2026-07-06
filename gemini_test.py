import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("AQ.Ab8RN6L4AcyeBHILcqbI_DgKz70_ow9VugoD0XG9ISk7JCOlvQ"))

model = genai.GenerativeModel("gemini-2.5-flash")

response = model.generate_content(
    "Explain Tomato Early Blight in simple language."
)

print(response.text)