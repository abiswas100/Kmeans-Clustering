from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

import csv

import getpass
import os
from pathlib import Path
import shutil as s
import time
from multiprocessing import cpu_count
import matplotlib.pyplot as plt
import matplotlib.cm as cm

'''
     The silhouette_score gives the average value for all the samples.
     This gives a perspective into the density and separation of the formed clusters
'''
def Silhoette(pixel_values_of_all_images,filenames):
    print("Computting Silhoette Coefficient ...")
    print("")
    
    # silhouette = []
    for i in range(len(pixel_values_of_all_images)):
        
        pixel_value = pixel_values_of_all_images[i]
     
        # clusterer = KMeans(n_clusters = 3, n_jobs = -1)
        # cluster_labels = clusterer.fit_predict(pixel_value)
        # silhouette_avg = silhouette_score(pixel_value, cluster_labels)
        # print("The average silhouette_score is :", silhouette_avg)         
        
        # silhouette.append(silhouette_avg)
        
        Sum_of_squared_distances = []
        K = range(1,21)
        for k in range(1,21):
            km = KMeans(n_clusters= k ,n_jobs= -1)
            km = km.fit(pixel_value)
            Sum_of_squared_distances.append(km.inertia_)
        
    
    #plot the values
    plt.plot(K, Sum_of_squared_distances, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Sum_of_squared_distances')
    plt.title('Elbow Method For Optimal k')
    plt.show()
    
    path = os.getcwd()
    parent_path = Path(path).parent
    os.chdir(parent_path)
    for files in os.listdir():  
        if files == 'Metric.csv': 
            os.remove('Metric.csv')    
        
    else: 
        file = 'Best-K'
        with open(file + '.csv' , 'a' ,newline='') as csvfile :
            writer = csv.writer(csvfile)
            writer.writerow(['FILENAME','SUM OF SQUARED DISTANCE']) 
            
            for i in range(0,len(filenames)):
                filename = filenames[i]
                for s in Sum_of_squared_distances:
                    writer.writerow([filename,s])
    os.chdir(path)
    return 1
