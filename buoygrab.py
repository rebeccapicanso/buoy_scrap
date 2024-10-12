import os.path
from bs4 import BeautifulSoup as bs
import requests
import os, time
import cv2
import numpy as np
from PIL import Image
from random import randrange
from collections import defaultdict
# test

jpg_images_store = []

def setup():
    os.environ['TZ'] = 'US/Aleutian'
    time.tzset()
    yesterday = time.strftime("%d", time.gmtime(time.time() - 86400))
    hours = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16',
            '17', '18', '19', '20', '21', '22', '23']

    days = 3

    count = 0

    for x in hours:
        count =+ 1
        dynamic_url_Z64A = 'https://www.ndbc.noaa.gov/images/buoycam/Z64A_2024_10_' + yesterday + '_' + x + '10.jpg'
        img_data_Z64A = requests.get(dynamic_url_Z64A).content

        jpg_name_Z64A = 'Z64A_2024_02_' + yesterday + '_' + x + '10.jpg'
        img = cv2.imread(jpg_name_Z64A)
        jpg_images.append(jpg_name_Z64A)

        with open(jpg_name_Z64A, 'wb') as handler:
            handler.write(img_data_Z64A)
        
    print(f"Downloaded {count} images.")


def sort_images_by_color(jpg_name):
    img = Image.open(jpg_name)
    x, y = img.size
    matrix = 250
    sample = 10
    sample_list = []

    for i in range(sample):
        x1 = randrange(0, x - matrix)
        y1 = randrange(0, y - matrix)
        cropped = img.crop((x1, y1, x1 + matrix, y1 + matrix))
        sample_list.append((cropped, get_dominant_color(cropped)))

    sample_list.sort(key=lambda x: sum(x[1]))

    for i, (cropped_img, color) in enumerate(sample_list):
        cropped_img.save(f'sorted_still_{i}_color_{color}.jpg')

    print(f"Sorted {sample} images by color.")

def get_dominant_color(image):
    width, height = image.size
    pixels = image.getcolors(width * height)
    
    color_counts = defaultdict(int)
    for count, color in pixels:
        if isinstance(color, tuple): 
            color = color[:3]  # Convert RGBA to RGB if necessary
        color_counts[color] += count
    
    dominant_color = max(color_counts, key=color_counts.get)
    return dominant_color

setup()

