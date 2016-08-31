import random

# TODO: Make this part faster? Takes a couple seconds.


def GetStarterWords(numberOfWords):

    # Open the built-in Mac dictionary file twice. I assume this isn't necessary.
    # TODO: Find a way to only open the dictionary file once.
    dictFile = open('/usr/share/dict/words', 'r')
    dictFile2 = open('/usr/share/dict/words', 'r')

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
        if line in lineNumbers:
            if len(word) < 7:
                starterWords.append(word)
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


