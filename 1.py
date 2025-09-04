import streamlit as st
from PIL import Image, ImageDraw
import pandas as pd
from func import split_image_into_blocks_with_grid, cernai

# Завантаження файлів
im = st.file_uploader(
    "Upload images", type=["bmp"]
)

# Відображення завантажених зображень
if im:
    # Відкриваємо зображення за допомогою PIL
    image = Image.open(im).convert("RGB")

    blocks, grid_img = split_image_into_blocks_with_grid(image, 6, 6)
    st.image(grid_img, caption="Сітка блоків", use_column_width=True)
    
    x = []
    for i in range(36):
        x.append(cernai(blocks[i]))

if st.button("Відобразити вектор ознак", type = "primary"):
    st.write(str(x))

st.button("Нормалізувати вектор охнак", type = "primary")
