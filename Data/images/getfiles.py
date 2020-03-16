import os
import shutil
image_list = []
filenames = []
counter = 0
for files in os.listdir():
    if(files.endswith('.jpg')):
        filenames.append(files)

#get csvs
os.chdir('../csv')
print(os.getcwd())
mcsv = []
path = '../images'
for file in filenames:
    csv_filename = file[:-4] + '.csv'
    if os.path.exists(csv_filename):
        os.chdir('../csv')
        shutil.copy(csv_filename, path)
    else:mcsv.append(csv_filename)
print(mcsv)    

# get json
os.chdir('../json')
print(os.getcwd())
mjson = []
path = '../images'
for file in filenames:
    csv_filename = file[:-4] + '.jpg.json'
    if os.path.exists(csv_filename):
        os.chdir('../json')
        shutil.copy(csv_filename, path)
    else:
        mjson.append(csv_filename)
print(mjson)   