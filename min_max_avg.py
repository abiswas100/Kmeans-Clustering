import u_val as uval
import os
from pathlib import Path
import shutil as s
import cv2
import numpy as np
import psutil

import csv
import re
from statistics import mean
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
    #print(pixel_temperature[0],len(pixel_temperature[0]))
    return pixel_temperature


image_list = []
filename = []
counter = 0  
os.chdir(r"Data//images")
for files in os.listdir():
    if(files.endswith('.jpg')):
        #if(counter == 0):   # to input all the image just remove the conditional statements and use the below 4 lines
            img = cv2.imread(str(files))
            image_list.append(img)
            filename.append(files)
print("")
print("All Images loaded into array")
    #         counter = counter+1
    # else:            
    #     break

data_of_all_images = []
for img in range(len(image_list)):
    temperature = []
    u_value_eq1_points=[]
    u_value_eq2_points = []
    u_value_eq3_points = []
    u_value_eq4_points = []
    
    file = filename[img]
    csvfilename = file[:-4] + '.csv'
    temperature = extract_temperature(csvfilename)      #Getting pixel_temperature from Extract Temp function

    for row in temperature:  #iterating over temperature which is 512*640
        for i in range(len(row)-1):
            pixel_temp = float(row[i])
            #U value calculation
            u_value_1, u_value_2, u_value_3, u_value_4 = uval.u_value_calculation(pixel_temp)
            # temp_array.append(float(i))
            u_value_eq1_points.append(u_value_1)
            u_value_eq2_points.append(u_value_2)
            u_value_eq3_points.append(u_value_3)
            u_value_eq4_points.append(u_value_4)
    u1 = mean(u_value_eq1_points)
    u2 = mean(u_value_eq2_points)
    u3 = mean(u_value_eq3_points)
    u4 = mean(u_value_eq4_points)

    #min,max, temp values of images 
    l = 0
    temp_array = []
    for i in range(len(temperature)):
        single_row = temperature[i]
        l = len(single_row)-1
        for j in range(l):
            temp_array.append(float(single_row[j]))
    #print(len(temp_array))
    data = list([min(temp_array),max(temp_array),mean(temp_array),u1,u2,u3,u4])
    data_of_all_images.append(data)
    
    
#Pushing data into csv

path = os.getcwd()
parent_path = Path(path).parent
os.chdir(parent_path)

print("Images loaded to disk..pushing clustering information to disk")
print("")    
try:
    file = 'Raw_Image_data'
    with open(file + '.csv' , 'a' ,newline='') as csvfile :
        writer = csv.writer(csvfile)
        writer.writerow(['Filename','minimum','maximum','average','U1','U2','U3','U4']) 
        for i in range(0,len(filename)):
            file = filename[i]
            print(file,data_of_all_images[i])
            minimum = data_of_all_images[i][0]
            maximum = data_of_all_images[i][1]
            average = data_of_all_images[i][2]
            U1 = data_of_all_images[i][3]
            U2 = data_of_all_images[i][4]
            U3 = data_of_all_images[i][5]
            U4 = data_of_all_images[i][6]
            writer.writerow([file,minimum,maximum,average,U1,U2,U3,U4])
except FileExistsError:
    os.remove('Raw_Image_data.csv')


    
print("Finished .................")
print(" ")
print(" ")






    
    