import os
from pathlib import Path

import csv
import json
import cv2
from skimage import draw
import numpy as np
import re
not_working = []
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



def start_parsing(image,filename,choice): # choice is the type of annootation
    flag = 0
    #changing into the json directory in data folder
    path = os.getcwd()
    parent_path = Path(path).parent
    os.chdir(parent_path)    
    os.chdir('json')

    x_coordinates, y_coordinates = [0],[0]
    img = image 
    json_filename = filename[:-4] + '.jpg.json'  
    new_coord = []                         # will contain all the coordinate values for the Region of Interst
    temp_image = []                        #will contain the pixel color values for coordinates in new_coord
    with open(json_filename) as json_content:
            json_data = json.load(json_content)
            for entry in json_data['objects']:
                '''
                Window Annotation goes here
                ''' 
                if   choice == 1:
                    #Considering Window annotations
                    if (entry['classTitle'] == 'Window' or entry['classTitle'] == 'Windows'):
                        print("working",filename)
                        x_values = []
                        y_values = []
                        points = entry['points']
                        exterior = points['exterior']
                        for k, coordinates in enumerate(exterior):
                            x_values.append(exterior[k][0])
                            y_values.append(exterior[k][1])
                        if (len(x_values) < 4):
                            print("ERROR: LESS THAN 4 POINTS ANNOTATED FOR WINDOW. NUMBER OF POINTS: {}".format(len(x_values)),filename)
                            x_coordinates, y_coordinates = 0,0
                        else:
                            x_coordinates, y_coordinates = polygon_area_calculation(x_values, y_values)      
                            for i in range(len(x_coordinates)):
                                    x = x_coordinates[i].item()
                                    y = y_coordinates[i].item()
                                    new_coord.append([x,y])
                    else: 
                        flag = -1             
                '''
                Wall Annotation goes here
                '''            
                elif choice == 2 : 
                    if (entry['classTitle'] == 'Facet' or entry['classTitle'] == 'Facade' or entry['classTitle'] == 'Facades'):
                        x_values = []
                        y_values = []
                        points = entry['points']
                        exterior = points['exterior']
                        for k, coordinates in enumerate(exterior):
                            x_values.append(exterior[k][0])
                            y_values.append(exterior[k][1])
                        if (len(x_values) < 4):
                            print("ERROR: LESS THAN 4 POINTS ANNOTATED FOR FACADE. NUMBER OF POINTS: {}".format(len(x_values)),filename)
                        else:
                            x_coordinates, y_coordinates = polygon_area_calculation(x_values, y_values)
                            '''
                            Subtracting window pixels from facade pixels
                            '''
                            #Convert the x and y coordiantes lists into one list of x,y
                            coordinates = []
                            for i in range(len(x_coordinates)):
                                coordinates.append([x_coordinates[i], y_coordinates[i]])
                            #convert list to set
                            coordinate_set = set(tuple(x) for x in coordinates)
                            

                        #Open up the json file again and reread all windows
                        with open(json_filename) as json_file_content:
                            '''
                            Lists that will have coordiantes added to for each object. It should be noted that the coordinates
                            appended to these lists are a cumilitaive of all instances of that object within a picture.
                            This way they can be subtracted from the face coordiantes. 
                            '''
                            window_sets = []
                            door_sets = []
                            hvac_sets = []

                            json_data = json.load(json_file_content)
                            for entry in json_data['objects']:
                                if(entry['classTitle'] == 'Window'):
                                    x_values = []
                                    y_values = []
                                    points = entry['points']
                                    exterior = points['exterior']
                                    for i, coordinates in enumerate(exterior):
                                        x_values.append(exterior[i][0])
                                        y_values.append(exterior[i][1])
                                    if(len(x_values) < 4):
                                        print("ERROR: LESS THAN 4 POINTS ANNOTATED FOR WINDOW. NUMBER OF POINTS: {}".format(len(x_values)))
                                    else:
                                        x_coordinates, y_coordinates = polygon_area_calculation(x_values, y_values)
                                        
                                        #Convert x and y coordinate of windows to sets
                                        for y in range(len(x_coordinates)):
                                            window_sets.append([x_coordinates[y], y_coordinates[y]])

                                if(entry['classTitle'] == 'Door'):
                                    x_values = []
                                    y_values = []
                                    points = entry['points']
                                    exterior = points['exterior']
                                    for i, coordinates in enumerate(exterior):
                                        x_values.append(exterior[i][0])
                                        y_values.append(exterior[i][1])
                                    if(len(x_values) < 4):
                                        print("ERROR: LESS THAN 4 POINTS ANNOTATED FOR DOOR. NUMBER OF POINTS: {}".format(len(x_values)))
                                    else:
                                        x_door_coordinates, y_door_coordinates = polygon_area_calculation(x_values, y_values)
                                        
                                        #Convert x and y coordinate of windows to sets
                                        for y in range(len(x_door_coordinates)):
                                            door_sets.append([x_door_coordinates[y], y_door_coordinates[y]])

                                    
                                if(entry['classTitle'] == 'HVAC'):
                                    x_values = []
                                    y_values = []
                                    points = entry['points']
                                    exterior = points['exterior']
                                    for i, coordinates in enumerate(exterior):
                                        x_values.append(exterior[i][0])
                                        y_values.append(exterior[i][1])
                                    if(len(x_values) < 4):
                                        print("ERROR: LESS THAN 4 POINTS ANNOTATED FOR DOOR. NUMBER OF POINTS: {}".format(len(x_values)))
                                    else:
                                        x_hvac_coordinates, y_hvac_coordinates = polygon_area_calculation(x_values, y_values)
                                        
                                        #Convert x and y coordinate of windows to sets
                                        for y in range(len(x_hvac_coordinates)):
                                            hvac_sets.append([x_hvac_coordinates[y], y_hvac_coordinates[y]])
                    

                        #Converting the list to a set
                        window_sets = set(tuple(x) for x in window_sets)
                        door_sets = set(tuple(x) for x in door_sets)
                        hvac_sets = set(tuple(x) for x in hvac_sets)
                        
                        #Finding difference (set-thory) to extract facade pixels
                        coordinate_set = coordinate_set.difference(window_sets)
                        coordinate_set = coordinate_set.difference(door_sets)
                        coordinate_set = coordinate_set.difference(hvac_sets)       
                    
                    else: 
                        flag = -1
                        '''
                        At this point coordinate_set has only the pixels of the facade. Windows, doors, and hvacs have been subtracted.
                        '''
                        new_coord = list(coordinate_set)
                '''
                Roof Annotation goes here
                ''' 
                elif choice == 3 : 
                    #Considering Roof annotations
                    if (entry['classTitle'] == 'Roof' or entry['classTitle'] == 'Roofs'):
                        print("working",filename)
                        x_values = []
                        y_values = []
                        points = entry['points']
                        exterior = points['exterior']
                        for k, coordinates in enumerate(exterior):
                            x_values.append(exterior[k][0])
                            y_values.append(exterior[k][1])
                        if (len(x_values) < 4):
                            print("ERROR: LESS THAN 4 POINTS ANNOTATED FOR WINDOW. NUMBER OF POINTS: {}".format(len(x_values)),filename)
                            x_coordinates, y_coordinates = 0,0
                        else:
                            x_coordinates, y_coordinates = polygon_area_calculation(x_values, y_values)      
                            for i in range(len(x_coordinates)):
                                    x = x_coordinates[i].item()
                                    y = y_coordinates[i].item()
                                    new_coord.append([x,y])
                    else: 
                        flag = -1
            
            #adding the pixel values for the ROI        
            if flag != -1 :
                try:     
                    for j in new_coord:
                        r ,g,b = img[j[1],j[0]]
                        temp_image.append(list([r,g,b]))  
                                        
                except UnboundLocalError : 
                    print("Annotation not working",filename)
                    print("")   
            else : continue
    return temp_image, new_coord,flag
     
