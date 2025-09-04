import streamlit as st
from PIL import Image, ImageDraw

def split_image_into_blocks_with_grid(image: Image.Image, grid_x: int, grid_y: int):

    width, height = image.size
    block_w = width // grid_x
    block_h = height // grid_y

    cropped_images = []

    # Створюємо копію для малювання сітки
    grid_image = image.copy()
    draw = ImageDraw.Draw(grid_image)

    # Малюємо вертикальні лінії
    for i in range(1, grid_x):
        x = i * block_w
        draw.line([(x, 0), (x, height)], fill="black", width=1)

    # Малюємо горизонтальні лінії
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
            # Получаем значение цвета пикселя по координатам (R, G, B)
            r, g, b = pixels[x, y]
            # Черный цвет имеет значения R=0, G=0, B=0
            if r == 0 and g == 0 and b == 0:
                black_pixel_count += 1

    return black_pixel_count