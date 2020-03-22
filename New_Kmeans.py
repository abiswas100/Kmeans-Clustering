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

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import psutil
from progressbar import ProgressBar
from sklearn.cluster import KMeans
from statistics import mean

import csv
import json

 
def input_images():
    image_list = []
    filenames = []
    #counter = 0
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
        #     breakpass
    
    return image_list,filenames

def add_annotation(image_list,filenames):
    coordinates_of_all_images = []
    pixel_values_of_all_images = []
    counter = 0
    for image in image_list:
        pixel_values,coordinates = ann.start_parsing(image,filenames[counter])
        coordinates_of_all_images.append(coordinates)
        pixel_values_of_all_images.append(pixel_values)
        counter = counter + 1 
    return coordinates_of_all_images,pixel_values_of_all_images

def clustering(image_list,pixel_values_of_all_images,filenames  ):  
    pbar = ProgressBar()
    
    clustered_images_list = [] #list containing all the clustered outputs
    labels_of_all_image = []
    
    print("")
    print("Clustering the image ")
    
    for i in pbar(range(len(image_list))):
        #adding annotations and changing the image_list array
        # pixel_values,coordinates = ann.start_parsing(image,filenames[counter])
        # coordinates_of_all_images.append(coordinates)
        pixel_values = pixel_values_of_all_images[i]
        pixel_values = np.float32(pixel_values)
    
        kmeans = KMeans(n_clusters=3, random_state=0, n_jobs = -1).fit(pixel_values)
        # convert back to 8 bit values
        centers = kmeans.cluster_centers_
        centers = np.uint8(centers)
        labels = kmeans.labels_
        labels_of_all_image.append(labels)
        segmented_image = centers[labels]
        clustered_images_list.append(segmented_image)

    print(" ")
    return labels_of_all_image,clustered_images_list

def masking_image(filenames,image_list,labels_of_all_image,coordinates_of_all_images,clustered_images_list):
    print("length of clustered image",len(clustered_images_list))
    print("")
    print("Finding the Cluster containing the hotspot and Masking it ...")
    print("")
     
    masked_image_list = []
    best_cluster_of_all_image = []
    density_of_all_image = []
    data_of_all_images = []
    
    iterator = 0
    '''
    The lines below iterates over the cluster_image list and converts the pixel to the hotspot_cluster and store 
    the images in the masked image list.. 
    '''

    for iterator in range(len(image_list)):
        best_cluster,data_of_all_cluster = fb.calculate_temperature(labels_of_all_image[iterator],filenames[iterator],coordinates_of_all_images[iterator])
        best_cluster_of_all_image.append(best_cluster)
        data_of_all_images.append(data_of_all_cluster) 


        labels = labels_of_all_image[iterator]
        coordinate = coordinates_of_all_images[iterator]
    
        temp_image = image_list[iterator]
        masked_image = np.copy(temp_image)

        #changing labels    
        for i in range(len(labels)):
            if labels[i] != best_cluster:coordinate[i] = [-1,-1] 
            else:continue
    
        try:    
            temp_image = []        
            for j in coordinate:
                if j != [-1,-1]:
                    masked_image[j[1],j[0]] = [255,255,255]
   
        except UnboundLocalError : 
            print(filenames[iterator])
            print("")

        masked_image_list.append(masked_image)
        #Finding the Density of Hotspot for the 
        count = 0
        for label in labels:
            if label ==  best_cluster: count = count + 1

        density = (count/len(labels))*100
        print("Density of hotspot..",density,'%')
        density_of_all_image.append(density)

    return masked_image_list,best_cluster_of_all_image,data_of_all_images,density_of_all_image

def save_to_file(filenames,masked_image_list,data_of_all_images,density_of_all_image,best_cluster_of_all_image):
    #print("In save_to_file",data_of_all_images)
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
            writer.writerow(['Filename','Hotspot-cluster','minimum','maximum','average','Hotspot-U1','Hotspot-U2','Hotspot-U3','Hotspot-U4','density']) 
        
            for i in range(0,len(filenames)):
                #for a single Image
                file = filenames[i]
                cluster = best_cluster_of_all_image[i]
                data = data_of_all_images[i]
                d = data[cluster]

                minimum = d[1]
                maximum = d[2]
                average = d[3]
                hu1 = d[4]
                hu2 = d[5]
                hu3 = d[6]
                hu4 = d[7]
                den = density_of_all_image[i]

                writer.writerow([file,cluster,minimum,maximum,average,hu1,hu2,hu3,hu4,str(den)+'%'])
    except FileExistsError:
        os.remove('mueseum.csv')   
 
    return 1

def U_value(coordinates_of_all_images,filenames):
    
    U_values_of_all_images = []
    
    for i in range(len(filenames)):    
        coordinates = coordinates_of_all_images[i]
        filename = filenames[i]    
        csv_filename = filename[:-4] + '.csv'

        temperature = fb.extract_temperature(csv_filename)

        useful_temp = [] 
        for i in coordinates:                                                                       #getting the temperature values in a 1-D array for the considered object
            x = i[0]
            y = i[1]
            useful_temp.append(float(temperature[x][y]))
        '''
        Computing Overall U-values for the object and storing in U_vals_Data
        Adding  Overall U-values for the object 
        '''
        #U value calculation
        u_value_eq1_points,u_value_eq2_points,u_value_eq3_points,u_value_eq4_points = [],[],[],[]
        ou1,ou2,ou3,ou4 = 0,0,0,0
    
        for t in useful_temp:                                                                          #iterating over Useful_temp which has all the pixel-temp of the object
                u_value_1, u_value_2, u_value_3, u_value_4 = U_val.u_value_calculation(float(t))
                # temp_array.append(float(i))
                u_value_eq1_points.append(u_value_1)
                u_value_eq2_points.append(u_value_2)
                u_value_eq3_points.append(u_value_3)
                u_value_eq4_points.append(u_value_4)
        ou1 = mean(u_value_eq1_points)/5.678
        ou2 = mean(u_value_eq2_points)/5.678
        ou3 = mean(u_value_eq3_points)/5.678
        ou4 = mean(u_value_eq4_points)/5.678
    
        U_values_of_all_images.append(list([ou1,ou2,ou3,ou4]))
    
    print(len(U_values_of_all_images))
    path = os.getcwd()
    parent_path = Path(path).parent
    os.chdir(parent_path)
    for files in os.listdir():
        if files == 'U-values.csv': os.remove('U-values.csv')
    
    else:
        file = 'U-values'
        with open(file + '.csv' , 'a' ,newline='') as csvfile :
            writer = csv.writer(csvfile)
            writer.writerow(['Filename','U1','U2','U3','U4']) 

            for i in range(0,len(filenames)):
                #for a single Image
                u_values = U_values_of_all_images[i]
                file = filenames[i]
                u1 = u_values[0]
                u2 = u_values[1]
                u3 = u_values[2]
                u4 = u_values[3]
                
                writer.writerow([file,u1,u2,u3,u4])


    os.chdir(path)

    return 1  
