import optimum_K as op

import os,shutil
import time
from multiprocessing import cpu_count

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import psutil
from progressbar import ProgressBar
from sklearn.cluster import KMeans

image_list = []
filename = []
counter = 0  
os.chdir(r"Museum Clustering Tryouts//images")
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
print("Clustering the image ")

for image in pbar(image_list):
    # reshape the image to a 2D array of pixels and 3 color values (RGB)
    pixel_values = image.reshape((-1, 3))
    # convert to float
    pixel_values = np.float32(pixel_values)
    print(pixel_values)
    print("Length of the pixel value list",len(pixel_values))
    
    #this function will return the best k for each image
    
    # cluster = op.silhoette(pixel_values)
    
    #create an array for the number of clusters
    kmeans = KMeans(n_clusters=1, random_state=0, n_jobs = -1).fit(pixel_values)
    # convert back to 8 bit values
    centers = kmeans.cluster_centers_
    centers = np.uint8(centers)
    print("The centers are ----",centers)
    # flatten the labels array
    labels = kmeans.labels_
    print("The actual labels array",labels)
    print("The labels set",set(labels),"The length of the labels array",len(labels))
    segmented_image = centers[labels]
    segmented_image = segmented_image.reshape(image.shape)
    clustered_images_list.append(segmented_image)

end = time.time()
print("Time consumed in working: ",end - start)


#the labels array contains all the pixel ..it is of size 32780 so we have to interpret the a 1-D labels array 
# as pixels in x,y co-ordinate.






# # disable only the cluster number 2 (turn the pixel into black)
# masked_image = np.copy(image)
# # convert to the shape of a vector of pixel values
# masked_image = masked_image.reshape((-1, 3))
# # color (i.e cluster) to disable
# clusters = [0,1,2,3,4,5]
# #for x in clusters:
# temp = np.array()    #temp array that has the pixel values for a specific cluster
# temp = masked_image[labels == 0]
# # print("\ncluster : ",x )""
# temp=temp.flatten()
# print(len(temp))
# print(temp)

# # convert back to original shape
# for i in clusters:
#     masked_image[labels == i] = [0,0,0]
# masked_image[labels == 2] = [255,255,255]   #hotspot for 12 is cluster 2
# masked_image = masked_image.reshape(image.shape)
# # show the image
# plt.imshow(cv2.cvtColor(masked_image, cv2.COLOR_BGR2RGB))


#Saving the images in output folder
try:
    os.mkdir('kmeans-output')
except FileExistsError:
    print("File already exists so just saving them in that folder")
    folder = 'kmeans-output'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))
    
    print("Removed previous outputs and creating again")
finally:
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