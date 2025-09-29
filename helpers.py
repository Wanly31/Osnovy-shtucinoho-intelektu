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

    #вертик лінії
    for i in range(1, grid_x):
        x = i * block_w
        draw.line([(x, 0), (x, height)], fill="black", width=1)

    #горизонт лінії
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

def l2(v1, v2):
    return np.max(np.abs(np.array(v1) - np.array(v2)))

def im_upload(reference_images):
    #Масив для додавання всіх векторів
    all_vectors = []
    
    cols = st.columns(len(reference_images))
    for i, (col, img_file) in enumerate(zip(cols, reference_images)):
        with col:
            image = Image.open(img_file).convert("RGB").resize((600, 600))
            blocks, grid_img = split_image_into_blocks_with_grid(image, 6, 6)
            st.image(grid_img, caption=f"Еталон 1.{i+1}", use_column_width=True)

            x = [cernai(block) for block in blocks]
            max_val = max(abs(val) for val in x) or 1
            x_norm = [abs(val)/max_val for val in x]

            all_vectors.append(x_norm)

    return all_vectors
