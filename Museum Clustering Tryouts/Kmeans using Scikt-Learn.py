

from PIL import Image
import cv2
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, DBSCAN
import matplotlib.pyplot as plt
import time

filename = "0012_MWIR (2).jpg"
image = cv2.imread(filename)
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

# reshape the image to a 2D array of pixels and 3 color values (RGB)
pixel_values = image.reshape((-1, 3))
# convert to float
pixel_values = np.float32(pixel_values)
print(pixel_values)

start = time.time()
kmeans = KMeans(n_clusters=3, random_state=0, n_jobs = -1).fit(pixel_values)
end = time.time()
print("Time consumed in working: ",end - start)

centers = kmeans.cluster_centers_
centers = np.uint8(centers)
print(centers)
labels = kmeans.labels_
print(labels)

segment_image = centers[labels]

segment_image = segment_image.reshape(image.shape)
plt.imshow(cv2.cvtColor(segment_image, cv2.COLOR_BGR2RGB))
