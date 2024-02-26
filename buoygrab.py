import os.path
from bs4 import BeautifulSoup as bs
import requests
import os, time
import cv2
import numpy as np
from PIL import Image
from random import randrange


# this is tracking a single buoy off the coast of the Aleutian Islands!
# can be expanded to include all 54 buoys, but not recommended unless you are uploading images to
# google cloud storage or something similar.

# set timezone for Aleutian
os.environ['TZ'] = 'US/Aleutian'
time.tzset()

# get yesterday's date
yesterday = time.strftime("%d", time.gmtime(time.time() - 86400))

# create an hour variable
hours = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16',
          '17', '18', '19', '20', '21', '22', '23']

# create a loop to grab images for each hour

count = 0

for x in hours:
    count =+ 1
    dynamic_url_Z64A = 'https://www.ndbc.noaa.gov/images/buoycam/Z64A_2024_02_' + yesterday + '_' + x + '10.jpg'
    img_data_Z64A = requests.get(dynamic_url_Z64A).content

    # read image and asssess HSV value
    jpg_name_Z64A = 'Z64A_2024_02_' + yesterday + '_' + x + '10.jpg'
    img = cv2.imread(jpg_name_Z64A)

    with open(jpg_name_Z64A, 'wb') as handler:
        handler.write(img_data_Z64A)

    # crop random square from image
    img = Image.open(jpg_name_Z64A)
    x, y = img.size

    matrix = 250
    sample = 10
    sample_list = []

    for i in range(sample):
        x1 = randrange(0, x - matrix)
        y1 = randrange(0, y - matrix)
        sample_list.append(img.crop((x1, y1, x1 + matrix, y1 + matrix)))
    
    # save cropped images
    for i in range(sample):
        sample_list[i].save('still' + str(i) + '.jpg')

