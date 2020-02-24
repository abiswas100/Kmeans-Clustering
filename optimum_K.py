import os
import multiprocessing

import numpy
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
import pandas
import progressbar


def silhoette(pixel_array):
    for i in range(0,20):
            clusterer = KMeans(n_clusters= i, random_state=10)
    cluster_labels = clusterer.fit_predict(pixel_array)

    # The silhouette_score gives the average value for all the samples.
    # This gives a perspective into the density and separation of the formed
    # clusters
    silhouette_avg = silhouette_score(X, cluster_labels)
    print("For n_clusters =", i,"The average silhouette_score is :", silhouette_avg)   
    
    
    
    pass
print("hello world")
