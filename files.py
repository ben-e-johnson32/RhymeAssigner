import os
from datetime import datetime


def Save(userLines, scoreOutput, filename, fileDict):
    # This method saves the file.

    # Get the path to the directory where we keep the saves.
    cwd = os.getcwd() + "/saves/"

    # If the filename is not already taken, call the WriteFile method.
    if filename not in fileDict.values():
        WriteFile(cwd, filename, scoreOutput, userLines)

    # If the filename is already taken, ask the user if they want to overwrite that file.
    # If yes, write the file. If no, have them enter another filename and call this method again
    # with the new file name.
    else:
        overwrite = input(filename + ".txt already exists. Would you like to overwrite it? (Y/N) ")
        if str(overwrite).lower() == 'y':
            WriteFile(cwd, filename, scoreOutput, userLines)
        elif str(overwrite).lower() == 'n':
            fileName = input("Enter another file name: ")
            Save(userLines, scoreOutput, fileName, fileDict)


def WriteFile(cwd, filename, scoreOutput, userLines):
    # This method writes the file.

    # Open a new file for writing.
    file = open(cwd + filename + ".txt", 'w')

    # Write each of the user's lines, their score info, and the current date and time to the file.
    # TODO: Add the starter words and chosen settings to the file.
    for line in userLines:
        line += "\n"
        file.write(line)
    file.write(scoreOutput)
    file.write(GetTimeAndDate())
    file.close()


def GetTimeAndDate():
    # This method gets the current date and time and returns it as a string to add to a saved file.

    # Use datetime to make a datetime object.
    d = datetime.now()
    # Copy the hour since the object isn't writable.
    hour = d.hour

    # Convert 24 hour clock to AM/PM
    if hour > 11:
        timeSuffix = "PM"
    else:
        timeSuffix = "AM"
    if hour > 12:
        hour -= 12
    elif hour == 0:
        hour = 12

    # Build the output string. zfill makes a number always the specified number of digits, so 4:03 won't be 4:3.
    timeAndDateString = str(d.month) + "/" + str(d.day) + "/" + str(d.year) + " " + \
                        str(hour) + ":" + str(d.minute).zfill(2) + " " + timeSuffix + "\n"
    return timeAndDateString


def Read(filename):
    # This method reads a saved file.

    # Get the path to the saved files directory and open the file.
    cwd = os.getcwd() + "/saves/"
    file = open(cwd + filename + ".txt", 'r')

    # Read the file into a list of its lines and initialize an empty string for output.
    lineList = file.readlines()
    output = ""

    # Loop through the list of lines and add each to the output string, then print the string and close the file.
    # TODO: Add the filename (without extension) to the output - label as Title.
    for line in lineList:
        output += line
    print(output)
    file.close()


def GetFileDict():
    fileDict = {}

    # I took the first line of this for loop from the first answer to this question on stack overflow:
    # http://stackoverflow.com/questions/18262293/python-open-every-file-in-a-folder
    index = 0
    for file in os.listdir(os.getcwd() + "/saves/"):
        # If it's a text file, add its name to the list. All files saved with files.Save are .txt files,
        # and all other files in this project's directory
        fileName = file[:-4]
        dictEntry = {index: fileName}
        fileDict.update(dictEntry)
        index += 1

    return fileDict
