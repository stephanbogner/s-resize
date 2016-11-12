# ----------------------------------------------------------------------------------
# | Settings
# ----------------------------------------------------------------------------------


folderToMinimize = "$originals" #this is the folder's name in which hi-res images have to be placed
compressionQuality = 85 #level of image compression (in percent) (e.g. Google uses this)
convertNonTransparentImages = True #whether pngs/gifs which are not transparent should be converted and ... (Note: Only checks the alpha channel meta tag of the file)
convertNonTransparentImagesTo = "jpg" # ... into which file format
defaultPreset = "@default"
sizePresets = { #options for resizing
    "@default": {   "width": 800    },
    "@cover": {     "width": 1200,    
                    "prefix": "_"},
    "@thumb": {     "width": 128,  
                    "overwrite": "thumb"},
    "@small": {     "width": 400    },
    "@full": {      "width": 2880,
                    "suffix": "_fullscreen" },
    "@large": {     "width": 2000   },
    "@zoomable": {  "width": 2440,
                    "suffix": "_zoomable"   }
}

fileTypesToResize = ["gif", "jpg", "jpeg", "png", "tiff", "webp"]


# ----------------------------------------------------------------------------------
# | Code
# ----------------------------------------------------------------------------------


import os
import string
from PIL import Image
from collections import defaultdict

def getHeight(currentWidth, currentHeight, targetWidth):
    widthPercent = (targetWidth / float(currentWidth))
    return int((float(currentHeight)*float(widthPercent)))

print
print
print
print ("----------------------------------------")
print (" Start")
print ("----------------------------------------")

rootDir = '.' # Set the directory you want to start from
for dirName, subdirList, fileList in os.walk(rootDir):
    print
    print (dirName)
    for fileName in fileList:
        #fullPath = os.path.abspath( dirName + "/"+ fileName) #path to file including filename
        relativePathToFile = dirName + "/"+ fileName
        basename = os.path.basename(dirName) #current folder

        if basename == folderToMinimize: #images of current folder should be minified
            fileNameSplitByPeriod = fileName.split(".") #image.jpg -> ['image', 'jpg']
            extension = fileNameSplitByPeriod[len(fileNameSplitByPeriod)-1].lower() # image.jpg ->  'jpg'
            fileNameWithoutExtension = fileNameSplitByPeriod[len(fileNameSplitByPeriod)-2] # image.jpg ->  'image'

            if extension in fileTypesToResize:
                print("   - [" + fileName + "]")
                
                parentDirectory = os.path.abspath(os.path.join(dirName, os.pardir))

                fileNameWithoutExtensionAndResizeInformation = fileNameWithoutExtension
                for key in sizePresets:
                    fileNameWithoutExtensionAndResizeInformation = string.replace(fileNameWithoutExtensionAndResizeInformation, key, '') #remove size information from string

                if fileNameWithoutExtensionAndResizeInformation == fileNameWithoutExtension:
                    width = sizePresets[defaultPreset]['width']
                    img = Image.open(relativePathToFile)
                    height = getHeight(img.size[0], img.size[1], width)
                    exportFileName = fileNameWithoutExtension + "." + extension
                    print ("         Use default - " + defaultPreset.ljust(25) + (" ["  + str(width) + "x" + str(height) + "]").ljust(25) + " -> " + exportFileName)
                    imaged = img.resize((width, height), Image.ANTIALIAS)
                    imaged.save(parentDirectory + "/"+ exportFileName, quality = compressionQuality)
                else:
                    for key in sizePresets:
                        if key in fileNameWithoutExtension:

                            exportFileName = ""
                            if 'overwrite' in sizePresets[key]:
                                exportFileName = sizePresets[key]['overwrite']
                            else:
                                #Part 1: Prefix (if set)
                                if 'prefix' in sizePresets[key]:
                                    exportFileName += sizePresets[key]['prefix']

                                #Part 2: Main Name
                                exportFileName += fileNameWithoutExtensionAndResizeInformation

                                # Part 3: Suffix (if set)
                                if 'suffix' in sizePresets[key]:
                                    exportFileName += sizePresets[key]['suffix']

                            

                            width = sizePresets[key]['width']
                            img = Image.open(relativePathToFile)
                            if convertNonTransparentImages and img.mode != "RGBA" or "transparency" in img.info:
                                extension = convertNonTransparentImagesTo
                                # print ("         Non-transparent image -> Convert to " + convertNonTransparentImagesTo)

                            # Part 4: Adding extension
                            exportFileName += "." + extension

                            height = getHeight(img.size[0], img.size[1], width)
                            print ("         " + key.ljust(25) + (" ["  + str(width) + "x" + str(height) + "]").ljust(25) + " -> " + exportFileName)
                            imaged = img.resize((width, height), Image.ANTIALIAS)
                            imaged.save(parentDirectory + "/"+ exportFileName, quality = compressionQuality)
            else:
                print("   - [" + fileName + "] no image (ignoring)")
print
print ("----------------------------------------")
print (" All done - glad I could help :)")
print ("----------------------------------------")
print
print
print