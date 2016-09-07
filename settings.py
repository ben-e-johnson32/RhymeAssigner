# A couple of methods to get info from the user on what they want to do.
# TODO: Add timed mode? Add all input to one module?


def setNumOfStarterWords():
    numOfStarterWords = int(input("How many word suggestions would you like? "))
    return numOfStarterWords


def setNumOfLines():
    numOfLines = int(input("How many lines will you write? "))
    return numOfLines


def setNumOfSyllables():
    numOfSyllables = int(input("How many syllables in each line? "))
    return numOfSyllables
