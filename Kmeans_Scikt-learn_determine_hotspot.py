import optimum_K as op
import Find_best_cluster as fb

import os
from pathlib import Path
import shutil as s
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
        # if(counter == 0):   # to input all the image just remove the conditional statements and use the below 4 lines
            img = cv2.imread(str(files))
            image_list.append(img)
            filename.append(files)
print("")
print("All Images loaded into array")
    #         counter = counter+1
    # else:            
    #           break

#Restricting python to use only 2 cores
cpu_nums = list(range(psutil.cpu_count()))
proc = psutil.Process(os.getpid())
# proc.cpu_affinity(cpu_nums[:2]) #will use all CPU cores uncomment to use 2 cores
print("CPUS being consumed..",cpu_count())


pbar = ProgressBar()
start = time.time()
clustered_images_list = [] #list containing all the clustered outputs
 # Running 6 clusters on each image of Museum
 # For Twamley keep cluster above 10 
print("")
print("Clustering the image ")
labels_of_all_image = []
for image in pbar(image_list):
    # reshape the image to a 2D array of pixels and 3 color values (RGB)
    pixel_values = image.reshape((-1, 3))
    # convert to float
    pixel_values = np.float32(pixel_values)
    print("")
    # print("The pixel array is ")
    # print(pixel_values)
    # print("Length of the pixel value list",len(pixel_values))
    # print("")
    #this function will return the best k for each image
    
    # cluster = op.silhoette(pixel_values)
    
    #create an array for the number of clusters
    kmeans = KMeans(n_clusters=6, random_state=0, n_jobs = -1).fit(pixel_values)
    # convert back to 8 bit values
    centers = kmeans.cluster_centers_
    centers = np.uint8(centers)
    # print("The centers are ----",centers)
    # flatten the labels array
    labels = kmeans.labels_
    labels_of_all_image.append(labels)
    # print("The actual labels array",labels)
    # print("The labels set - ",set(labels),"   The length of the labels array",len(labels))
    segmented_image = centers[labels]
    segmented_image = segmented_image.reshape(image.shape)
    clustered_images_list.append(segmented_image)

print(" ")
end = time.time()
print("Time consumed in clustering: ",end - start)


#function to mask only the hotspot
print("")
print("Masking the image finding the best cluster")
masked_image_list = []
print("")
counter = 0
for image in clustered_images_list:
    masked_image = 0
    masked_image = np.copy(image)
    # convert to the shape of a vector of pixel values
    masked_image = masked_image.reshape((-1, 3))
    # index_of_image = clustered_images_list.index(image)
    best_cluster = fb.calculate_temperature(labels_of_all_image[counter],filename[counter])
    labels = labels_of_all_image[counter]
    for i in range(0,6):
        if i == best_cluster:
            masked_image[labels == best_cluster] = [255,255,255]      
        # else:
        #     masked_image[labels == i] = [0,0,0]
    masked_image = masked_image.reshape(image.shape)
    masked_image_list.append(masked_image)     
    counter = counter+1  

#Saving the masked images in Kmeans-masked-output folder
print("  ")
try:
    path = os.getcwd()
    parent_path = Path(path).parent
    os.chdir(parent_path)    
    os.mkdir('kmeans-output')

except FileExistsError:
    print(" ")
    print("Folder already exists so removing the previous outputs and creating again")
    s.rmtree('kmeans-output')
    os.mkdir('kmeans-output')

finally:
    print("Pushing clustered images to disk..............")    
    os.chdir('kmeans-output')
    counter = 0
    for img in masked_image_list:
        cv2.imwrite(filename[counter], img)
        counter = counter + 1
        img = 0
print("Finished .................")
print(" ")
print(" ")



# #Saving the clustered images in output folder
# print("  ")
# try:
#     path = os.getcwd()
#     parent_path = Path(path).parent
#     os.chdir(parent_path)    
#     os.mkdir('kmeans-output')

# except FileExistsError:
#     print(" ")
#     print("Folder already exists so removing the previous outputs and creating again")
#     s.rmtree('kmeans-output')
#     os.mkdir('kmeans-output')
#     print(" ")
# finally:
#     print("Pushing clustered images to disk..............")    
#     os.chdir('kmeans-output')
#     counter = 0
#     for img in clustered_images_list:
#         print(" ")
#         cv2.imwrite(filename[0], img)
#         counter = counter + 1
# print("Clustered image stored .................")

