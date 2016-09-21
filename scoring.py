import string
import sqlite3 as lite
import os


def GetScore(userLines, possibleRhymes, numOfSyllables):
    rhymeScore = 0
    syllableScore = 0

    # Basic prototype of the scoring.
    # Format each line to remove punctuation and make it lowercase. Then split it into a list of words.
    for line in userLines:
        for c in string.punctuation:
            line = line.replace(c, "")
        line = line.lower()
        words = line.split()

        # If a user's word is also in the list of possible rhymes, add that word's score to the rhyme score.
        for word, score in possibleRhymes.items():
            if word in words:
                rhymeScore += score
        # Calculate the syllable score for the line and add it to the syllable score.
        lineScore = CalculateSyllableScore(words, numOfSyllables)
        syllableScore += lineScore

    output = [""]

    # If the total score makes the top ten, add a message.
    if (rhymeScore + syllableScore) > GetLowHighScore():
        output[0] = "\nHigh score!"

    # A string showing score info.
    output[0] += "\nRhyme score: " + str(rhymeScore) + "\nSyllable Score: " + str(syllableScore) + \
                 "\nTotal Score: " + str(rhymeScore + syllableScore) + "\n"

    # Also return the int value of the score.
    output.append(str(rhymeScore + syllableScore))

    return output


def CalculateSyllableScore(words, numOfSyllables):
    # Get the number of syllables in the line.
    countInLine = SyllablesInLine(words)

    # Give a score based on how close the number of syllables is to the target number.
    if countInLine == numOfSyllables:
        score = 100
    elif countInLine in range(numOfSyllables - 1, numOfSyllables + 2):
        score = 75
    elif countInLine in range(numOfSyllables - 2, numOfSyllables + 3):
        score = 50
    elif countInLine in range(numOfSyllables - 3, numOfSyllables + 4):
        score = 25
    else:
        score = 0

    return score


def SyllablesInLine(words):
    # A method to look up the number of syllables in a line.
    connection = lite.connect("syllables.db")
    cursor = connection.cursor()

    total = 0

    # Loop through each word in the list and look it up in the syllables database.
    # If the word's not in the database, an IndexError exception is caught, and the word
    # is sent to the primitive syllable counter.
    for word in words:
        try:
            cursor.execute("SELECT syllables FROM syllables WHERE word=?", (word,))
            count = cursor.fetchall()[0]
            total += count[0]
        except IndexError:
            total += PrimitiveSyllableCount(word)

    connection.close()
    return total


def PrimitiveSyllableCount(word):
    # A method to count the syllables in a word. Doesn't work great, but shouldn't be applied often.
    # Most of this was taken from this stackoverflow question:
    # http://stackoverflow.com/questions/14541303/count-the-number-of-syllables-in-a-word
    count = 0
    vowels = 'aeiouy'
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith('e'):
        count -= 1
    if word.endswith('ed'):
        count -= 1
    if word.endswith('le'):
        count += 1
    if word.endswith('ism'):
        count += 1
    if "ia" in word:
        count += 1
    if "ua" in word:
        count += 1
    if "io" in word:
        count += 1
    if count <= 0:
        count = 1
    return count


def GetLowHighScore():
    # This method finds the lowest score on the high scores list.
    cwd = os.getcwd()
    file = open(cwd + "/high_scores.txt", "r")
    lines = file.readlines()
    file.close()

    # If there aren't 10 high scores yet, return 0.
    if len(lines) < 20:
        return 0

    # The lowest score on the list will be the last line of the file.
    lowHighScore = int(lines[len(lines) - 1].rstrip("\n"))
    return lowHighScore


def DisplayHighScores(fileDict):
    # Open the high scores file and read its lines into a list.
    cwd = os.getcwd()
    file = open(cwd + "/high_scores.txt", "r")
    lines = file.readlines()
    file.close()
    highScoresDict = {}

    # A loop with 2 counters. Fills the high scores dictionary from the lines of the file.
    y = 0
    x = 0
    while x < len(lines):
        filename = lines[x][:-1]
        score = lines[x + 1].rstrip("\n")
        entry = {y: [filename, score]}
        highScoresDict.update(entry)
        x += 2
        y += 1

    # A loop that prints the titles and scores of all high score entries in a numbered list.
    x = 0
    while x < len(highScoresDict):
        print(str(x + 1) + ". " + highScoresDict[x][0] + " - " + highScoresDict[x][1])
        x += 1

    # Have the user enter either the filename or the number on the list.
    choice = input("Enter the number or the filename: ")

    # Figure out whether they chose the number or the string, set a flag.
    try:
        choiceIsInt = True
        choice = int(choice) - 1
    except TypeError:
        choiceIsInt = False
    except ValueError:
        choiceIsInt = False

    # If the choice is a key in the high scores dictionary or a value in the file dictionary,
    # set the filename. If we know it to be an int, set it based on the high scores dictionary.
    # Otherwise it's a string - the filename itself.
    filename = ""
    if choice in highScoresDict.keys() or choice in GetHighScoreFilenames():
        if choiceIsInt:
            filename = highScoresDict[choice][0]
        else:
            filename = choice

    return filename


def GetHighScoreFilenames():

    cwd = os.getcwd()
    file = open(cwd + "/high_scores.txt", "r")
    lines = file.readlines()
    file.close()
    highScoreFilenames = []

    x = 0
    while x < len(lines):
        if x % 2 == 0:
            highScoreFilenames.append(lines[x][:-1])
        x += 2

    return highScoreFilenames
