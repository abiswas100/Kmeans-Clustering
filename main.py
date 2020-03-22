import New_Kmeans as Kmeans

import os
from pathlib import Path
import psutil
import time
from multiprocessing import cpu_count


def main():
    start = time.time()
    '''
    Inputting Images
    '''
    image_list,filenames = Kmeans.input_images()

    '''
    Getting Annotations from Consider_Annotations function
    '''
    coordinates_of_all_images,pixel_values_of_all_images = Kmeans.add_annotation(image_list,filenames)
    
    # Restricting python to use only 2 cores
    # cpu_nums = list(range(psutil.cpu_count()))
    # proc = psutil.Process(os.getpid())
    # proc.cpu_affinity(cpu_nums[:-2])                                              #will use all CPU cores uncomment to use 2 cores     
    print("CPUS being consumed..",cpu_count())
    
    '''
    Getting U-values for images 
    '''
    Kmeans.U_value(coordinates_of_all_images,filenames)

    '''
    Cluster Images
    '''
    labels_of_all_image,clustered_images_list = Kmeans.clustering(image_list,pixel_values_of_all_images,filenames)
    
    '''
    Masking Hotspot Clusters in the Image
    '''
    masked_image_list,best_cluster_of_all_image ,data_of_all_images ,density_of_all_image = Kmeans.masking_image(filenames,image_list,labels_of_all_image,coordinates_of_all_images,clustered_images_list)
    
    '''
    Saving Data in CSVs and pushing images into folder
    '''
    Kmeans.save_to_file(filenames,masked_image_list,data_of_all_images,density_of_all_image,best_cluster_of_all_image) # Saves all the data to Kmeans-output folder and stores data in a CSV

    end = time.time()
    print("Time consumed: ",end - start)
    print("Finished .................")
    print(" ")
    return 1

if __name__== "__main__":
    main()

