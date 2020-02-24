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

temperature = extract_temperature()

 
def calculate_temperature(image,labels):
     
 # ##########################################
        #    Find Average Temperature
# ##########################################
    os.chdir(r"Museum Clustering Tryouts//csv")
    clusters = [0,1,2,3,4,5];
    masked_image = np.copy(image)
    # convert to the shape of a vector of pixel values
    masked_image = masked_image.reshape((-1, 3))

    for i in clusters:
        temp = np.where(labels==i)
        print("temp:", temp)

    