import re
import csv
import os
import numpy as np

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
best_cluster = 0
cluster_averages = []
def calculate_temperature(image,labels,filename):
    csv_filename = filename[:-4] + '.csv'
    temperature = extract_temperature("csv_filename")
   
    for cluster in set(labels):         #set(labels) == (0,1,2,3,4,5)
        pixel_labels = np.where(labels == cluster)
        for pixel_label in pixel_labels:
            X_coordinate = int(pixel_label/512)
            Y_coordinate = int(pixel_label/512)#change in the proper way
            temp = float(temperature[X_coordinate][Y_coordinate])
            
            total_temp = total_temp + temp
    
            average = total_temp/len(pixel_labels)
    cluster_averages.append(average)           
    return max(cluster_averages)

