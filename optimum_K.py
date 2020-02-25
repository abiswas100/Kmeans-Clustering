import os
import multiprocessing

import numpy
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
import pandas
from progressbar import ProgressBar
pbar = ProgressBar()
def silhoette(pixel_array):
    print("Finding Optimum-k")
    for i in pbar(range(0,20)):
            clusterer = KMeans(n_clusters= i, random_state=0)
            cluster_labels = clusterer.fit_predict(pixel_array)

<<<<<<< HEAD

def silhoette(pixel_values):
    pass
=======
            # The silhouette_score gives the average value for all the samples.
            #This gives a perspective into the density and separation of the formed
            # clusters
            silhouette_avg = silhouette_score(pixel_array, cluster_labels)
            print("For n_clusters =", i,"The average silhouette_score is :", silhouette_avg)   
    
            # Compute the silhouette scores for each sample
            sample_silhouette_values = silhouette_samples(pixel_array, cluster_labels)
            print("silhouette score for each sample",sample_silhouette_values)
    pass
>>>>>>> 2285549b962815ed6b1d8bb4f9916e8f97d0dd0e
