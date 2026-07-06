from dotenv import dotenv_values
from dotenv import load_dotenv
import os
import streamlit as st

print("dotenv_values:", dotenv_values(".env"))

load_dotenv(dotenv_path=".env", override=True)


print("Streamlit secret:", st.secrets["OPENWEATHER_API_KEY"])
print("os.environ:", os.environ.get("OPENWEATHER_API_KEY"))