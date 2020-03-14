import U_value as U_val

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
    #print("length of Pixel temp",len(pixel_temperature))
    return pixel_temperature


#the function only return only the min,max avg of the annotated region

def calculate_temperature(labels,filename,coordinates):   
    csv_filename = filename[:-4] + '.csv'
    temperature =  extract_temperature(csv_filename)
    print("")
     
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
            # print(filename,len(temperature),len(coordinates))
            # exit()        
    '''
    Adding  Overall U-values for the object 
    '''
    u_value_eq1_points = []
    u_value_eq2_points = []
    u_value_eq3_points = []
    u_value_eq4_points = []
    ou1,ou2,ou3,ou4 = 0,0,0,0
    
    for row in temperature:  #iterating over temperature which is 512*640
        for i in range(len(row)-1):
            pixel_temp = float(row[i])
            #U value calculation
            u_value_1, u_value_2, u_value_3, u_value_4 = U_val.u_value_calculation(pixel_temp)
            # temp_array.append(float(i))
            u_value_eq1_points.append(u_value_1)
            u_value_eq2_points.append(u_value_2)
            u_value_eq3_points.append(u_value_3)
            u_value_eq4_points.append(u_value_4)
    ou1 = mean(u_value_eq1_points)/5.678
    ou2 = mean(u_value_eq2_points)/5.678
    ou3 = mean(u_value_eq3_points)/5.678
    ou4 = mean(u_value_eq4_points)/5.678
    print(ou1,ou2,ou3,ou4)
    '''
    Getting Min Max average for objects and selecting the best cluster and U-values of hotspot
    '''

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
        
        min2 = []  # to store only those values which are positive to calculate minimum
        #calculate minimum values
        for val in temp_array:
            if val >= 0:
                min2.append(val)        
            else:continue
        try:
            minimum = min(min2)
        except ValueError:
            minimum = min(temp_array)
        maximum = max(temp_array)
        average = mean(temp_array)
        
        '''
        Finding the U-values for Hotspots
        '''
        hu_value_eq1_points,hu_value_eq2_points,hu_value_eq3_points,hu_value_eq4_points = [],[],[],[]
        for t in temp_array:
            #U value calculation
            hu_value_1, hu_value_2, hu_value_3, hu_value_4 = U_val.u_value_calculation(float(t))
            # temp_array.append(float(i))
            hu_value_eq1_points.append(hu_value_1)
            hu_value_eq2_points.append(hu_value_2)
            hu_value_eq3_points.append(hu_value_3)
            hu_value_eq4_points.append(hu_value_4)
        
        hu1 = mean(hu_value_eq1_points)/5.678
        hu2 = mean(hu_value_eq2_points)/5.678
        hu3 = mean(hu_value_eq3_points)/5.678
        hu4 = mean(hu_value_eq4_points)/5.678     
        
        data = list([cluster,minimum,maximum,average,ou1,ou2,ou3,ou4,hu1,hu2,hu3,hu4])    
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
















