import streamlit as st
from PIL import Image
import numpy as np
from helpers import split_image_into_blocks_with_grid, cernai, l2, im_upload

#Група 1
reference_images = st.file_uploader(
    "Еталонні образи 1", type=["bmp"], accept_multiple_files=True
)
mean_vector = None
if reference_images:
    
    all_vectors = im_upload(reference_images)

    if all_vectors:
        mean_vector = np.mean(all_vectors, axis=0)
        st.subheader("Середній вектор ознак (Група 1)")
        st.write(f"{mean_vector}")


#Група 2
reference_images2 = st.file_uploader(
    "Еталонні образи 2", type=["bmp"], accept_multiple_files=True
)
mean_vector2 = None
if reference_images2:

    all_vectors2 = im_upload(reference_images)

    if all_vectors2:
        mean_vector2 = np.mean(all_vectors2, axis=0)
        st.subheader("Середній вектор ознак (Група 2)")
        st.write(f"{mean_vector2}")


#Невідомий образ
unknown_image = st.file_uploader("Невідомий образ", type=["bmp"])
x_unknown_norm = None
if unknown_image:
    image = Image.open(unknown_image).convert("RGB").resize((600, 600))
    blocks, grid_img = split_image_into_blocks_with_grid(image, 6, 6)
    st.image(grid_img, caption="Невідомий образ", use_column_width=True)

    x_unknown = [cernai(block) for block in blocks]
    max_val = max(abs(val) for val in x_unknown) or 1
    x_unknown_norm = [abs(val)/max_val for val in x_unknown]


#Порівняння
if mean_vector is not None and mean_vector2 is not None and x_unknown_norm is not None:
    st.subheader("Міри відповідності")
    dist1 = l2(mean_vector, x_unknown_norm)
    dist2 = l2(mean_vector2, x_unknown_norm)

    st.write(f"Відстань до групи 1: {dist1:.4f}")
    st.write(f"Відстань до групи 2: {dist2:.4f}")

    if dist1 < dist2:
        st.success("Невідомий образ ближче до ГРУПИ 1")
    else:
        st.success("Невідомий образ ближче до ГРУПИ 2")
