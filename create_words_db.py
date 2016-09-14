import sqlite3 as lite
import os

# This file isn't ever used when the program is running, it just shows how I made my database.


def CreateTable():
    # Connect to the database and create a cursor for that connection.
    db = lite.connect('words.db')
    cursor = db.cursor()

    # Drop the words table, then create it right this time.
    # All we need is an auto-incrementing primary key and a column for the word.
    cursor.execute('DROP TABLE WORDS')
    cursor.execute('''CREATE TABLE WORDS(id INTEGER PRIMARY KEY, word TEXT)''')

    db.commit()
    db.close()


def FillTable():
    db = lite.connect("words.db")
    cursor = db.cursor()

    # Open a file of the 10,000 most common English words - found at:
    # https://github.com/first20hours/google-10000-english
    cwd = os.getcwd()
    file = open(cwd + "/google-10000-english-usa.txt", 'r')

    # Loop through the file and add each line of it as a row in the words table.
    for word in file:
        cursor.execute("INSERT INTO WORDS(WORD) VALUES(?)", [word])

    db.commit()
    db.close()
    file.close()


def ReadLine():
    db = lite.connect("words2.db")
    cursor = db.cursor()

    # Display stuff to see how it's working.
    cursor.execute("select id, word from WORDS")
    rows = cursor.fetchall()
    print(rows)
    db.close()


def RemoveShort():
    db = lite.connect("words.db")
    cursor = db.cursor()

    # Remove short words. I wanted only words with 4 or more letters.
    # Since these still have a newline, the length we want is 5 or more.
    cursor.execute("DELETE FROM WORDS WHERE length(word) < 5")

    db.commit()
    db.close()


def RebuildDB():
    # Since we just deleted a bunch of entries, we won't be able to randomly
    # generate a line number as easily. So, I move the words that remain after
    # removing the short words to another database. (I realize now I could have
    # filtered the words as I took them from the file, but I guess the end result
    # is the same.)
    con = lite.connect("words.db")
    con2 = lite.connect("words2.db")
    c = con.cursor()
    c2 = con2.cursor()

    # Create the words table in the new database.
    c2.execute("DROP TABLE WORDS")
    c2.execute("CREATE TABLE WORDS(id INTEGER PRIMARY KEY, word TEXT)")

    # Take all the rows from the original database.
    c.execute("SELECT word FROM WORDS")

    # Use a while loop to insert the old rows into the new table.
    # The first line inside the loop de-tuples the data from the cursor.
    row = c.fetchone()
    while row:
        row = ''.join(row)
        c2.execute("INSERT INTO WORDS(word) VALUES(?)", [row])
        row = c.fetchone()

    con.commit()
    con2.commit()
    con.close()
    con2.close()


# CreateTable()
# FillTable()
# ReadLine()
# RemoveShort()
# RebuildDB()

# con = lite.connect("words2.db")
# c = con.cursor()
# c.execute("SELECT * FROM WORDS")
# rows = c.fetchall()
# print(rows)
# con.close()
