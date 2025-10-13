import streamlit as st
from PIL import Image
import numpy as np
from helpers import (
    split_image_into_blocks_with_grid,
    cernai,
    im_upload,
    hopfield_weights,
    hopfield_classify
)

# Група 1

reference_images = st.file_uploader(
    "Еталонні образи 1", type=["bmp"], accept_multiple_files=True
)
if reference_images:

    all_vectors = im_upload(reference_images)
    W1 = hopfield_weights(all_vectors)
    if st.button("Відобразити матрицю коефіцієнтів Хопфілда (Група 1):"):
        st.write("Матриця коефіцієнтів Хопфілда (Група 1):")
        st.dataframe(W1)


# Група 2

reference_images2 = st.file_uploader(
    "Еталонні образи 2", type=["bmp"], accept_multiple_files=True
)
if reference_images2:

    all_vectors2 = im_upload(reference_images2)
    W2 = hopfield_weights(all_vectors2)
    if st.button("Відобразити матрицю коефіцієнтів Хопфілда (Група 2):"):
        st.write("Матриця коефіцієнтів Хопфілда (Група 2):")
        st.dataframe(W2)



# Невідомий образ

unknown_image = st.file_uploader("Невідомий образ", type=["bmp"])
x_unknown_norm = None
if unknown_image:
    image = Image.open(unknown_image).convert("RGB").resize((600, 600))
    blocks, grid_img = split_image_into_blocks_with_grid(image, 6, 6)
    st.image(grid_img, caption="Невідомий образ", width = 'stretch')

    x_unknown = [cernai(block) for block in blocks]
    max_val = max(abs(val) for val in x_unknown) or 1
    x_unknown_norm = [abs(val) / max_val for val in x_unknown]

    #бінаризація
    #threshold = sum(x_unknown_norm) / len(x_unknown_norm)і
    #x_unknown_bin = [1 if val >= threshold else -1 for val in x_unknown_norm]

    x_unknown_bin = [1 if val >= 0.5 else -1 for val in x_unknown_norm]

    if reference_images and reference_images2:
        x_arr = np.array(x_unknown_bin)
        x1_final, iter1 = hopfield_classify(W1, x_arr)
        x2_final, iter2 = hopfield_classify(W2, x_arr)
        E1 = -0.5 * x1_final @ W1 @ x1_final.T
        E2 = -0.5 * x2_final @ W2 @ x2_final.T
        st.write(f"🔹 Клас 1: E = {E1:.3f}, ітерацій: {iter1}")
        st.write(f"🔹 Клас 2: E = {E2:.3f}, ітерацій: {iter2}")
        min_E = min(E1, E2)
        if min_E == E1:
            st.success("Невідомий образ класифіковано як Клас 1")
        elif min_E == E2:
            st.success("Невідомий образ класифіковано як Клас 2")
        else:
            st.warning("Результат неоднозначний — енергії рівні.")