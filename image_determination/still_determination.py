# in development!!!!!!

# takes the stills scrapped in the directory and determines if the dominant color is a "good" color.

import matplotlib
import matplotlib.pyplot as plt
import os

# load all jpgs in curren directory
images = os.listdir()
images = [i for i in images if i[-3:] == 'jpg']

# split the images into 6 individual images horizonally
fig, ax = plt.subplots(2, 3, figsize=(15, 10))
ax = ax.ravel()
for i in range(len(images)):
    img = plt.imread(images[i])
    ax[i].imshow(img)
    ax[i].set_title(images[i])
    ax[i].set_axis_off()
plt.show()


def color_check():
    for i in images:
        img = plt.imread(i)
        img = img / 255
