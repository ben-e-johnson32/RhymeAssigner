import requests
import dictionary
import settings
import scoring
import files


##################################################################################################
# This program provides a number of starter words for a user, who then attempts to rhyme with    #
# those words as much as possible in a poem or song lyrics. Then, the program scores the user's  #
# work using RhymeBrain's rhyme score function. - Ben Johnson                                    #
##################################################################################################


def main():
    # The menu for the program. The whole program is in a while loop that only breaks when the user enters
    # 'x' when given the option.
    choices = "Enter 'w' to write, 'r' to read a previous entry, 'd' to delete a previous entry, or 'x' to quit: "
    x = 0
    while True:
        # Get a dictionary of the saved files. They have an integer as the key and the filename as the value.
        fileDict = files.GetFileDict()

        # If this is the first iteration of the loop, display a greeting. If not, just display the choices.
        if x == 0:
            mainMenuChoice = input("Welcome to Rhyme Assigner! " + choices).lower()
        else:
            mainMenuChoice = input(choices).lower()

        # The user enters 'w', choosing write mode.
        if mainMenuChoice == 'w':
            # Get the number of random words to find, then get them using the dictionary module.
            numOfStarterWords = settings.setNumOfStarterWords()
            numOfLines = settings.setNumOfLines()
            numOfSyllables = settings.setNumOfSyllables()
            starterWords = dictionary.GetStarterWords(numOfStarterWords)

            possibleRhymes = {}         # Initialize a dictionary for all the possible rhymes and their scores.

            # Fill the dictionary of possible rhymes.
            possibleRhymes = GetPossibleRhymes(numOfStarterWords, possibleRhymes, starterWords)

            # Display the starter words and all the possible rhymes to make sure it's working. (just for testing)
            print(starterWords)
            print(possibleRhymes)

            # The user enters their lines.
            userLines = GetLines(numOfLines)

            # Score the line and return the results as a string.
            scoreOutput = scoring.GetScore(userLines, possibleRhymes, numOfSyllables)
            print(scoreOutput)

            # Ask the user if they want to save their entry, or just go back to the menu.
            keepGoing = input("Enter 's' to save this entry, or 'm' to go back to the main menu: ")

            # Save the file.
            if keepGoing == 's':
                fileName = input("Enter a file name: ")
                files.Save(userLines, scoreOutput, fileName, fileDict)

            # If they don't want to save, go back to the top of the loop.
            else:
                continue

        # The user enters r, choosing read mode.
        elif mainMenuChoice == 'r':
            print("Choose a file: ")

            # Display a list of the saved files by looping through the dictionary of files.
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

            # If the choice is either a key (integer file index) or value (string filename),
            # read the file.
            if choice in list(fileDict.keys()) or choice in list(fileDict.values()):
                if choiceIsInt:
                    filename = fileDict[choice]
                else:
                    filename = choice
                print()
                files.Read(filename)

        # TODO: An option to delete previous entries.
        elif mainMenuChoice == 'd':
            print("Choose a file to delete: ")

            x = 0
            while x < len(fileDict):
                print(str(x + 1) + ". " + fileDict[x])
                x += 1

        # Entering 'x' when prompted will break the loop, thus ending the program.
        elif mainMenuChoice == 'x':
            break

        x += 1


def GetPossibleRhymes(numOfStarterWords, possibleRhymes, starterWords):
    # A for loop that will grab all possible rhymes for the starter words and put them
    # into the possibleRhymes dictionary.
    for num in range(numOfStarterWords):
        targetURL = "http://rhymebrain.com/talk?function=getRhymes&word="
        targetURL += starterWords[num]
        response = requests.get(targetURL).json()
        for entry in response:
            if entry['score'] >= 192:   # Only take a result if its score is reasonably high.
                entry = {entry['word']: entry['score']}   # Take the word and its score.
                possibleRhymes.update(entry)
    return possibleRhymes


def GetLines(numOfLines):
    # The method that takes user input. Uses a while loop to take lines from the user and put them into a list,
    # then returns that list of lines.
    lines = []

    print("Enter " + str(numOfLines) + " lines, pressing enter after each.\n")
    x = 0
    while x < numOfLines:
        line = input()
        lines.append(line)
        x += 1

    return lines


main()
