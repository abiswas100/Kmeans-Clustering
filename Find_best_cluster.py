import os
from pathlib import Path

import re
import csv
import numpy as np
from statistics import mean
import pandas as pd
#this function works just fine we can use this
def extract_temperature(csv_filename):
    '''
    Function will extract all of the temperatures within a csv file into a 2D list of lenth [512][640].
    The temperature values should be in celisus and the 2D list cannot be any smaller than this.
    :param csv_filename: CSV filename you you are trying to parse
    :param dir_path: Parent directory to OGI_u_value_module project
    :param csv_file_path: CSV filepath extension
    :return: List containing [512][640] = 327680 data points
    '''
    path = os.getcwd()
    parent_path = Path(path).parent
    
    os.chdir(parent_path)    
    os.chdir('csv')

    csv_name = re.split(r'[_.\s ]', csv_filename)
    if('MWIR' in csv_name):
        with open(csv_filename) as csv_file:
            csv_file_content = csv.reader(csv_file, delimiter=',', quotechar='|')
            pixel_temperature = []

            for i, data in enumerate(csv_file_content):
                if(i >= 8):
                    pixel_temperature.append(data[0:])
    else:
        with open(csv_filename) as csv_file:
            csv_file_content = csv.reader(csv_file, delimiter=',', quotechar='|')
            pixel_temperature = []
            for i, data in enumerate(csv_file_content):
                if(i >= 1):
                    pixel_temperature.append(data[0:])
    print("length of Pixel temp",len(pixel_temperature))
    return pixel_temperature


#the function only return only the min,max avg of the annotated region

def calculate_temperature(labels,filename,coordinates):   
    csv_filename = filename[:-4] + '.csv'
    temperature =  extract_temperature(csv_filename)
    print("")
    print("Working on file",filename) 
    cluster_averages = []
    data_of_all_clusters = []
    
    
    list_labels = labels.tolist()
    
    useful_temp = []
    for i in coordinates:
        x = i[0]
        y = i[1]
        #print(x,y)
        try:
            temp = float(temperature[x][y])
            useful_temp.append(temp)
        except IndexError: continue
    print("Length of useful_temp",len(useful_temp),"Length of List_labels",len(list_labels))
    no_of_labels = set(labels)

    for cluster in no_of_labels:
        temp_array = []
        
        for j in range(len(useful_temp)): 
            try:
                if list_labels[j] == cluster:
                    temp_array.append(useful_temp[j])        
            except IndexError:
                print("")
                print("Jth index",j)
                exit()
        min2 = [] 
        #calculate minimum values
        for val in temp_array:
            if val >= 0:
                min2.append(val)        
            else:continue
        try:
            minimum = min(min2)
        except ValueError:minimum = min(temp_array)
        maximum = max(temp_array)
        average = mean(temp_array)
        data = list([cluster,minimum,maximum,average])    
               
        print("For Cluster = ",cluster)
        print("minimum Surface Temperature = ",minimum)
        print("maximum Surface Temperature = ",maximum)
        print("average Surface Temperature = ",average)
        cluster_averages.append(average)
        data_of_all_clusters.append(data)        
    print("")
    max_avg = max(cluster_averages)
    print("Maximum average temperature of all clusters = ",max_avg)
    best_cluster = cluster_averages.index(max_avg)
    print("The hottest cluster = ",best_cluster)

    return best_cluster , data_of_all_clusters



#This function call the extract temperature function and calculates surface temperature and hottest cluster

# def calculate_temperature(labels,filename,coordinates):
#     print("")
#     print("For image - ",filename)
#     best_cluster = 0
#     cluster_averages = []
#     data_of_all_cluster = []
#     csv_filename = filename[:-4] + '.csv'
#     temperature = extract_temperature(csv_filename) #calling the extract temperature to give the all the pixel_temps in the temperature array
#     for cluster in set(labels):         #set(labels) == (0,1,2,3,4,5)
#         temp_array = []
#         pixel_labels = np.where(labels == cluster)
#         for pixel_label in pixel_labels: 
#             counter = 0
#             #print("Pixel labels",pixel_labels,"length of PIxel_labels",len(pixel_labels))
#             for pixel in pixel_label : 
#                 try:
#                     #assuming pixel_label is the index that is in the current cluster
#                     x = int(pixel/512)                     #the row in the CSV
#                     y = int(pixel - (x*512))    #Subtract the row * 512 to get the location of the y coord
#                     temp = float(temperature[x][y])  
#                     temp_array.append(temp)
#                 except IndexError: 
#                     break       
#         try:
#             minimum = min(temp_array)
#             maximum = max(temp_array)
#             average = mean(temp_array)
#             data = list([cluster,minimum,maximum,average])        
#         except ValueError and UnboundLocalError:
#             minimum,maximum,average = 0,0,0
#         finally:    
#             # print("For Cluster = ",cluster)
#             # print("minimum Surface Temperature = ",minimum)
#             # print("maximum Surface Temperature = ",maximum)
#             # print("average Surface Temperature = ",average)
#             cluster_averages.append(average)
#             data_of_all_cluster.append(data)        
#     print("")
#     max_avg = max(cluster_averages)
#     print("Maximum average temperature of all clusters = ",max_avg)
#     best_cluster = cluster_averages.index(max_avg)
#     print("The hottest cluster = ",best_cluster)

#     return best_cluster , data_of_all_cluster


            