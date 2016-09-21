# A couple of methods to get info from the user on what they want to do.


def setNumOfStarterWords():
    while True:
        try:
            numOfStarterWords = int(input("How many word suggestions would you like? "))
            if 0 < numOfStarterWords < 11:
                return numOfStarterWords
            print("Please enter an integer between 1 and 10.")
        except ValueError:
            print("Please enter an integer between 1 and 10.")


def setNumOfLines():
    while True:
        try:
            numOfLines = int(input("How many lines will you write? "))
            if 0 < numOfLines < 101:
                return numOfLines
            print("Please enter an integer between 1 and 100.")
        except ValueError:
            print("Please enter an integer between 1 and 100.")


def setNumOfSyllables():
    while True:
        try:
            numOfSyllables = int(input("How many syllables in each line? "))
            if 0 < numOfSyllables < 21:
                return numOfSyllables
            print("Please enter an integer between 1 and 20.")
        except ValueError:
            print("Please enter an integer between 1 and 20.")

