from nltk.corpus import cmudict
from curses.ascii import isdigit
import sqlite3 as lite

# Like the create_words_db file, this just shows how I made the syllables database.


def CreateTable():
    # Create the table. Only took one try this time!
    connection = lite.connect("syllables.db")
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE syllables
                      (word TEXT PRIMARY KEY,
                       syllables INT);''')
    connection.commit()
    connection.close()


def FillTable():
    connection = lite.connect("syllables.db")
    cursor = connection.cursor()
    d = cmudict.dict()
    newD = {}

    # Read from the cmudict, take the word and syllable count. Expression for counting syllables (line 30) found here:
    # http://stackoverflow.com/questions/5513391/code-for-counting-the-number-of-syllables-in-the-words-in-a-file
    for key in d.keys():
        syllables = max([len(list(y for y in x if isdigit(y[-1]))) for x in d[key.lower()]])
        entry = {key: syllables}
        # Add the word and its syllable count to the new dictionary.
        newD.update(entry)

    # For every entry in the new dictionary, create a row in the syllables database.
    for key in newD.keys():
        cursor.execute("INSERT INTO syllables(word, syllables) VALUES(?, ?)", (key, newD.get(key)))

    connection.commit()
    connection.close()


def GetWord():
    # Just a way to get some output to make sure it's working.
    connection = lite.connect("syllables.db")
    cursor = connection.cursor()

    cursor.execute("SELECT word, syllables FROM syllables WHERE word=?", ("emancipation",))
    rows = cursor.fetchall()
    print(rows)
    connection.close()


# CreateTable()
# FillTable()
# GetWord()
