import os
import time
import csv
import cv2
import numpy as np
import pandas as pd
import psutil
import matplotlib.pyplot as plt
from multiprocessing import cpu_count
from progressbar import ProgressBar
from sklearn.cluster import KMeans

image_list = []
filename = []
counter = 0  
os.chdir(r"D:\UND\GCSP\Project_Files\Kmeans\Museum Clustering Tryouts\images")
for files in os.listdir():
    if(files.endswith('.jpg')):
        if(counter == 0):   # to input all the image just remove the conditional statements and use the below 4 lines
            img = cv2.imread(str(files))
            image_list.append(img)
            filename.append(files)
            print("All Images loaded into array")
            counter = counter+1
        else:            
            break

#Restricting python to use only 2 cores
cpu_nums = list(range(psutil.cpu_count()))
proc = psutil.Process(os.getpid())
proc.cpu_affinity(cpu_nums[:2])
print("CPUS being consumed..",cpu_count())


pbar = ProgressBar()
start = time.time()
clustered_images_list = [] #list containing all the clustered outputs
 # Running 6 clusters on each image of Museum
 # For Twamley keep cluster above 10 
print("")
print("Clustering the dataset in into ")
for image in pbar(image_list):
    # reshape the image to a 2D array of pixels and 3 color values (RGB)
    pixel_values = image.reshape((-1, 3))
    # convert to float
    pixel_values = np.float32(pixel_values)
    print(pixel_values)
    print("Length of the pixel value list",len(pixel_values))
    #create an array for the number of clusters
    kmeans = KMeans(n_clusters=6, random_state=0, n_jobs = -1).fit(pixel_values)
    # convert back to 8 bit values
    centers = kmeans.cluster_centers_
    centers = np.uint8(centers)
    print(centers)
    # flatten the labels array
    labels = kmeans.labels_
    print("The actual labels array",labels)
    print("The labels set",set(labels),"The length of the labels array",len(labels))
    segmented_image = centers[labels]
    segmented_image = segmented_image.reshape(image.shape)
    clustered_images_list.append(segmented_image)

end = time.time()
print("Time consumed in working: ",end - start)
##########################################
#           Find Average Temperature
##########################################
bool_matrix = np.zeros(len(labels))
print(len(labels))
clusters = [0,1,2,3,4,5];
masked_image = np.copy(image)
# convert to the shape of a vector of pixel values
masked_image = masked_image.reshape((-1, 3))
for i in clusters:
    #check each index for every label
        masked_image[labels == i] 
        print(i)
#masked_image[labels == 2] = [255,255,255]
masked_image = masked_image.reshape(image.shape)





############################################
#the labels array contains all the pixel ..it is of size 32780 so we have to interpret the a 1-D labels array 
# as pixels in x,y co-ordinate.

#Saving the images in output folder

try:
    os.mkdir('kmeans-output')
except FileExistsError:
    print("File already exists so just saving them in that folder")
    os.removedirs('Kmeans-output')
    os.mkdir('kmeans-output')
    print("")
print("Pushing clustered images to disk..............")    
os.chdir('kmeans-output')
counter = 0
for img in clustered_images_list:
    # show the image
    #plt.imshow(cv2.cvtColor(segmented_image, cv2.COLOR_BGR2RGB))
    #cv2.imwrite(str(counter) + '.jpg', img)
    cv2.imwrite(filename[0], img)
    counter = counter + 1
print("Finished .................")


def extract_temperature(csv_filename):
    '''
    Function will extract all of the temperatures within a csv file into a 2D list of lenth [512][640].
    The temperature values should be in celisus and the 2D list cannot be any smaller than this.
    :param csv_filename: CSV filename you you are trying to parse
    :param dir_path: Parent directory to OGI_u_value_module project
    :param csv_file_path: CSV filepath extension
    :return: List containing [512][640] = 327680 data points
    '''
    with open(csv_filename) as csv_file:

        csv_file_content = csv.reader(csv_file, delimiter=',', quotechar='|')
        pixel_temperature = []
        for i, data in enumerate(csv_file_content):
            length = len(data)
            if(length == 0):
                continue
            if(i <= 8):
                pixel_temperature.append(data[0:])
    return pixel_temperature