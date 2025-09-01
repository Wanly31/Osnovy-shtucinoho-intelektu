import streamlit as st
from PIL import Image

# Завантаження файлів
uploaded_files = st.file_uploader(
    "Upload images", type=["bmp"]
)

# Відображення завантажених зображень
if uploaded_files:
    # Відкриваємо зображення за допомогою PIL
    image = Image.open(uploaded_files)
    image = image.resize((600,600))
    st.image(image, caption=uploaded_files.name)

st.button("Відобразити вектор ознак", type = "primary")

st.button("Нормалізувати вектор охнак", type = "primary")
