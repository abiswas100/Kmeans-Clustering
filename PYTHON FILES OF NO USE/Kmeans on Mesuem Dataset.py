import os
import time
from multiprocessing import cpu_count

import cv2
import matplotlib.pyplot as plt
import numpy as np
import psutil
from progressbar import ProgressBar
from sklearn.cluster import KMeans


#run this file directly in the images folder of Twamley or Museum
#Storing the images from File to an array named image_list
image_list = []
filename = []
for files in os.listdir():
    if(files.endswith('.jpg')):
        img = cv2.imread(str(files))
        image_list.append(img)
        filename.append(files)

#Restricting python to use only 2 cores
cpu_nums = list(range(psutil.cpu_count()))
proc = psutil.Process(os.getpid())
proc.cpu_affinity(cpu_nums[:2])
print("CPUS being consumed..",cpu_count())

pbar = ProgressBar()
start = time.time()
clustered_images_list = []

 # Running 6 clusters on each image of Museum
 # For Twamley keep cluster above 10 iam

print("Clustering the dataset in into ")
for image in pbar(image_list):
    # reshape the image to a 2D array of pixels and 3 color values (RGB)
    pixel_values = image.reshape((-1, 3))
    # convert to float for kmeans to understand
    pixel_values = np.float32(pixel_values)
    #Criteria for Stopping the clustering
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.01)
    #KMEANS 
    clusters = 6
    compactness, labels, centers = cv2.kmeans(pixel_values, clusters, None,criteria, 10, cv2.KMEANS_PP_CENTERS)
    # convert back to 8 bit values
    centers = np.uint8(centers)
    # flatten the labels array
    labels = labels.flatten()
    #Reconstructing the Clustered Image
    segmented_image = centers[labels]
    segmented_image = segmented_image.reshape(image.shape)
    clustered_images_list.append(segmented_image)

end = time.time()
print("Time consumed in working: ",end - start)  
print("clustering completed ......")

# saving the clustered images in a folder

try:
    os.mkdir('kmeans-output')
except FileExistsError:
    print("File already exists so just saving them in that folder")
    pass
print("Pushing clustered images to disk..............")    
os.chdir('kmeans-output')
counter = 0
for img in clustered_images_list:
    # show the image
    #plt.imshow(cv2.cvtColor(segmented_image, cv2.COLOR_BGR2RGB))
    #cv2.imwrite(str(counter) + '.jpg', img)
    cv2.imwrite(filename[counter], img)
    counter = counter + 1
print("Finished .................")