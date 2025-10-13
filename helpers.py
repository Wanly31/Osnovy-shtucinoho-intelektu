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


def hopfield_weights(X):
    """
    Обчислює матрицю коефіцієнтів ШНМ Хопфілда.
    w_ij = sum_k(x_i^k * x_j^k), якщо i ≠ j; 0, якщо i = j
    """
    X = np.array(X)
    m, n = X.shape
    W = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i != j:
                W[i, j] = np.sum(X[:, i] * X[:, j])
    return W

import numpy as np

def hopfield_classify(W, x_init, max_iter=100):
    # Формально: x(0) = x_init; змінюємо у циклі через sign та перевіряємо стабілізацію.
    x = np.array(x_init, dtype=int) 
    for it in range(max_iter):
        S = W @ x    # локальні суми
        x_new = np.where(S >= 0, 1, -1)
        if np.array_equal(x_new, x):
            return x_new, it + 1
        x = x_new
    return x, max_iter