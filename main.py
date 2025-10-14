import streamlit as st
from PIL import Image
import numpy as np

from helpers import (
    split_image_into_blocks_with_grid,
    cernai,
    im_upload,
    perceptron_train,
    perceptron_predict,
)

X = []
y = []

# Група 1

reference_images = st.file_uploader(
    "Еталонні образи 1", type=["bmp"], accept_multiple_files=True
)
mean_vector = None
if reference_images:

    all_vectors = im_upload(reference_images)

    for v in all_vectors:
        X.append(v)
        y.append(1)
# Група 2

reference_images2 = st.file_uploader(
    "Еталонні образи 2", type=["bmp"], accept_multiple_files=True
)
mean_vector2 = None

if reference_images2:

    all_vectors2 = im_upload(reference_images2)

    for v in all_vectors2:
        X.append(v)
        y.append(-1)
w = None
if len(X) > 0 and len(y) > 0:
    X_np = np.array(X)
    y_np = np.array(y)
    w = perceptron_train(X_np, y_np, lr=0.1, max_epochs=200)
    st.success("Перцептрон навчено!")
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

    pred = perceptron_predict(w, x_unknown_norm)
    if pred == 1:
        st.success("Невідомий образ належить до ГРУПИ 1")
    else:
        st.success("Невідомий образ належить до ГРУПИ 2")
