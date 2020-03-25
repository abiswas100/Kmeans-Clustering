import U_value as U_val

import os
from pathlib import Path
import inspect

import re
import csv
import numpy as np
from statistics import mean,variance


def extract_temperature(filename):
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

    csv_filename = filename[:-4] + '.csv'
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
    #print("length of Pixel temp",len(pixel_temperature))
    return pixel_temperature

def calculate_temperature(labels,filename,coordinates): 
    
    print()
    print(filename)

    list_labels = labels.tolist()
    temperature =  extract_temperature(filename)
    
    cluster_averages = []
    data_of_all_clusters = []
    
    '''
    #converting 3-D pixel_temperature array into 1D useful_temp
    '''
    useful_temp = useful_temperature(temperature,coordinates)
    '''
    Finding Min,Max and Average and U_values of Each Cluster
    '''
    no_of_labels = set(labels) 
    for cluster in no_of_labels:
        temp_array = []                                              # temporary array to store temperature of only those pixels belonging to a perticular cluster
        for j in range(len(useful_temp)): 
            if list_labels[j] == cluster:
                temp_array.append(useful_temp[j])        

        print("Cluster  = ",cluster)
        minimum,maximum,average = min_max_average(temp_array)       # function returns the min,max and average for each cluster 
           
        hu1,hu2,hu3,hu4 = U_values(temp_array)                      # function returns the U-values belonging to the cluster
        
        data = list([cluster,minimum,maximum,average,hu1,hu2,hu3,hu4])    

        cluster_averages.append(average)
        data_of_all_clusters.append(data)        
    
    print("")
    best_cluster =  find_hotspot(cluster_averages)

    return best_cluster , data_of_all_clusters 

def useful_temperature(temperature,coordinates):
    useful_temp = [] 
    for i in coordinates:
        x = i[0]
        y = i[1]
        useful_temp.append(float(temperature[x][y]))
    return useful_temp

def min_max_average(temperature):
    stack = inspect.stack()
    caller = stack[1].filename[-13:]
    '''
    Computes Min Max and Average for each cluster 
    '''
    min2 = []  # to store only those values which are positive to calculate minimum
        #calculate minimum values
    for val in temperature:
        if val >= 0:
            min2.append(val)        
        else:continue
    try : minimum = min(min2)
    except ValueError : minimum = min(temperature)
    maximum = max(temperature)
    average = mean(temperature)
    if caller != 'New_Kmeans.py':
        print("minimum Surface Temperature = ",minimum)
        print("maximum Surface Temperature = ",maximum)
        print("average Surface Temperature = ",average) 
    
    return minimum,maximum,average

def U_values(temperature):
        #U value calculation
    u_value_eq1_points,u_value_eq2_points,u_value_eq3_points,u_value_eq4_points = [],[],[],[]
    u1,u2,u3,u4 = 0,0,0,0   
    for t in temperature:
            u_value_1, u_value_2, u_value_3, u_value_4 = U_val.u_value_calculation(float(t))
            # temp_array.append(float(i))
            u_value_eq1_points.append(u_value_1)
            u_value_eq2_points.append(u_value_2)
            u_value_eq3_points.append(u_value_3)
            u_value_eq4_points.append(u_value_4)
        
    u1 = mean(u_value_eq1_points)/5.678
    u2 = mean(u_value_eq2_points)/5.678
    u3 = mean(u_value_eq3_points)/5.678
    u4 = mean(u_value_eq4_points)/5.678 
    return u1,u2,u3,u4

def find_hotspot(cluster_averages):
    
    print("")
    max_avg = max(cluster_averages)
    print("Maximum average temperature of all clusters = ",max_avg)
    best_cluster = cluster_averages.index(max_avg)
    print("The hottest cluster = ",best_cluster) 
    print("Varience =  ",variance(cluster_averages)," and the standard deviation is ...")
    return best_cluster