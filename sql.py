import sqlite3

# Connect to or create the users.db file
conn = sqlite3.connect('users.db')

# Create a cursor
c = conn.cursor()

# Create the users table
c.execute('''CREATE TABLE users
             (id INTEGER PRIMARY KEY, gender TEXT, partner_gender TEXT, uni TEXT, partner_uni TEXT)''')

# Commit the changes and close the connection
conn.commit()
conn.close()
