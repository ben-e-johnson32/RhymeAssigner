import random
import sqlite3 as lite


def GetWords(numberOfWords):
    # Connect to the database, create a cursor.
    connection = lite.connect("words2.db")
    cursor = connection.cursor()

    # Execute a statement to find the highest ID in the database,
    # which would also be the row count + 1.
    cursor.execute("SELECT max(id) FROM WORDS")
    rowCount = cursor.fetchone()[0] - 1

    # Two empty lists, one for the output words, one for the random line numbers.
    words = []
    lineNumbers = []

    # Generate some random numbers in the range of the number of rows in the database.
    for x in range(numberOfWords):
        lineNumbers.append(random.randint(0, rowCount))
    # For each of those numbers we generated, grab that word from the database and add it to output.
    for num in lineNumbers:
        cursor.execute("SELECT word FROM WORDS WHERE id={id}".format(id=num))
        words.append(cursor.fetchone()[0])

    # A while loop to strip off the newline characters.
    x = 0
    while x < len(words):
        words[x] = words[x].strip('\n')
        x += 1

    # Close the connection to the database and return the list of words.
    connection.close()
    return words
