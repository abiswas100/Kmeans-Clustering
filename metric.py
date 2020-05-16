from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np


def Silhoette_Coeff(pixel_values_of_all_images,filenames):
    print("here")
    for i in range(len(pixel_values_of_all_images)):
        pixel_value = pixel_values_of_all_images[i]
        #filename = filenames[i]
        print(i)
        clusterer = KMeans(n_clusters = 3, n_jobs = -1)
        cluster_labels = clusterer.fit_predict(pixel_value)
        print("hello")
        silhouette_avg = silhouette_score(pixel_value, cluster_labels)
        print("The average silhouette_score is :", silhouette_avg)         
    # The silhouette_score gives the average value for all the samples.
    # This gives a perspective into the density and separation of the formed
    # clusters
       
        
    return 1
    