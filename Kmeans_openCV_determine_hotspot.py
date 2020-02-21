#!/usr/bin/env python
# coding: utf-8

# In[207]:


from PIL import Image
import cv2 
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, DBSCAN
import matplotlib.pyplot as plt
import time


# In[239]:


image = cv2.imread("F:\Kmeans\Museum_Tryout_12.jpg")
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))


# In[240]:


# reshape the image to a 2D array of pixels and 3 color values (RGB)
pixel_values = image.reshape((-1, 3))
# convert to float
pixel_values = np.float32(pixel_values)
print(pixel_values)
len(pixel_values)


# In[241]:


#create an array for the number of clusters
n_clusters = 6
averages = []


# In[242]:


criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.1)


# In[243]:


start = time.time()
compactness, labels, centers = cv2.kmeans(pixel_values, n_clusters, None, criteria, 10, cv2.KMEANS_PP_CENTERS)
end = time.time()
print("Time consumed in working: ",end - start)


# In[244]:


# convert back to 8 bit values
centers = np.uint8(centers)
print(centers)
# flatten the labels array
labels = labels.flatten()
# print(labels)


# In[245]:


print(set(labels))
print(len(labels))


# In[246]:


compactness


# In[247]:


segmented_image = centers[labels]
segmented_image


# In[248]:


# reshape back to the original image dimension
segmented_image = segmented_image.reshape(image.shape)
# show the image
plt.imshow(cv2.cvtColor(segmented_image, cv2.COLOR_BGR2RGB))


# In[274]:


# disable only the cluster number 2 (turn the pixel into black)
masked_image = np.copy(image)
# convert to the shape of a vector of pixel values
masked_image = masked_image.reshape((-1, 3))
#masked_image


# In[275]:


# color (i.e cluster) to disable
clusters = [0,1,2,3,4,5]


# In[276]:


#for x in clusters:
temp = np.array()    #temp array that has the pixel values for a specific cluster

temp = masked_image[labels == 0]
# print("\ncluster : ",x )""
temp=temp.flatten()
print(len(temp))
print(temp)


# In[277]:


# convert back to original shape
for i in clusters:
    masked_image[labels == i] = [0,0,0]
masked_image[labels == 2] = [255,255,255]   #hotspot for 12 is cluster 2
masked_image = masked_image.reshape(image.shape)
# show the image
plt.imshow(cv2.cvtColor(masked_image, cv2.COLOR_BGR2RGB))


# In[ ]:




