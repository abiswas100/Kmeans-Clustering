
from PIL import Image
import cv2
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import os 


# import os
# #os.chdir('C:\Users\avhishek.biswas\Documents\Avhishek\HeatLossProject\Museum Clustering Tryouts')
# image_list = []
# for files in os.listdir('ds\\img'):
#     image_list.append(files)


filename = "0012_MWIR (2).jpg"
image = cv2.imread(filename)
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

# reshape the image to a 2D array of pixels and 3 color values (RGB)
pixel_values = image.reshape((-1, 3))
# convert to float
pixel_values = np.float32(pixel_values)
print(pixel_values)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.1)

# number of clusters (K)
k = 6
import time
start = time.time()
compactness, labels, centers = cv2.kmeans(pixel_values, k, None,criteria, 10, cv2.KMEANS_PP_CENTERS)
end = time.time()
print("Time consumed in working: ",end - start)

# convert back to 8 bit values
centers = np.uint8(centers)
print(centers)
# flatten the labels array
labels = labels.flatten()
# print(labels)

segmented_image = centers[labels]

# reshape back to the original image dimension
segmented_image = segmented_image.reshape(image.shape)
# show the image
plt.imshow(cv2.cvtColor(segmented_image, cv2.COLOR_BGR2RGB))

try:
    os.mkdir('kmean-output')
except FileExistsError:
    print("File already exists so just saving them in that folder")
    pass
    
os.chdir('kmean-output')
os.getcwd()
cv2.imwrite(filename, segmented_image)

# Masking the hotspot

# disable only the cluster number 2 (turn the pixel into black)
masked_image = np.copy(image)
# convert to the shape of a vector of pixel values
masked_image = masked_image.reshape((-1, 3))
# color (i.e cluster) to disable
clusters = [0,1,2,4,5]
for i in clusters:
    masked_image[labels == i] = [0,0,0]
masked_image[labels == 3] = [255,255,255]
# convert back to original shape
masked_image = masked_image.reshape(image.shape)
# show the image
plt.imshow(cv2.cvtColor(masked_image, cv2.COLOR_BGR2RGB))


# masked_image.shape
# test = masked_image[0][1]
# test2 = [0,0,0]
          
# for i in range(512):
#     for y in range(640):
#           #print(masked_image[i][y])
#           if((masked_image[i][y] != test2).all()):
#               masked_image[i][y] == [255,255,255]

# plt.imshow(cv2.cvtColor(masked_image, cv2.COLOR_BGR2RGB))

