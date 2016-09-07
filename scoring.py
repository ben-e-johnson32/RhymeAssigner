import string


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

    output = "\nRhyme score: " + str(rhymeScore) + "\nSyllable Score: " + str(syllableScore) + \
             "\nTotal Score: " + str(rhymeScore + syllableScore) + "\n"

    return output


def CalculateSyllableScore(words, numOfSyllables):
    # A method to count the syllables in a line and compare it to the target syllables.
    # Most of this was taken from this stackoverflow question:
    # http://stackoverflow.com/questions/14541303/count-the-number-of-syllables-in-a-word
    # Basically, it looks at vowel placement to calculate the number of syllables. As you'll
    # quickly find, though, there are tons of exceptions to every rule in the English language.
    # I've found that it's not a very easy programming problem to solve - I'll either replace this
    # with another method if I find a better one or try to incorporate WordsAPI.

    count = 0
    vowels = 'aeiouy'

    for word in words:
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

    # Still have to fix this part. I plan to give some points if the number of syllables is close
    # to the target number.
    if count == numOfSyllables:
        score = 100
    # elif (count == numOfSyllables - 1) or (count == numOfSyllables + 1):
    #     score = 75
    # elif count == numOfSyllables - 2 or count == numOfSyllables + 2:
    #     score = 50
    # elif count == numOfSyllables - 3 or count == numOfSyllables + 3:
    #     score = 25
    else:
        score = 0

    return score



