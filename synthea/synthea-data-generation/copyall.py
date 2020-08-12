import os
path = "/nvme1/synthea/output/"
os.chdir(path)
foldernames = os.listdir("csv")
filepathtemp="/nvme1/synthea/output/csv/" + str(foldernames[0])
filenames = os.listdir(filepathtemp)
#for each folder
#create local files that needs to be called as final files under folder FINAL
print("Creating a final Folder")
os.mkdir("Final")
print("Creating Final File names in Final Folder")
for files in filenames:
    with open(path+"Final/"+str(files), 'w') as fp: 
        pass



#for each filename
for filesnamescounter in filenames:
    print("Merging for {}".format(filesnamescounter))
#Open the file      
    fout = open("Final/"+ str(filesnamescounter),"a")
# Copy file from first folder only (with headers)
    for line in open("/nvme1/synthea/output/csv/" + str(foldernames[0])+ "/" + str(filesnamescounter)):
        fout.write(line)
# now append the files from rest of the folders
    for folders in foldernames[1:]:
        f = open("/nvme1/synthea/output/csv/"+str(folders)+"/"+str(filesnamescounter))
#skip header
        f.__next__()
        for line in f:
            fout.write(line)
        f.close()
    fout.close()
    

