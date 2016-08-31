import requests
import dictionary
import settings


##################################################################################################
# This program provides a number of starter words for a user, who then attempts to rhyme with    #
# those words as much as possible in a poem or song lyrics. Then, the program scores the user's  #
# work using RhymeBrain's rhyme score function. - Ben Johnson                                    #
##################################################################################################


def main():
    # Get the number of random words to find, then get them using the dictionary module.
    numOfStarterWords = settings.setNumOfStarterWords()
    numOfLines = settings.setNumOfLines()
    starterWords = dictionary.GetStarterWords(numOfStarterWords)
    possibleRhymes = {}         # Initialize a dictionary for all the possible rhymes and their scores.

    # Fill the dictionary of possible rhymes.
    possibleRhymes = GetPossibleRhymes(numOfStarterWords, possibleRhymes, starterWords)

    # Display the starter words and all the possible rhymes to make sure it's working.
    print(starterWords)
    print(possibleRhymes)

    # The user enters their lines.
    userLines = GetLines(numOfLines)
    totalScore = 0

    # Basic prototype of the scoring.
    # TODO: Strip out punctuation from the user's lines.
    # TODO: Move scoring out of main into its own method - add other scoring criteria.
    for line in userLines:
        words = line.split()
        for word, score in possibleRhymes.items():
            if word in words:
                totalScore += score

    print("Score: " + str(totalScore))


def GetPossibleRhymes(numOfStarterWords, possibleRhymes, starterWords):
    # A for loop that will grab all possible rhymes for the starter words and put them
    # into the possibleRhymes dictionary.
    for num in range(numOfStarterWords):
        targetURL = "http://rhymebrain.com/talk?function=getRhymes&word="
        targetURL += starterWords[num]
        response = requests.get(targetURL)
        x = response.json()
        for y in x:
            if y['score'] >= 192:   # Only take a result if its score is reasonably high.
                entry = {y['word']: y['score']}   # Only take the word and its score - maybe more later.
                possibleRhymes.update(entry)
    return possibleRhymes


def GetLines(numOfLines):
    # The method that takes user input. Uses a while loop to take lines from the user and put them into a list,
    # then returns that list of lines.
    lines = []

    print("Enter " + str(numOfLines) + " lines, pressing enter after each.")
    x = 0
    while x < numOfLines:
        line = input()
        lines.append(line)
        x += 1

    return lines


main()
