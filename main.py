import streamlit as st
from PIL import Image, ImageDraw
import pandas as pd
from func import split_image_into_blocks_with_grid, cernai

im = st.file_uploader(
    "Upload images", type=["bmp"], accept_multiple_files = True
)

if im:
    cols = st.columns(len(im))

    for i, (col, img_file) in enumerate(zip(cols, im)):
        with col:  # Все всередині цієї колонки
            image = Image.open(img_file).convert("RGB")
            blocks, grid_img = split_image_into_blocks_with_grid(image, 6, 6)
            st.image(grid_img, caption="Сітка блоків", use_column_width=True)

            # Обчислення ознак
            x = [cernai(block) for block in blocks]
            max_val = max(abs(val) for val in x)
            x_normalized = [abs(val)/max_val for val in x]

            # Кнопки під зображенням
            if st.button(f"Відобразити вектор ознак {i+1}", key=f"show_{i}"):
                st.write(f"Абсолютні ознаки: {x}")

            if st.button(f"Нормалізувати ознаки {i+1}", key=f"norm_{i}"):
                st.write(f"Нормовані ознаки: {x_normalized}")
