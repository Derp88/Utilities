#Simple little tool to compare file names in different directorys to see which ones are unique or matching
import os

#Write unique files to file
writeOutput = True

#Delete duplicate files in dir 2
deleteDupesDir2 = False

#Put directory paths here
dir1 = "C://example//dir//here//1"
dir2 = "C://example//dir//here//2"

#Get file contents in a list
dir1List = os.listdir(dir1)
dir2List = os.listdir(dir2)

#Lists that store the file names that are unique to said directory
uniqueDir1List = []
uniqueDir2List = []
matchingList = []

#Find uniques for dir 1
for fileName in dir1List:
    if fileName not in dir2List:
        uniqueDir1List.append(fileName)
    else:
        matchingList.append(fileName)

#Find uniques for dir 2
for fileName in dir2List:
    if fileName not in dir1List:
        uniqueDir2List.append(fileName)

#Output
print("The first directory has unique files: " + str(uniqueDir1List))
print("The second directory has unique files: " + str(uniqueDir2List))
print("They both contain: " + str(matchingList))

#Write unique file names to text files
if(writeOutput):
    with open("uniqueDir1.txt", "w") as dir1File:
        for fileName in uniqueDir1List:
            dir1File.write(fileName + "\n")
    with open("uniqueDir2.txt", "w") as dir2File:
        for fileName in uniqueDir2List:
            dir2File.write(fileName + "\n")
    with open("matching.txt", "w") as matchingFile:
        for fileName in matchingList:
            matchingFile.write(fileName + "\n")

#Optional functionality to delete duplicate files in dir 2
if(deleteDupesDir2):
    for fileName in matchingList:
        #Sanity check to make sure the file actually exists. (It really should, we found it!)
        deletePath = os.path.join(dir2, fileName)
        if os.path.exists(deletePath):
            print("Deleting: " + deletePath)
            os.remove(deletePath)
        else:
            print("Error: The file " + deletePath + " does not exist!")

