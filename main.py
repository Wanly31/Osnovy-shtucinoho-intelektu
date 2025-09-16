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
        image = Image.open(img_file).convert("RGB")
        
        blocks, grid_img = split_image_into_blocks_with_grid(image, 6, 6)
        col.image(grid_img, caption="Сітка блоків", use_column_width=True)

        # Обчислення ознак
        x = [cernai(block) for block in blocks]

        # Нормалізація
        max_val = max(abs(val) for val in x)
        x_normalized = [abs(val)/max_val for val in x]

        # Виведення ознак
        col.write(f"Абсолютні ознаки: {x}")
        col.write(f"Нормовані ознаки: {x_normalized}")



    #blocks, grid_img = split_image_into_blocks_with_grid(image, 6, 6)
    #st.image(grid_img, caption="Сітка блоків", use_column_width=True)
    
    #x = []
    #for i in range(36):
     #   x.append(cernai(blocks[i]))

    # Беремо абсолютні значення та знаходимо максимум
    #max_val = max(abs(val) for val in x)

    # Нормалізуємо вектор
    #x_normalized = [abs(val)/max_val for val in x]

if st.button("Відобразити вектор ознак", type = "primary"):
    st.write(str(x))

if st.button("Нормалізувати вектор ознак", type = "primary"):
    st.write("Нормалізований вектор:", str(x_normalized))
