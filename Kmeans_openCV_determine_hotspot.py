import os
import time
from multiprocessing import cpu_count

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import psutil
from progressbar import ProgressBar
from sklearn.cluster import KMeans

image_list = []
filename = []
counter = 0  
os.chdir(r"Museum Clustering Tryouts//images")
for files in os.listdir():
    if(files.endswith('.jpg')):
        if(counter == 0):   # to input all the image just remove the conditional statements and use the below 4 lines
            img = cv2.imread(str(files))
            image_list.append(img)
            filename.append(files)
            print("All Images loaded into array")
            counter = counter+1
        else:            
            break



#Restricting python to use only 2 cores
cpu_nums = list(range(psutil.cpu_count()))
proc = psutil.Process(os.getpid())
proc.cpu_affinity(cpu_nums[:2])
print("CPUS being consumed..",cpu_count())


    # reshape the image to a 2D array of pixels and 3 color values (RGB)
pixel_values = image.reshape((-1, 3))
    # convert to float
pixel_values = np.float32(pixel_values)
print(pixel_values)
len(pixel_values)

#create an array for the number of clusters
n_clusters = 6
averages = []
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.1)
start = time.time()
compactness, labels, centers = cv2.kmeans(pixel_values, n_clusters, None, criteria, 10, cv2.KMEANS_PP_CENTERS)
end = time.time()
print("Time consumed in working: ",end - start)
# convert back to 8 bit values
centers = np.uint8(centers)
print(centers)
# flatten the labels array
labels = labels.flatten()
# print(labels)
print(set(labels))
print(len(labels))

segmented_image = centers[labels]
# reshape back to the original image dimension
segmented_image = segmented_image.reshape(image.shape)
# show the image
plt.imshow(cv2.cvtColor(segmented_image, cv2.COLOR_BGR2RGB))


# disable only the cluster number 2 (turn the pixel into black)
masked_image = np.copy(image)
# convert to the shape of a vector of pixel values
masked_image = masked_image.reshape((-1, 3))
# color (i.e cluster) to disable
clusters = [0,1,2,3,4,5]
#for x in clusters:
temp = np.array()    #temp array that has the pixel values for a specific cluster
temp = masked_image[labels == 0]
# print("\ncluster : ",x )""
temp=temp.flatten()
print(len(temp))
print(temp)

# convert back to original shape
for i in clusters:
    masked_image[labels == i] = [0,0,0]
masked_image[labels == 2] = [255,255,255]   #hotspot for 12 is cluster 2
masked_image = masked_image.reshape(image.shape)
# show the image
plt.imshow(cv2.cvtColor(masked_image, cv2.COLOR_BGR2RGB))






