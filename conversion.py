import os

def convert():
    # ask user if they want to convert a file or folder
    while True:
        # conversionType = input("Do you want to convert a file or a folder (enter file/folder): ").strip()
        firstfile = input("Enter the name of the file/folder to convert: ").strip()
        convertfile = input("Enter the name of the file to assist the conversion: ")
        if "." in firstfile:
            convertSingleFile(firstfile, convertfile)
            break
        else:
            convertFolder(firstfile, convertfile)
            break


def convertSingleFile(firstfile, convertfile):

    secondfile = firstfile.split('.')[0] + "_calc.dfyp"

    # enter the directory to store the conversion
    #directory = input("Enter the name of directory to save the conversion to (enter nothing to be saved in currect directory): ")
    
    # opening first file in append mode and second file in read mode
    f1 = open(firstfile, 'r')
    f2 = open(secondfile, 'a+')
    f3 = open(convertfile, 'r')

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

    #

    # appending the contents of the second file to the first file
    f2.write("// This proves whether the students wp proof is correct\n\n")

    calcBody = False
    prevLine = ""
    prevStatement = ""
    whiteSpaces = 0
    firstProof = True
    elseSkips = 0
    lbraceSkips = 0
    rbraceSkips = 0
    lemmas = []
    # read content from first file
    for line in f3:

        if "lemma" in line.strip():
            lemmas.append(line.replace(" ", "")[5:].split('(')[0])

        hasLemma = False
        for lemma in lemmas:
            if lemma in line.strip():
                hasLemma = True
                break

        if hasLemma:
            f2.write(line)
            continue

        if calcBody and not line.strip().startswith("}"):
            prevLine = line.strip()
            if ";" in line.strip() and "{" not in prevStatement and "}" not in prevStatement and prevStatement.count(";") == 0:
                prevStatement = prevStatement + " \n" + " " * (whiteSpaces + 8) + line.strip()
            else:
                if calcBody:
                    prevStatement = line.strip()
            continue

        if calcBody and line.strip().startswith("}"):
            f2.write(' ' * (whiteSpaces + 4) + prevStatement + "\n")
            prevStatement = ""
            calcBody = False

        if line.strip().startswith("calc == {"):
            f2.write(line)
            calcBody = True

        whiteSpaces = len(line) - len(line.strip()) - 1

        if not calcBody:
            f2.write(line)
        else:
            if firstProof:
                prevLine = "{"
            match = False
            proof = False
            elsesToSkip = elseSkips
            lbracesToSkip = lbraceSkips
            rbracesToSkip = rbraceSkips
            for line in f1:
                if match:
                    if line.strip()[:2] == "//":
                        f2.write(' ' * (whiteSpaces + 4) + line.strip() + "\n")
                        continue

                    if not line.strip().startswith("proof ") and not proof:
                        f1.seek(0)
                        break

                    if line.strip().startswith("proof ") and ";" not in line.strip():
                        f2.write(' ' * (whiteSpaces + 4) + line.strip()[6:] + "\n")
                        proof = True
                        continue

                    if line.strip().startswith("proof ") and ";" in line.strip():
                        f2.write(' ' * (whiteSpaces + 4) + line.strip()[6:] + "\n")
                        if len(line.strip().split(';')) > 1:
                            if "strengthening" in line.strip().split(';')[1].lower():
                                f2.write(' ' * (whiteSpaces) + "==>\n")
                        continue
                       
                    if ";" in line.strip() and proof:
                        f2.write(' ' * (whiteSpaces + 8) + line.strip() + "\n")
                        proof = False
                        if len(line.strip().split(';')) > 1:
                            if "strengthening" in line.strip().split(';')[1].lower():
                                f2.write(' ' * (whiteSpaces) + "==>\n")
                        continue
                    
                    if ";" not in line.strip() and proof:
                        f2.write(' ' * (whiteSpaces + 8) + line.strip() + "\n")
                        continue

                if line.strip().replace(" ", "") == "}else{":
                    if elsesToSkip > 0:
                        elsesToSkip -= 1
                        continue 

                if line.strip().replace(" ", "") == "{":
                    if lbracesToSkip > 0:
                        lbracesToSkip -= 1
                        continue 
                
                if line.strip().replace(" ", "") == "}":
                    if rbracesToSkip > 0:
                        rbracesToSkip -= 1
                        continue
                
                if firstProof:
                    firstProof = False

                if line.strip() == prevLine:
                    if line.strip().replace(" ", "") == "}else{":
                        elseSkips += 1
                    if line.strip().replace(" ", "") == "{":
                        lbraceSkips += 1
                    if line.strip().replace(" ", "") == "}":
                        rbraceSkips += 1
                    match = True

        prevLine = line.strip()

        if ";" in line.strip() and "{" not in prevStatement and "}" not in prevStatement and prevStatement.count(";") == 0:
            prevStatement = prevStatement + " \n" + " " * (whiteSpaces + 8) + line.strip()
        else:
            if calcBody:
                prevStatement = line.strip()

    # relocating the cursor of the files at the beginning
    f1.seek(0)
    f2.seek(0)
    f3.seek(0)
    
    # closing the files
    f1.close()
    f2.close()
    f3.close()

def convertFolder(firstfolder, convertfile):

    secondfolder = firstfolder + "_calc"

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
            convertMultipleFiles(f,secondfolder, convertfile)
    
    print("The converted folder is called " + firstfolder + "_calc")