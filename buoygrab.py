import os.path
from bs4 import BeautifulSoup as bs
import requests
import os, time
from datetime import datetime, timedelta
import cv2
import numpy as np
from PIL import Image
from random import randrange
from collections import defaultdict

import logging


cams = ['Z98A','W17A']

# read kml and dump into json

# go to root directory that isn't
try:
    os.chdir('/Users/rebeccapicanco/code')
except OSError as e:
    print(f"Failed to change directory: {e}")

jpg_images = []

def setup():
    os.environ['TZ'] = 'US/Aleutian'
    time.tzset()

    yesterday = datetime.now() - timedelta(days=1)
    month = yesterday.strftime("%m")
    day = yesterday.strftime("%d")
    year = yesterday.strftime("%Y")
    
    hours = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16',
             '17', '18', '19', '20', '21', '22', '23']
    count = 0


    for camera in cams:
        for x in hours:
            try:

                dynamic_url_Z64A = f'https://www.ndbc.noaa.gov/images/buoycam/{camera}_{year}_{month}_{day}_{x}10.jpg'
                # if dir doesn't exist
                if not os.path.exists(f'buoy_tmp/{camera}/{year}/{month}/{day}'):
                    os.makedirs(f'buoy_tmp/{camera}/{year}/{month}/{day}', exist_ok=True)
                camera_path_temp = f'buoy_tmp/{camera}/{year}/{month}/{day}/{camera}_{year}_{month}_{day}_{x}11.jpg'
                
                if not os.path.exists(camera_path_temp):
                    img_data = requests.get(dynamic_url_Z64A)
                    
                    if img_data.status_code == 200:  # Check if download was successful
                        with open(camera_path_temp, 'wb') as handler:
                            handler.write(img_data.content)
                        count += 1
                        jpg_images.append(camera_path_temp)
                        print(f"Downloaded: {camera_path_temp}")
                    else:
                        print(f"Failed to download {dynamic_url_Z64A}: Status code {img_data.status_code}")
                        
            except Exception as e:
                print(f"Error downloading image for hour {x}: {e}")
                
        print(f"Downloaded {count} new images for {year}-{month}-{day}")

import os
from PIL import Image
import pandas as pd

class ImageDataset:
    def __init__(self, data_dir, labels_df):
        self.data_dir = data_dir
        self.labels_df = labels_df
    
    def __getitem__(self, idx):
        # Get image path and label from dataframe
        row = self.labels_df.iloc[idx]
        img_path = os.path.join(self.data_dir, row['image_filename'])
        label = row['label']
        
        # Load and preprocess image
        image = Image.open(img_path).convert('RGB')
        # Add your preprocessing here (resize, normalize, etc.)
        
        return image, label

# def sort_images_by_color(jpg_name):
#     try:
#         img = Image.open(jpg_name)
#         x, y = img.size
#         matrix = 250
#         sample = 10
#         sample_list = []
        
#         for i in range(sample):
#             x1 = randrange(0, x - matrix)
#             y1 = randrange(0, y - matrix)
#             cropped = img.crop((x1, y1, x1 + matrix, y1 + matrix))
#             sample_list.append((cropped, get_dominant_color(cropped)))
            
#         sample_list.sort(key=lambda x: sum(x[1]))
        
#         output_dir = 'sorted_images'
#         os.makedirs(output_dir, exist_ok=True)
        
#         for i, (cropped_img, color) in enumerate(sample_list):
#             output_path = os.path.join(output_dir, f'sorted_still_{i}_color_{color}.jpg')
#             cropped_img.save(output_path)
            
#         print(f"Sorted {sample} images by color from {jpg_name}")
        
#     except Exception as e:
#         print(f"Error processing {jpg_name}: {e}")

# # working on this, maybe not needed?
# def get_dominant_color(image):
#     width, height = image.size
#     pixels = image.getcolors(width * height)
#     color_counts = defaultdict(int)
    
#     for count, color in pixels:
#         if isinstance(color, tuple):
#             color = color[:3]
#         color_counts[color] += count
        
#     dominant_color = max(color_counts, key=color_counts.get)
#     return dominant_color

if __name__ == "__main__":
    print("Starting buoy image download...")
    setup()

    for image in jpg_images:
        sort_images_by_color(image)


# they are guessing one in an array

# if number is not in array
# add number to a