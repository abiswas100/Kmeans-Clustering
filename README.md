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
    Run the main.py file to perform Clustering and U-value Calculation.It works as a driver function of the whole model.
    It call functions from the New_Kmeans file .
</p>
<p>
    <b>Find-Best-Cluster</b> finds pixel_temperature using Extract Temperature function , for each image and converts the 3-D temperature array into 1-D Useful temperature array. This array is used to find the <b>U-values,Minimum,Maximum and Average</b> of the total annotated object. It also return the data-of-all-clusters for an image which contains the  <b>U-values,Minimum,Maximum and Average</b> of all the cluster and the hotspot of that corresponding Image.
    
</p>
<p>
    <b>New_Kmeans.py</b> will perform the Clustering and Masking the hotspots in all the images.
        Input Images functions checks the Images folder in the Data folder and inports all the images and there corresponding filenames and stores them in seperate arrays.Then it returns the image list and filenames
        The add annotation call the consider annotations file for each image. Returns the list of coordinates and the pixel-values of the object for all images.  
        The Clustering function takes pixel-values and clusters the object. It returns the labels array for all the images.
        The masking Images function calls the calculate temperature from the find-best-cluster and masks those pixels belonging to the hotspot cluster. 
        The Save-to-file creates a folder called Kmeans-Output and stores all the masked images and then writes the Data into a CSV file.
        U-value function computes the U-values and the min max and Average of the object.
</p>

<p>
    <b>Optimum-K</b> finds the best number of clusters for a dataset which is currently in progress.
</p>

<p>
    <b>Consider_annotation </b> takes in the JSON files and returns pixel-array and the required coordinates of the object in Consideration.
</p>

