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
                if(i >= 9):
                    pixel_temperature.append(data[0:])
    else:
        with open(csv_filename) as csv_file:
            csv_file_content = csv.reader(csv_file, delimiter=',', quotechar='|')
            pixel_temperature = []
            for i, data in enumerate(csv_file_content):
                if(i >= 1):
                    pixel_temperature.append(data[0:])
    
    return pixel_temperature

#This function call the extract temperature function and calculates surface temperature and hottest cluster

def calculate_temperature(labels,filename):
    print("")
    print("For image - ",filename)
    best_cluster = 0
    cluster_averages = []
    data_of_all_cluster = []
    csv_filename = filename[:-4] + '.csv'
    temperature = extract_temperature(csv_filename) #calling the extract temperature to give the all the pixel_temps in the temperature array
    for cluster in set(labels):         #set(labels) == (0,1,2,3,4,5)
        temp_array = []
        pixel_labels = np.where(labels == cluster)
        for pixel_label in pixel_labels: 
            for pixel in pixel_label : 
                try:#assuming pixel_label is the index that is in the current cluster
                    X_coordinate = int(pixel/512)                     #the row in the CSV
                    Y_coordinate = int(pixel - (X_coordinate*512))    #Subtract the row * 512 to get the location of the y coord
                    temp = float(temperature[X_coordinate][Y_coordinate])  
                    temp_array.append(temp)
                except IndexError: 
                    break       
        try:
            minimum = min(temp_array)
            maximum = max(temp_array)
            average = mean(temp_array)
            data = list([cluster,minimum,maximum,average])        
        except ValueError:
            pass
        finally:    
            print("For Cluster = ",cluster)
            print("minimum Surface Temperature = ",minimum)
            print("maximum Surface Temperature = ",maximum)
            print("average Surface Temperature = ",average)
            cluster_averages.append(average)
            data_of_all_cluster.append(data)        
    print("")
    max_avg = max(cluster_averages)
    print("Maximum average temperature of all clusters = ",max_avg)
    best_cluster = cluster_averages.index(max_avg)
    print("The hottest cluster = ",best_cluster)

    return best_cluster , data_of_all_cluster
