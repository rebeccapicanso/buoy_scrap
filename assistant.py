import colorsys
from PIL import Image
import numpy as np

def prep(full_image_path):
    image = Image.open(full_image_path)
    width, height = image.size
    image = image.crop((0, 0, width, height - height // 10))
    width, height = image.size
    part_width = width // 6
    images = []
    for i in range(6):
        part = image.crop((i * part_width, 0, (i + 1) * part_width, height))
        images.append(part)
    return images

def prioritize_colors(colors, criteria):
    def calculate_score(color):
        r, g, b = [x/255.0 for x in color]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        brightness_score = v * criteria.get('brightness', 0)
        saturation_score = s * criteria.get('saturation', 0)
        hue_preference = abs(1 - h) if h > 0.5 else h
        hue_score = hue_preference * criteria.get('hue_preference', 0)
        return brightness_score + saturation_score + hue_score
    return sorted(colors, key=calculate_score, reverse=True)

def analyze_image(image_path):
    with Image.open(image_path) as img:
        img = img.convert('RGB')
        img_array = np.array(img)
        avg_color = np.mean(img_array, axis=(0, 1))
        brightness = np.mean(avg_color)
        is_night = brightness < 50
        contains_moon = False
        gray_img = np.mean(img_array, axis=2)
        bright_spots = np.where(gray_img > 200)
        if len(bright_spots[0]) > 0:
            y_coords, x_coords = bright_spots
            center_y, center_x = np.mean(y_coords), np.mean(x_coords)
            distances = np.sqrt((y_coords - center_y)**2 + (x_coords - center_x)**2)
            if np.std(distances) < 20:
                contains_moon = True
    return contains_moon, is_night

def get_dominant_color(image):
    img = Image.open(image)
    img = img.resize((64, 64))
    img_array = np.array(img)
    return np.argmax(np.mean(img_array, axis=(0, 1)))

def preprocess_image(image_path):
    img = Image.open(image_path)
    img = img.resize((64, 64))
    return np.array(img) / 255.0