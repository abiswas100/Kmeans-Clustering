# Kmeans
Install the Requirements Files 
<ol>
<li>Open-CV</li>
<li>numpy</li>
<li>pandas</li>
<li>psutil</li>
<li>progressbar</li>
<li>re</li>
<li>Scikit-Learn</li>
<li>Scikit-image</li>
<li>matplotlib</li>
<li>psutil</li>
</ol>
<p>
Run the main.py file to perform Clustering and U-value Calculation.</p>
The code in New_Kmeans.py will perform the Clustering and Masking the hotspots in all the images.
The functions in Find_best_cluster finds the pixel_temperature for every image and from that finds min,max and average for each Cluster.
From that it finds the maximum average of all the clusters and masks that cluster with (255,255,255).



The file Optimum-K finds the best number of clusters for a dataset which is currently in progress.
<br>
the file Consider_annotation.py adds annotation into consideration returns image an array with only annotations of all the images
</br>
