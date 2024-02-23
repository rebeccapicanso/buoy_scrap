import os.path
from bs4 import BeautifulSoup as bs
import requests
import os, time

# url = 'https://www.ndbc.noaa.gov/images/buoycam/Z32A_2023_10_27_0210.jpg'
# page = requests.get(url)

# set timezone for Aleutian
os.environ['TZ'] = 'US/Aleutian'
time.tzset()
day = time.strftime("%d")

# grab image from webpage
dynamic_url_Z64A = 'https://www.ndbc.noaa.gov/images/buoycam/Z64A_2024_01_' + day + '_2010.jpg'
img_data_Z64A = requests.get(dynamic_url_Z64A).content
jpg_name_Z64A = 'Z64A_2024_01_' + day + '_2010.jpg'

with open(jpg_name_Z64A, 'wb') as handler:
    handler.write(img_data_Z64A)

##### CHECK HUE VALUE #####

import cv2
import numpy as np

# read image
img = cv2.imread(jpg_name_Z64A)

# convert img to hsv
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h = hsv[:,:,0]
s = hsv[:,:,1]
v = hsv[:,:,2]

# write the hue to a file
np.savetxt('h.txt', h)

# # shift the hue
    
# # cv2 will clip automatically to avoid color wrap-around
# huechange = 10   # 0 is no change; 0<=huechange<=180
# hnew = cv2.add(h, huechange)

# # combine new hue with s and v
# hsvnew = cv2.merge([hnew,s,v])

# # convert from HSV to BGR
# result = cv2.cvtColor(hsvnew, cv2.COLOR_HSV2BGR)

# # save result
# cv2.imwrite('result.png', result)
    
# # decide if you should keep or not depending on the type of hue
    
    

# if huechange < 10:
#     print("keep")
# else:
#     print("discard")
