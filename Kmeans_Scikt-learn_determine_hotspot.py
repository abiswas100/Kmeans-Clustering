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
from skimage import draw
import csv


'''
Functions used for different calculations on the objects. 
1. Calcualting all coordinates within a polygon given the edge coordinates
2. Calculate v_values from the generated coordinates
3. Calculating the mean of all u_values calculated within an object (polygon)
'''
def polygon_area_calculation(x_inputs, y_inputs):
    '''
    Function generate a list of all coordinates that are found within the polygon object.
    Generates a list of x and y coordinates of the same length (they are pairs). In order to
    access the coordinates, step through each list (x_coordiantes, y_coordinates) at the same rate
    ie. one for loop with len(x_coordinates)
    :param x_inputs: list of x coordinates from the annotated json file
    :param y_inputs: list of y coordinates from the annotated json file
    :return: x_coordinates, y_coordinates which hold the x and y, respectively, coordinates of the polygon.
    '''
    r = np.array(x_inputs)
    c = np.array(y_inputs)
    x_coordinates, y_coordinates = draw.polygon(r, c)
    return x_coordinates, y_coordinates



'''
Main function used to parse/open/initiate calculations for all files within the chosen project
TODO: Rewrite so this function is called each time you want to do calculation, not it looping through all files
'''
import json
def start_parsing(json_files, project_name):
    draw_window = []
    draw_face = []
    filename = json_files.split('.')

 
    with open('Data/json/' + "0633_MWIR.jpg.json") as json_content:
        json_data = json.load(json_content)
        for entry in json_data['objects']:
            if (entry['classTitle'] == 'Facet' or entry['classTitle'] == 'Facade' or entry['classTitle'] == 'Facades'):
                x_values = []
                y_values = []
                points = entry['points']
                exterior = points['exterior']
                for i, coordinates in enumerate(exterior):
                    x_values.append(exterior[i][1])
                    y_values.append(exterior[i][0])
                if (len(x_values) < 4):
                    print("ERROR: LESS THAN 4 POINTS ANNOTATED FOR WINDOW. NUMBER OF POINTS: {}".format(
                        len(x_values)))
                else:
                    x_coordinates, y_coordinates = polygon_area_calculation(x_values, y_values)
        
        
        #X_coordiantes and y_coordiantes now hold points of interes
        os.chdir(r"Museum Clustering Tryouts//images")
        for files in os.listdir():
            if(files.endswith('.jpg')):
                img = cv2.imread(str(files))
                filenames.append(files)
        new_list = []
        for i in range(len(x_coordinates)):
            print("{} {}".format(x_coordinates[i], y_coordinates[i]))
            #new_list.append(img[x_coordinates[i][y_coordinates[i]]])
            r ,g,b = img[x_coordinates[i], y_coordinates[i]]
            new_list.append([r,g,b])
            
            
        print(len(new_list)),filenames
        
# start_parsing("test", "test")
#         for i in len(x_coordiantes):
            
# counter = 0  
#     #         counter = counter+1
#     # else:            
#     #           break

new_image_list,filenames = start_parsing()
#Restricting python to use only 2 cores
cpu_nums = list(range(psutil.cpu_count()))
proc = psutil.Process(os.getpid())
proc.cpu_affinity(cpu_nums[:-2]) #will use all CPU cores uncomment to use 2 cores
print("CPUS being consumed..",cpu_count())


pbar = ProgressBar()
start = time.time()
clustered_images_list = [] #list containing all the clustered outputs

 # Running 6 clusters on each image of Museum
 # For Twamley keep cluster above 10 
print("")
print("Clustering the image ")
labels_of_all_image = []
for image in pbar(new_image_list):
    # reshape the image to a 2D array of pixels and 3 color values (RGB)
    pixel_values = image.reshape((-1, 3))
    # convert to float
    pixel_values = np.float32(pixel_values)
    print("")
    #create an array for the number of clusters
    kmeans = KMeans(n_clusters=10, random_state=0, n_jobs = -1).fit(pixel_values)
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
best_cluster_of_all_image = []
density_of_all_image = []
for image in clustered_images_list:
    masked_image = 0
    masked_image = np.copy(image)
    # convert to the shape of a vector of pixel values
    masked_image = masked_image.reshape((-1, 3))
    # index_of_image = clustered_images_list.index(image)
    best_cluster,data_of_all_cluster = fb.calculate_temperature(labels_of_all_image[counter],filenames[counter])
    best_cluster_of_all_image.append(best_cluster)
    labels = labels_of_all_image[counter]
    for i in range(0,10):
        if i == best_cluster:
            masked_image[labels == best_cluster] = [255,255,255]        
        # else:
        #     masked_image[labels == i] = [0,0,0]
    masked_image = masked_image.reshape(image.shape)
    masked_image_list.append(masked_image)     
    counter = counter+1  
    count = 0
    for label in labels:
        if label ==  best_cluster: count = count +1

    density = round((count/327860)*100)
    print("Density of hotspot..",density,'%')
    density_of_all_image.append(density)
    
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
print("Images loaded to disk..pushing clustering information to disk")
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
    
print("Finished .................")
print(" ")
print(" ")
