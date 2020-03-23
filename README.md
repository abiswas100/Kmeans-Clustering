# Kmeans-Clustering 
Install the Requirements Modules 
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
    Run the main.py file to perform Clustering and U-value Calculation.
</p>

<p>
    <b>New_Kmeans.py</b> will perform the Clustering and Masking the hotspots in all the images.
    The functions in Find_best_cluster finds the pixel_temperature for every image and from that finds min,max and average for each Cluster.
    From that it finds the maximum average of all the clusters and masks that cluster with (255,255,255).
</p>

<p>
    <b>Optimum-K</b> finds the best number of clusters for a dataset which is currently in progress.
</p>

<p>
<b>Consider_annotation </b> adds annotation into consideration returns image an array with only annotations of all the images
</p>

