import random
# import requests
import os

# TODO: Make this part faster? Takes a couple seconds.


def GetStarterWords(numberOfWords):

    # Open the dictionary file twice. I assume this isn't necessary.
    # TODO: Find a way to only open the dictionary file once.
    cwd = os.getcwd()
    dictFile = open(cwd + "/words", 'r')
    dictFile2 = open(cwd + "/words", 'r')

    # Two empty lists - one for the output list of starter words, and one for the
    # random line numbers to take from the dictionary file.
    starterWords = []
    lineNumbers = []

    # Find the number of lines in the file.
    # TODO: Hard-code this to avoid looping through hundreds of thousands of lines twice?
    lineCount = len(dictFile.readlines())

    # Fill the list of random line numbers to take from the file.
    for x in range(numberOfWords):
        lineNumbers.append(random.randint(0, lineCount))

    # Loop through the file - if the line number is in the lineNumbers list,
    # and the word is relatively short (makes for better rhyme results and fewer
    # strange, rarely-used words), add it to the starterWords list. If the word is
    # too long, keep checking the next line until you find one short enough.
    # TODO: Find a way to further limit weird words.
    for line in range(lineCount):
        word = dictFile2.readline()
        word = word.strip('\n')
        if line in lineNumbers:
            if len(word) < 5:
                starterWords.append(word)
                lineNumbers.remove(line)
                if len(lineNumbers) == 0:
                    break
            else:
                lineNumbers.remove(line)
                lineNumbers.append(line + 1)

    # While loop with a counter that strips the newline from each word.
    b = 0
    while b < len(starterWords):
        starterWords[b] = starterWords[b].strip('\n')
        b += 1

    # Close the files and return the list of starter words.
    dictFile.close()
    dictFile2.close()
    return starterWords


# def CheckFrequency(word):
#     headers = {"X-Mashape-Key": ""}
#     url = "https://wordsapiv1.p.mashape.com/words/" + word
#
#     response = requests.get(url, headers=headers)
#
#     response = response.json()
#
#     if "frequency" in response.keys():
#         frequency = response['frequency']
#
#     else:
#         frequency = 0
#
#     return frequency
