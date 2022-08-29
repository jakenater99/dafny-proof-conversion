import os

def convert():
    # ask user if they want to convert a file or folder
    while True:
        conversionType = input("Do you want to convert a file or a folder (enter file/folder): ").strip()
        if(conversionType == "file"):
            convertSingleFile()
            break
        if(conversionType == "folder"):
            convertFolder()
            break


def convertSingleFile():
    # entering the file names
    firstfile = input("Enter the name of the file to convert: ")
    secondfile = firstfile.split('.')[0] + "_calc.dfyp"
    assistfile = input("Enter the name of the file to assit the conversion: ")

    # enter the directory to store the conversion
    #directory = input("Enter the name of directory to save the conversion to (enter nothing to be saved in currect directory): ")
    
    # opening first file in append mode and second file in read mode
    f1 = open(firstfile, 'r')
    f2 = open(secondfile, 'a+')
    f3 = open(assistfile, 'r')

    # convert f1 into f2
    convertFile(f1, f2, f3)

    print("The converted file is called " + secondfile)


def convertMultipleFiles(firstfile, folder, assistfile):
    
    secondfile = folder + "\\" + firstfile.split('.')[0].split('\\')[-1] + "_calc.dfyp"

    # opening first file in append mode and second file in read mode
    # opening first file in append mode and second file in read mode
    f1 = open(firstfile, 'r')
    f2 = open(secondfile, 'a+')
    f3 = open(assistfile, 'r')

    # convert f1 into f2
    convertFile(f1, f2, f3)


def convertFile(f1, f2, f3):

    # appending the contents of the second file to the first file
    f2.write("calc == {\n")

    copyNextLine = False
    firstLine = True
    offset = 0
    # read content from first file
    for line in f1:
        
        # count number of whitespaces
        count = 0
        for char in line:
            if(char != " "):
                break
            count += 1 

        # removes all whitespaces from leading and trailing ends
        line = line.strip() + "\n"

        # offset all lines according to the first proof    
        if(line.startswith("proof ") and firstLine is True):
            if(count < 4):
                offset = 4 - count
            if(count > 4):
                offset = count - 4
            firstLine = False

        # copy the next line if the proof stmt is on multiple lines
        if(copyNextLine):
            f2.write(" " * (count + offset) + line)

            # check if proof line has finished
            if(";" in line):
                copyNextLine = False

        # check if line is a proof
        if(line.startswith("proof ")):  
            # append content to second file
            f2.write(" " * (count + offset) + line[6:])

            # check if proof line has finished
            if(";" not in line):
                copyNextLine = True

    f2.write("}")

    # relocating the cursor of the files at the beginning
    f1.seek(0)
    f2.seek(0)

    
    # closing the files
    f1.close()
    f2.close()

def convertFolder():
    # entering the file names
    firstfolder = input("Enter the name of the folder to convert: ")
    secondfolder = firstfolder + "_calc"
    assistfile = input("Enter the name of the file to assit the conversion: ")

    # Check whether the specified path exists or not
    isExist = os.path.exists(secondfolder)

    if not isExist:
    
        # Create a new directory because it does not exist 
        os.makedirs(secondfolder)
        

    # iterate over files in that directory
    for filename in os.listdir(firstfolder):
        f = os.path.join(firstfolder, filename)
        # checking if it is a file
        if os.path.isfile(f):
            convertMultipleFiles(f,secondfolder)
    
    print("The converted folder is called " + firstfolder + "_calc")