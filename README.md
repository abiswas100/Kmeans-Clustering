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
    <b>Find-Best-Cluster</b>finds pixel_temperature for each image and converts a 3-D temperature array into 1-D Useful temperature array. This array is used to find the <b>U-values,Minimum,Maximum and Average</b> of the total annotated object. It also return the data-of-all-clusters for an image which contains the  
</p>
<p>
    <b>New_Kmeans.py</b> will perform the Clustering and Masking the hotspots in all the images.
        The functions in 
        From that it finds the maximum average of all the clusters and masks that cluster with (255,255,255).
</p>

<p>
    <b>Optimum-K</b> finds the best number of clusters for a dataset which is currently in progress.
</p>

<p>
    <b>Consider_annotation </b> takes in the JSON files and returns pixel-array and the required coordinates of the object in Consideration.
</p>

