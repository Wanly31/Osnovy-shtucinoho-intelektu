import streamlit as st
from PIL import Image
import numpy as np
from helpers import (
    split_image_into_blocks_with_grid,
    cernai,
    im_upload,
    init_hamming_weights,
    hamming_first_layer,
    init_second_layer,
    stabilize_hamming_second_layer,
    hamming_classify
)

patterns, labels = [], []
# Група 1

reference_images = st.file_uploader(
    "Еталонні образи 1", type=["bmp"], accept_multiple_files=True
)
if reference_images:
    all_vectors1 = im_upload(reference_images)
    for vec in all_vectors1:
        patterns.append(vec)
        labels.append(1)




# Група 2

reference_images2 = st.file_uploader(
    "Еталонні образи 2", type=["bmp"], accept_multiple_files=True
)
if reference_images2:
    all_vectors2 = im_upload(reference_images2)
    for vec in all_vectors2:
        patterns.append(vec)
        labels.append(2)




# Невідомий образ
if patterns:
    st.success(f"Завантажено {len(patterns)} еталонів для класифікації.")

# Класифікуємо невідомий образ
unknown_image = st.file_uploader("Невідомий образ", type=["bmp"])
if unknown_image and patterns:
    image = Image.open(unknown_image).convert("RGB").resize((600, 600))
    blocks, grid_img = split_image_into_blocks_with_grid(image, 6, 6)
    st.image(grid_img, caption="Невідомий образ", width='stretch')

    x_unknown = [cernai(block) for block in blocks]
    max_val = max(abs(val) for val in x_unknown) or 1
    x_unknown_norm = [abs(val) / max_val for val in x_unknown]
    x_unknown_bin = [1 if val >= 0.5 else 0 for val in x_unknown_norm]  # Для Хеммінга (0/1)

    # 1. Ініціалізація ваг
    W1, B1 = init_hamming_weights(patterns)
    # 2. Перший шар
    y1 = hamming_first_layer(x_unknown_bin, W1, B1)
    # 3. Другий шар - ініціалізація
    y2 = init_second_layer(y1)
    # 4. Стабілізація
    epsilon = 0.9 / len(patterns)
    y2_final, iterations = stabilize_hamming_second_layer(y2, epsilon)

    winner_idx = np.argmax(y2_final)
    predicted_class = labels[winner_idx]

    st.write(f"Клас результату: {predicted_class} (індекс: {winner_idx+1}) на {iterations} ітерації.")
    st.write(f"Вихід другого шару: {y2_final}")

else:
    st.info("Завантажте еталонні образи, а потім невідомий для класифікації.")