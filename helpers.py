import streamlit as st
from PIL import Image, ImageDraw
import numpy as np


def split_image_into_blocks_with_grid(image: Image.Image, grid_x: int, grid_y: int):

    width, height = image.size
    block_w = width // grid_x
    block_h = height // grid_y

    cropped_images = []

    grid_image = image.copy()
    draw = ImageDraw.Draw(grid_image)

    # вертик лінії

    for i in range(1, grid_x):
        x = i * block_w
        draw.line([(x, 0), (x, height)], fill="black", width=1)
    # горизонт лінії

    for j in range(1, grid_y):
        y = j * block_h
        draw.line([(0, y), (width, y)], fill="black", width=1)
    # Обрізаємо блоки і додаємо в масив

    for j in range(grid_y):
        for i in range(grid_x):
            left = i * block_w
            top = j * block_h
            right = (i + 1) * block_w
            bottom = (j + 1) * block_h

            cropped = image.crop((left, top, right, bottom))
            cropped_images.append(cropped)
    return cropped_images, grid_image

def cernai(image: Image.Image):

    black_pixel_count = 0
    width, height = image.size
    pixels = image.load()

    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            if r == 0 and g == 0 and b == 0:
                black_pixel_count += 1
    return black_pixel_count

def im_upload(reference_images):
    # Масив для додавання всіх векторів

    all_vectors = []

    cols = st.columns(len(reference_images))
    for i, (col, img_file) in enumerate(zip(cols, reference_images)):
        with col:
            image = Image.open(img_file).convert("RGB").resize((600, 600))
            blocks, grid_img = split_image_into_blocks_with_grid(image, 6, 6)
            st.image(grid_img, caption=f"Еталон 1.{i+1}", width="stretch")

            x = [cernai(block) for block in blocks]
            max_val = max(abs(val) for val in x) or 1
            x_norm = [abs(val) / max_val for val in x]


            #Бінаризація
            # Бінаризація через поріг 0.5
            x_bin = [1 if val >= 0.5 else -1 for val in x_norm]

            #Середнє
            #threshold = sum(x_norm) / len(x_norm)
            #x_bin = [1 if val >= threshold else -1 for val in x_norm]

            #if st.button(f"Відобразити вектор ознак {i+1}", key=f"show_{i}"):
                #st.write(f"Абсолютні ознаки: {x_bin}")
                
            all_vectors.append(x_bin)
    return all_vectors


def init_hamming_weights(reference_patterns):
    """
    Ініціалізує ваги і пороги для першого шару Хеммінга.
    reference_patterns: список еталонних векторів (розмір m × n)
    """
    patterns = np.array(reference_patterns)  # m × n
    m, n = patterns.shape
    W1 = patterns.T / 2            # n × m
    B1 = np.full(m, n / 2)         # пороги, m-розмірність
    return W1, B1

def hamming_first_layer(x, W1, B1):
    """
    x: вхідний бінарний вектор (n,)
    W1: ваги першого шару (n × m)
    B1: пороги першого шару (m,)
    """
    s1 = W1.T @ x + B1  # результати першого шару (m,)
    y1 = np.maximum(s1, 0)  # ReLU або max(0, s) для стійкості
    return y1

def init_second_layer(y1):
    """
    y1: результати першого шару (m,)
    """
    return y1.copy()  # ініціалізація другого шару

def update_hamming_second_layer(y2, epsilon):
    """
    y2: поточні виходи другого шару (m,)
    epsilon: вага гальмуючих синапсів (0 < epsilon < 1/m)
    """
    m = len(y2)
    new_y2 = np.zeros_like(y2)
    for j in range(m):
        inhibition = np.sum(y2) - y2[j]
        s2 = y2[j] - epsilon * inhibition
        new_y2[j] = max(s2, 0)  # порогова функція (max(0, s2))
    return new_y2

def stabilize_hamming_second_layer(y2, epsilon, max_iter=100):
    """
    y2: ініціалізований другий шар (m,)
    epsilon: вага гальмуючих синапсів
    """
    for it in range(max_iter):
        new_y2 = update_hamming_second_layer(y2, epsilon)
        if np.allclose(new_y2, y2, atol=1e-6):
            return new_y2, it + 1
        y2 = new_y2
    return y2, max_iter
