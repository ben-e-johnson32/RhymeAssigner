import os
from datetime import datetime


def Save(userLines, scoreOutput, filename, fileDict, starterWords, numOfSyllables):
    # This method saves the file.

    # Get the path to the directory where we keep the saves.
    cwd = os.getcwd() + "/saves/"

    # If the filename is not already taken, call the WriteFile method.
    if filename not in fileDict.values():
        WriteFile(cwd, filename, scoreOutput, userLines, starterWords, numOfSyllables)

    # If the filename is already taken, ask the user if they want to overwrite that file.
    # If yes, write the file. If no, have them enter another filename and call this method again
    # with the new file name.
    else:
        overwrite = input(filename + ".txt already exists. Would you like to overwrite it? (Y/N) ")
        if str(overwrite).lower() == 'y':
            WriteFile(cwd, filename, scoreOutput, userLines, starterWords, numOfSyllables)
        elif str(overwrite).lower() == 'n':
            fileName = input("Enter another file name: ")
            Save(userLines, scoreOutput, fileName, fileDict, starterWords, numOfSyllables)


def WriteFile(cwd, filename, scoreOutput, userLines, starterWords, numOfSyllables):
    # This method writes the file.

    # Open a new file for writing.
    file = open(cwd + filename + ".txt", 'w')

    # Write each of the user's lines, their score info, and the current date and time to the file.
    file.write("Title: " + filename + "\n\n")
    for line in userLines:
        line += "\n"
        file.write(line)
    file.write(scoreOutput)
    file.write("Starter words: " + ', '.join(starterWords) + "\n")
    file.write("Target number of syllables: " + str(numOfSyllables) + "\n")
    file.write(datetime.now().strftime("%D %r"))
    file.close()
    print("'" + filename + ".txt' saved.")


def Read(filename):
    # This method reads a saved file.

    # Get the path to the saved files directory and open the file.
    cwd = os.getcwd() + "/saves/"

    try:
        file = open(cwd + filename + ".txt", 'r')
    except TypeError:
        print(filename + ".txt not found.")
        return

    # Read the file into a list of its lines and initialize an empty string for output.
    lineList = file.readlines()
    output = ""

    # Loop through the list of lines and add each to the output string, then print the string and close the file.
    for line in lineList:
        output += line
    print("\n" + output + "\n")
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


def ChooseFile(fileDict):
    # This method displays the currently saved files as a numbered menu.
    # It returns the filename of the file chosen by the user.

    # A while loop to print the files in a numbered list.
    x = 0
    while x < len(fileDict):
        print(str(x + 1) + ". " + fileDict[x])
        x += 1

    # The user enters either the number or filename.
    choice = input("Enter the number or the filename: ")
    # Some simple checking to see if the user entered the number or filename. Set a flag.
    try:
        choiceIsInt = True
        choice = int(choice) - 1
    except TypeError:
        choiceIsInt = False
    except ValueError:
        choiceIsInt = False

    # If the choice is either a key (integer file index) or value (string filename),
    # read the file.
    if choice in list(fileDict.keys()) or choice in list(fileDict.values()):
        if choiceIsInt:
            filename = fileDict[choice]
        else:
            filename = choice

        return filename


def Delete(filename):
    # This method deletes a file from the /saves/ directory.

    warning = input("Are you sure you want to delete '" + filename + ".txt'? (Y/N): ").lower()
    if warning == 'y':
        cwd = os.getcwd() + "/saves/"
        os.remove(cwd + filename + '.txt')
        print("'" + filename + ".txt' deleted.")
    else:
        return


def UpdateHighScores(filename, score):
    if filename == 0:
        filename = "x"
        score = "0"
    cwd = os.getcwd()
    file = open(cwd + "/high_scores.txt", "r")
    lines = file.readlines()
    highScoresDict = {}

    # Read through the file and add each title and score to the scores dict.
    x = 0
    while x < len(lines):
        title = lines[x]
        score2 = lines[x + 1]
        highScoresDict.update({title: score2})
        x += 2

    # Also add the score and title that were just written to the high scores dict.
    highScoresDict.update({filename + "\n": score + "\n"})

    # A pretty wonky way of sorting the scores. Build a list of just the scores, then
    # strip their newline character and convert them to ints so it can be sorted properly.
    highScoresListTitles = []
    highScoresListScores = list(highScoresDict.values())
    highScoresListScoresInt = []
    for x in range(len(highScoresListScores)):
        highScoresListScoresInt.append(int(highScoresListScores[x].rstrip("\n")))
    highScoresListScoresInt.sort()
    highScoresListScoresInt.reverse()

    # Then, starting with the highest score, re-find the title associated with that score.
    for score in highScoresListScoresInt:
        for t, s in highScoresDict.items():
            if s == str(score) + "\n":
                # If there's a match, add the title and update the dict, effectively removing
                # the added title's score. That way, if two files have the same score, they won't
                # both be added twice.
                highScoresListTitles.append(t)
                highScoresDict[t] = -1

    file.close()
    file = open(cwd + "/high_scores.txt", "w")

    # If the list is full, there are 10 scores.
    if len(lines) / 2 >= 10:
        highScores = 10
    # If there aren't any scores in the list yet, we only have the new entry.
    elif len(lines) < 2:
        highScores = 1
    # If it's partially full, halve the number of lines and add one for the new entry.
    else:
        highScores = len(lines) / 2 + 1

    # Rewrite the file two lines at a time.
    x = 0
    while x < highScores:
        title = highScoresListTitles[x]
        score = str(highScoresListScoresInt[x]) + "\n"
        file.write(title + score)
        x += 1

    file.close()
