import os
from pathlib import Path

import csv
import json
import cv2
from skimage import draw
import numpy as np
import re

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


image_list = []
def start_parsing(image_list,filenames): #json_files , project_name
    #changing into the json directory in data folder
    path = os.getcwd()
    parent_path = Path(path).parent
    os.chdir(parent_path)    
    os.chdir('json')
    i = 0
    for i in range(0,len(filenames)):
        img = image_list[i]
        file = filenames[i]
        json_filename = file[:-4] + '.jpg.json'
        
        draw_window = []
        draw_face = []
        
        with open(json_filename) as json_content:
            json_data = json.load(json_content)
            for entry in json_data['objects']:
                if (entry['classTitle'] == 'Window' or entry['classTitle'] == 'Windows'):
                    x_values = []
                    y_values = []
                    points = entry['points']
                    exterior = points['exterior']
                    for k, coordinates in enumerate(exterior):
                        x_values.append(exterior[k][1])
                        y_values.append(exterior[k][0])
                    if (len(x_values) < 4):
                        print("ERROR: LESS THAN 4 POINTS ANNOTATED FOR WINDOW. NUMBER OF POINTS: {}".format(
                            len(x_values)))
                    else:
                        x_coordinates, y_coordinates = polygon_area_calculation(x_values, y_values)
                        
            temp = []        
            for j in range(len(x_coordinates)):
                # print("{} {}".format(x_coordinates[i], y_coordinates[i]))
                #new_list.append(img[x_coordinates[i][y_coordinates[i]]])
                r ,g,b = img[x_coordinates[j], y_coordinates[j]]
                temp.append(list([r,g,b]))     
            for i in range(0,6): print(temp[i])
            print("") 
            print("Length of temp",len(temp))    
            # #converting into numpy-array
            # new_list = npa = np.asarray(image_list, dtype=np.float32)     
    return image_list
    
        