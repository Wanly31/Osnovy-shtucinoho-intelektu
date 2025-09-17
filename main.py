import streamlit as st
from PIL import Image, ImageDraw
import pandas as pd
from func import split_image_into_blocks_with_grid, cernai, l2

reference_images = st.file_uploader(
    "Еталонні образи", type=["bmp"], accept_multiple_files = True
)
reference_features = {}

if reference_images:
    cols = st.columns(len(reference_images))
    for i, (col, img_file) in enumerate(zip(cols, reference_images)):
        with col:
            image = Image.open(img_file).convert("RGB")
            image = image.resize((600, 600))
            blocks, grid_img = split_image_into_blocks_with_grid(image, 6, 6)
            st.image(grid_img, caption=f"Еталон {i+1}", use_column_width=True)

            x = [cernai(block) for block in blocks]
            max_val = max(abs(val) for val in x)
            x_norm = [abs(val)/max_val for val in x]

            reference_features[img_file.name] = {
                "raw": x,
                "norm": x_norm
            }

            if st.button(f"Відобразити вектор ознак {i+1}", key=f"show_{i}"):
                st.write(f"Абсолютні ознаки: {x}")

            if st.button(f"Нормалізувати ознаки {i+1}", key=f"norm_{i}"):
                st.write(f"Нормовані ознаки: {x_norm}")


unknown_image = st.file_uploader(
    "Невідомий образ", type=["bmp"]
)

if unknown_image:
    image = Image.open(unknown_image).convert("RGB")
    image = image.resize((600, 600))
    blocks, grid_img = split_image_into_blocks_with_grid(image, 6, 6)
    st.image(grid_img, caption="Невідомий образ", use_column_width=True)

    x_unknown = [cernai(block) for block in blocks]
    max_val = max(abs(val) for val in x_unknown)
    x_unknown_norm = [abs(val)/max_val for val in x_unknown]


    if st.button(f"Відобразити вектор ознак"):
                st.write(f"Абсолютні ознаки: {x_unknown}")
    if st.button(f"Нормалізувати ознаки"):
                st.write(f"Нормовані ознаки: {x_unknown_norm}")

if reference_features and unknown_image:
    st.subheader("Міри відповідності (L2-норма):")
    distances = {}

    # проходимо по всіх еталонних образах
    for name, feats in reference_features.items():
        dist = l2(feats["norm"], x_unknown_norm)
        distances[name] = dist
        st.write(f"{name}: {dist:.4f}")

    # знаходимо найближчу групу
    closest_name = min(distances, key=distances.get)
    st.success(f"Невідомий образ найбільш схожий на групу: **{closest_name}**")
