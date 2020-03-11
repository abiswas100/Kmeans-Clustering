import optimum_K as op
import Find_best_cluster as fb
import consider_annotation as ann
import getpass
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
from skimage import draw
from PIL import Image, ImageDraw, ImageFont 

import csv
import json


#############################
#  Importing the images   ###
#############################

image_list = []
filenames = []
counter = 0
os.chdir(r"data//images")
for files in os.listdir():
    if(files.endswith('.jpg')):
        # if(counter == 0):   # to input all the image just remove the conditional statements and use the below 4 lines and comment from counter to break
            img = cv2.imread(str(files))
            image_list.append(img)
            filenames.append(files)
print("")
print("All Images loaded into array")
    #         counter = counter+1
    # else:            
    #     break

############################################################    

# Restricting python to use only 2 cores
cpu_nums = list(range(psutil.cpu_count()))
proc = psutil.Process(os.getpid())
proc.cpu_affinity(cpu_nums[:-2]) #will use all CPU cores uncomment to use 2 cores
print("CPUS being consumed..",cpu_count())


pbar = ProgressBar()
start = time.time()
clustered_images_list = [] #list containing all the clustered outputs

 # Running 10 clusters on each image of Museum
 # For Twamley keep cluster above 20 


print("")
print("Clustering the image ")
labels_of_all_image = []
coordinates_of_all_images = []
a = 0 #just a loop counter
for image in pbar(image_list):
    #adding annotations and changing the image_list array
    pixel_values,coordinates = ann.start_parsing(image,filenames[a])
    coordinates_of_all_images.append(coordinates)
    pixel_values = np.float32(pixel_values)

    #create an array for the number of clusters  
    try:
        kmeans = KMeans(n_clusters=10, random_state=0, n_jobs = -1).fit(pixel_values)
        # convert back to 8 bit values
        centers = kmeans.cluster_centers_
        centers = np.uint8(centers)
        # print("The centers are ----",centers)
        # flatten the labels array
        labels = kmeans.labels_
        labels_of_all_image.append(labels)
        segmented_image = centers[labels]
        clustered_images_list.append(segmented_image)
        a = a + 1
    except ValueError: 
        getpass.getpass('Delete that file and press Enter')
        continue

print(" ")
end = time.time()
print("Time consumed in clustering: ",end - start)

########################################
## function to mask only the hotspot  ##
########################################
print("")
print("Finding the Cluster containing the hotspot and Masking it ...")
print("")

counter = 0
masked_image_list = []
best_cluster_of_all_image = []
density_of_all_image = []


for image in clustered_images_list:
    #print("image shape",image.shape)              ### size of the window in the image as a 1D array
    masked_image = 0
    masked_image = np.copy(image)
    # convert to the shape of a vector of pixel values
    # masked_image = masked_image.reshape((-1, 3))

    best_cluster,data_of_all_cluster = fb.calculate_temperature(labels_of_all_image[counter],filenames[counter],coordinates_of_all_images[counter])
    best_cluster_of_all_image.append(best_cluster)
    
    labels = labels_of_all_image[counter]
    
    img = image_list[counter]  # img is the original raw image in (512,640)
    #print("Original image shape",img.shape)
    
    # # #Add reconstruction of Image code here
    # numbers = []
    # counters = 0
    # indexes = 0
    # for i in range(len(x_coord)):
    #     for x in range(len(x_coord)):
            
    #         if(x_coord[x] ==  indexes):
    #             #print("GETTING HERE")
    #             for j in range(len(y_coord)):
    #                 counters = counters + 1
    #                 #print("GETTINGHERE")
    #                 #print("{} {}".format(x_coord[i].item,y_coord[i].item))
    #             #print(counters)
    #     numbers.append(counters)
    #     counters = 0
    #     indexes = indexes + 1
    # for number in numbers:
    #     print(number)

    # for i in range(0,10):
    #     if i == best_cluster:
    #         #testim = Image.open('../images/' + filenames[counter])
    #         #pixels = testim.load()
    #         masked_image[labels == best_cluster] = [255,255,255] 
    #         #pixels[y, x] = (255,255,255)       
    

    
    masked_image = masked_image.reshape(image.shape)
    # print(masked_image.shape)
    masked_image_list.append(masked_image)     
    counter = counter+1  
    # for i in range(len(x_coord)):
    #     print("{} {}".format())
    
    
    #Finding the Density of Hotspot in the region
    count = 0
    for label in labels:
        if label ==  best_cluster: count = count +1
    #print(count)
    density = (count/len(pixel_values))*100
    print("Density of hotspot..",density,'%')
    density_of_all_image.append(density)



#################################################
##    Saving Images and storing into CSVs      ##
#################################################

    
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
        cv2.imwrite(filenames[counter], img)
        counter = counter + 1
        img = 0
print("Images loaded to disk..pushing clustering information to csv file")
print("")    
try:
    file = 'kmeans'
    with open(file + 'museum.csv' , 'a' ,newline='') as csvfile :
        writer = csv.writer(csvfile)
        writer.writerow(['Filename','Hotspot-cluster','minimum','maximum','average','density']) 
        for i in range(0,len(filenames)):
            file = filenames[i]
            cluster = data_of_all_cluster[best_cluster_of_all_image[i]][0]
            minimum = data_of_all_cluster[best_cluster_of_all_image[i]][1]
            maximum = data_of_all_cluster[best_cluster_of_all_image[i]][2]
            average = data_of_all_cluster[best_cluster_of_all_image[i]][3]
            density = density_of_all_image[i]
            writer.writerow([file,cluster,minimum,maximum,average,str(density)+'%'])
except FileExistsError:
    os.remove('mueseum.csv')   

print(ann.not_working)
print("Finished .................")
print(" ")
print(" ")
