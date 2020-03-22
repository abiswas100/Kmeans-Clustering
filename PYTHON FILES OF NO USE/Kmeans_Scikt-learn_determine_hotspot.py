import optimum_K as op
import Find_best_cluster as fb
import consider_annotation as ann
import U_value as U_val

import getpass
import os
from pathlib import Path
import shutil as s
import time
from multiprocessing import cpu_count

from cv2 import cv2
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
        #if(counter == 0): 
            # to input all the image just remove the conditional statements and use the below 4 lines and comment from counter to break
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
    
    try:
        kmeans = KMeans(n_clusters=3, random_state=0, n_jobs = -1).fit(pixel_values)
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
U_vals_of_all_images = []
Data_of_all_images = []

'''
The lines below iterates over the cluster_image list and converts the pixel to the hotspot_cluster and store 
the images in the masked image list.. 
   
'''

for image in clustered_images_list:
    best_cluster,data_of_all_cluster,U_val = fb.calculate_temperature(labels_of_all_image[counter],filenames[counter],coordinates_of_all_images[counter])
    #print("In main",labels_of_all_image[counter],filenames[counter],len(coordinates_of_all_images[counter]))
    best_cluster_of_all_image.append(best_cluster)
    l = labels_of_all_image[counter]
    coordinate = coordinates_of_all_images[counter]
    U_vals_of_all_images.append(U_val)
    Data_of_all_images.append(data_of_all_cluster)


    temp_image = image_list[counter]
    masked_image = np.copy(temp_image)
    
    for i in range(len(l)):
        if l[i] != best_cluster:coordinate[i] = [-1,-1] 
        else:continue
    
    try:    
        temp_image = []        
        for j in coordinate:
            if j != [-1,-1]:
                masked_image[j[1],j[0]] = [255,255,255]
   
    except UnboundLocalError : 
            print(filenames[counter])
            print("")

    #masked_image = masked_image.reshape(image.shape)
    masked_image_list.append(masked_image)
    #Finding the Density of Hotspot for the 
    count = 0
    for label in l:
        if label ==  best_cluster: count = count +1
    #print(count)
    density = (count/len(labels))*100
    print("Density of hotspot..",density,'%')
    density_of_all_image.append(density)
    counter = counter + 1



# for d in Data_of_all_images:
#     print()
#     print(d)
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
        writer.writerow(['Filename','Hotspot-cluster','minimum','maximum','average','U1','U2','U3','U4','Hotspot-U1','Hotspot-U2','Hotspot-U3','Hotspot-U4','density']) 
        
        for i in range(0,len(filenames)):
            file = filenames[i]
            
            cluster = best_cluster_of_all_image[i]
            data = Data_of_all_images[i]

            d = data[cluster]

            minimum = d[1]
            maximum = d[2]
            average = d[3]
            hu1 = d[4]
            hu2 = d[5]
            hu3 = d[6]
            hu4 = d[7]


            density = density_of_all_image[i]
            
            u1 = U_vals_of_all_images[i][0]  
            u2 = U_vals_of_all_images[i][1]
            u3 = U_vals_of_all_images[i][2]
            u4 = U_vals_of_all_images[i][3]

            writer.writerow([file,cluster,minimum,maximum,average,u1,u2,u3,u4,hu1,hu2,hu3,hu4,str(density)+'%'])
except FileExistsError:
    os.remove('mueseum.csv')   

print("Finished .................")
print(" ")
print(" ")